### CHATBOT DO DISCORD COM GEMINI

Simples bot do discord que utiliza a API do Gemini para interagir com usuários de um servidor, sendo útil para informar coisas
rápidas e manter uma conversa.

´´´python
message_history = {}

message_history[user_id].append(prompt)
context = "\n".join(message_history[user_id])
´´´
Da contexto para o bot através das mensagens antigas
