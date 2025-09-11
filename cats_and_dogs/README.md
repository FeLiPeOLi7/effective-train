# Classificador de Gatos vs. Cães

## Visão Geral

Este projeto implementa um classificador binário de imagens usando uma rede neural convolucional (CNN) para distinguir entre imagens de gatos e cães. O modelo foi construído com TensorFlow/Keras e treinado no conjunto de dados [Cats vs. Dogs do Kaggle](https://www.kaggle.com/c/dogs-vs-cats/data), que contém aproximadamente 25.000 imagens. As imagens são pré-processadas, divididas em conjuntos de treinamento e validação, e usadas para treinar um modelo que classifica novas imagens como "gato" ou "cachorro" com alta precisão.

O projeto inclui:
- Um script para organizar as imagens em subdiretórios `cats` e `dogs`.
- Um modelo de Redes Neurais para classificação.
- Visualização de métricas de treinamento (acurácia e perda).
- Funcionalidade de predição para imagens individuais.

## Conjunto de Dados

O conjunto de dados utilizado é o Cats vs. Dogs do Kaggle, contendo ~25.000 imagens (~12.500 gatos, ~12.500 cães). As imagens são divididas da seguinte forma:
- **Treinamento**: ~20.000 imagens (80% do conjunto, com `validation_split=0.2`).
- **Validação**: ~5.000 imagens (20% do conjunto).
- **Estrutura de Diretórios**:
  - Imagens originais estão em `./train`.
  - As imagens são copiadas para `./tmp/cats` (primeiras 12.499 imagens) e `./tmp/dogs` (imagens restantes) usando a função `split_images`, que cria a pasta `./tmp` caso ela não exista.

## Requisitos

- Python 3.8+
- TensorFlow 2.x
- NumPy

Instale as dependências com:
```bash
pip install tensorflow numpy
```

## Arquitetura do Modelo

O modelo utiliza uma rede neural convolucional (CNN) com a seguinte arquitetura:
- **Entrada**: Imagens redimensionadas para 150x150 pixels com 3 canais de cor (RGB).
- **Camadas** (CNN personalizada):
  - Conv2D (16 filtros, 3x3, ReLU) + MaxPooling2D (2x2)
  - Conv2D (32 filtros, 3x3, ReLU) + MaxPooling2D (2x2)
  - Conv2D (64 filtros, 3x3, ReLU) + MaxPooling2D (2x2)
  - Flatten
  - Dense (512 unidades, ReLU)
  - Dense (1 unidade, sigmoid) | Apenas uma unidade, pois é um classificador binário
- **Função de Perda**: Binary Crossentropy
- **Otimizador**: Adam (taxa de aprendizado = 0.0001)
- **Métricas**: Acurácia

## Uso

1. **Executar o Script**:
   - Salve o código como `cat_dog_classifier.py` e execute:
     ```bash
     python cat_dog_classifier.py
     ```
   - O script irá:
     - Dividir as imagens em `./tmp/cats` e `./tmp/dogs`.
     - Treinar o modelo por 15 épocas.
     - Exibir acurácia e perda de treinamento/validação.
     - Solicitar uma imagem de teste (`dog.jpeg` ou `kitten.jpg`) e exibir a predição.

2. **Testar Predições**:
   - Insira o nome de uma imagem de teste (ex.: `dog.jpeg`).
   - O modelo retorna uma probabilidade e classifica a imagem como "gato" ou "cachorro" (baseado em `class_indices`).

## Resultados

O modelo foi treinado com ~20.000 imagens e uma divisão de validação de 20% (~5.000 imagens). Resultados de uma execução recente:
- **Treinamento**:
  - Acurácia: 99.55%
  - Perda: 0.0149
- **Validação** (de uma execução anterior):
  - Acurácia: 74.87%
  - Perda: 0.8665
- **Análise**:
  - Alta acurácia e baixa perda no treinamento indicam bom aprendizado no conjunto de treinamento.
  - Acurácia de validação mais baixa e alta perda sugerem **overfitting**, provavelmente devido à falta de aumento de dados (*data augmentation*) e ao treinamento de uma CNN do zero.

## Melhorias Futuras

- **Melhorar o Aumento de Dados**: Aumentar a intensidade do aumento (ex.: brilho, espelhamento vertical) para reduzir ainda mais o *overfitting*.
- **Utilizar ferramentas para visualizar gráficos**: Utilizar ferramentas como o matplotlib poderiam deixar o aprendizado do modelo mais visual para nós humanos.
