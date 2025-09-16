## Classificador de Dígitos Manuscritos com Redes Neurais

Este projeto demonstra a criação, o treino e a avaliação de um modelo de rede neural para classificar dígitos manuscritos (0 a 9) usando o famoso dataset MNIST.

O modelo é construído com a biblioteca TensorFlow/Keras e alcançou uma acurácia de 94% no conjunto de dados de validação.


# O código foi desenvolvido para ilustrar as etapas essenciais de um projeto de aprendizado de máquina, incluindo:

- Pré-processamento de Dados: Carregamento e manipulação de arrays com a biblioteca NumPy.

- Divisão do Dataset: Separação dos dados em conjuntos de treino e validação (80/20).

- Construção do Modelo: Criação de uma rede neural simples, mas eficiente, usando camadas densas (Dense).

- Treino: Otimização do modelo para aprender a partir dos dados.

- Validação: Uso de um conjunto de dados separado para monitorar o desempenho do modelo durante o treino.

- Predição: Demonstração de como usar o modelo treinado para prever um dígito a partir de uma imagem de entrada personalizada (.png).

# Como Executar o Projeto

Siga os passos abaixo para rodar o projeto em sua máquina.

Pré-requisitos

Certifique-se de que você tem o Python instalado. Em seguida, instale as bibliotecas necessárias no seu ambiente virtual:

```bash
pip install tensorflow numpy scipy
```

# Desempenho do Modelo

Durante o treino, o modelo atingiu uma acurácia de 94% no conjunto de validação, demonstrando uma boa capacidade de generalização e de reconhecimento de dígitos que ele não viu durante a fase de treino.