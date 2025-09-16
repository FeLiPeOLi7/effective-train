import tensorflow as tf
from tensorflow.keras.layers import Dense, Flatten
import numpy as np
from scipy.io import loadmat

#Fazendo o load dos dados
mnist = loadmat("mnist-original.mat")
mnist_data = mnist["data"].T
mnist_label = mnist["label"][0]

#Embaralhar pois se não seu conjunto de treino será composto apenas pelos dígitos '0', '1', '2', '3', '4', '5' e '6', 
# enquanto o conjunto de teste terá apenas '8' e '9'. (80/20)
indexes = np.arange(mnist_data.shape[0])
np.random.shuffle(indexes)

shuffled_data = mnist_data[indexes]
shuffled_labels = mnist_label[indexes]

#Separando em 80/20 os meus dados
cutting_edge = int(len(shuffled_data) * 0.8)

train_examples, val_examples = shuffled_data[:cutting_edge,:], shuffled_data[cutting_edge:,:]
train_labels, val_labels = shuffled_labels[:cutting_edge], shuffled_labels[cutting_edge:]

train_ds = tf.data.Dataset.from_tensor_slices((train_examples, train_labels))
val_ds = tf.data.Dataset.from_tensor_slices((val_examples, val_labels))

BATCH_SIZE = 32

train_ds = train_ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
val_ds = val_ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

model = tf.keras.models.Sequential([
    tf.keras.Input(shape=(784,)),
    Dense(units=32, activation='relu', name='layer1'),
    Dense(units=16, activation='relu', name='layer2'),
    Dense(units=10, activation='linear', name='layer3'),#10 classes (10 dígitos)
])

model.summary()

model.compile(optimizer=tf.keras.optimizers.Adam(0.001),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['sparse_categorical_accuracy'])

model.fit(
    train_ds,
    epochs=10,
    validation_data=val_ds,
)

#Prevendo com o modelo

exemplo_unico = val_examples[0]
rotulo_verdadeiro = val_labels[0]

#Mudar o formato da imagem para (1, 784)

exemplo_para_prever = exemplo_unico.reshape(1, 784)

#O predict retorna os logits (valores de saída) para cada uma das 10 classes
previsoes = model.predict(exemplo_para_prever)

#A função argmax retorna o índice (0 a 9) da maior probabilidade.
digito_predito = np.argmax(previsoes)

print(f"O modelo previu que a imagem é um: {digito_predito}")
print(f"O rótulo verdadeiro da imagem é: {rotulo_verdadeiro}")