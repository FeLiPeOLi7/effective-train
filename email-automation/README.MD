Projeto que utiliza o gmail API para utilizar os emails próprios como um dataset de treino, que consegue responder emails automaticamente, note que quanto mais dados ele tiver
mais ele consegue responder de forma apurada.

```python
# Escreve o par (email atual + resposta)
if current_subject and current_parts:  # Certifica-se de que há assunto e partes
  escreve_csv(sender, current_subject, current_body, date, response_sender, response_body, response_date)
```

Isso que irá nos permitir criar um dataset para nosso modelo e permitir que ele crie uma resposta.

```python
# Carrega o dataset produzido anteriormente com os emails da pessoa
data = pd.read_csv('emails_extended.csv')

def respondeMensagem(message):
    #Faz uma predição da resposta
    predicted_response = pipeline.predict([message])

    return predicted_response[0]
```
