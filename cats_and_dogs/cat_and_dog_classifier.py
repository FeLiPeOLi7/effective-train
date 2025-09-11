import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Dense, Flatten, Rescaling, Conv2D, MaxPooling2D, Dropout
from tensorflow.keras.preprocessing import image
import os
import shutil

def split_images(source_dir, cat_dir, dog_dir, cat_count=12499):
    os.makedirs(cat_dir, exist_ok=True)
    os.makedirs(dog_dir, exist_ok=True)
    
    files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
    
    files.sort()
    
    #Separa os gatos do cachorro, os primeiros 12500 elementos são gatos, o resto são cachorros
    cat_files = files[:cat_count]
    dog_files = files[cat_count:]
    
    #Passa os arquivos para uma pasta temporária, melhor para trabalhar com meus dados
    for file in cat_files:
        src_path = os.path.join(source_dir, file)
        dst_path = os.path.join(cat_dir, file)
        shutil.copy(src_path, dst_path)
    
    for file in dog_files:
        if(file != "cat.9999.jpg"):
            src_path = os.path.join(source_dir, file)
            dst_path = os.path.join(dog_dir, file)
            shutil.copy(src_path, dst_path)
        else:
            src_path = os.path.join(source_dir, file)
            dst_path = os.path.join(cat_dir, file)
            shutil.copy(src_path, dst_path)

def main():
    source_dir = './train' 
    cat_dir = './tmp/cats' 
    dog_dir = './tmp/dogs'
    
    split_images(source_dir, cat_dir, dog_dir)
    train_dir = './tmp'

    # De 0 até 255 para 0 até 1, mais fácil da NN entender
    train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.20)

    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(150, 150),
        batch_size=25,
        subset='training',
        class_mode='binary',
    )

    test_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.20)

    validation_generator = test_datagen.flow_from_directory(
        train_dir,
        target_size=(150, 150),
        batch_size=25,
        subset='validation',
        class_mode='binary',
    )

    # Print the number of files
    print(f"Number of training images: {len(train_generator.filenames)}")
    print(f"Number of validation images: {len(validation_generator.filenames)}")

    model = tf.keras.models.Sequential([
        Conv2D(16, (3,3), activation='relu', input_shape=(150, 150, 3), name='layer1'),
        MaxPooling2D(2,2),
        Conv2D(32, (3,3), activation='relu', name='layer2'),
        MaxPooling2D(2,2),
        Conv2D(64, (3,3), activation='relu', name='layer3'),
        MaxPooling2D(2,2),
        Flatten(),
        Dense(units=512, activation='relu'),
        Dense(units=1, activation='sigmoid')
    ])

    model.summary()

    model.compile(
        loss=tf.keras.losses.BinaryCrossentropy(),
        optimizer=tf.keras.optimizers.Adam(0.001),
        metrics=['accuracy'],
    )

    #Calcula a quantidade de passos necessários
    total_train_images = len(train_generator.filenames)
    total_val_images = len(validation_generator.filenames)
    steps_per_epoch = total_train_images // 25
    validation_steps = total_val_images // 25

    model.fit(
        train_generator,
        steps_per_epoch=steps_per_epoch,
        epochs=15,
        validation_data=validation_generator,
        validation_steps=validation_steps,
        verbose=2
    )

    img_input = input("Qual imagem você vai querer usar? dog.jpeg ou kitten.jpg: ")
    img_path = './'+img_input
    #Redimensionar a imagem
    img = image.load_img(img_path, target_size=(150, 150))
    #Converter para array
    img_array = image.img_to_array(img)
    # Adicionar dimensão de batch: (1, 180, 180, 3)
    img_array = np.expand_dims(img_array, axis=0)
    # Normalização
    img_array = img_array / 255.0

    prediction = model.predict(img_array)

    if prediction[0][0] < 0.5:
        print("É um gato!")
    else:
        print("É um cachorro")


if __name__ == "__main__":
    main()
