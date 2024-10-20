# Gmail API
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import smtplib
from email.mime.text import MIMEText
import joblib
from email_reader import extract_email_address, parse_parts, service

pipeline = joblib.load('email_responder_model.pkl')
sender = 'sender@gmail.com'
password = 'yourpassword'

def respondeMensagem(message):
    #Faz uma predição da resposta
    predicted_response = pipeline.predict([message])

    return predicted_response[0]

def send_email(response, recipient):
    msg = MIMEText(response)  # Create the email content
    msg['Subject'] = 'Resposta ao email'  # You can customize the subject
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipient, msg.as_string())
    print(f"Mensagem enviada de {sender} para {recipient} como {msg.as_string}!")

def le_msg_nova(service):
    try:
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages',[])#Lista de mensagens
        response = ""
        if not messages:
            print("Nao tem mensagens")
        else:
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
                payload = msg['payload']#Destrincha a carga da mensagem
                headers = payload.get("headers")#Destrincha da mensagem o cabecalho
                parts = payload.get("parts")

                message_body = parse_parts(parts)
                response = respondeMensagem(message_body)

                for header in headers:
                    if header['name'].lower() == "from":
                        recipient_email = extract_email_address(header['value'])
                        send_email(response, recipient_email)

                #Marca a mensagem como lida
                msg  = service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()
    except Exception as error:
        print(f'Deu erro: {error}')

le_msg_nova(service)
