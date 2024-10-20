'''
Objetivo de ler um email não lido do Gmail,
 e utilizar um chatbot para criar uma resposta e enviar um email com essa resposta
Para que o chatbot responda corretamente ele precisar ser treinado com vários emails
 e suas respostas
'''
import os
import re
import csv
import pickle
# Gmail API
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# encoding/decoding mensagens
from base64 import urlsafe_b64decode, urlsafe_b64encode
# Utilizando mime para ler textos e anexos
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

# Aqui informamos nosso email (o mesmo que fizemos na GMAIL API) para ler/escrever/etc
SCOPES = ['https://mail.google.com/']
email = 'sender@gmail.com'

def autentica_gmail():
    creds = None
    # token.pickle armazena o token do usuário, para que não seja necessário logar a todo momento
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # Se nenhuma eh valida, apenas deixa o usuário logar
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Salva o token para a prox vez
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

# Pega o serviço do Gmail API
service = autentica_gmail()

def clean_email_text(text):
    """
    Se o texto contiver a expressão 'Em ... escreveu', retorna a parte antes dessa expressão.
    Caso contrário, retorna o texto original.
    """
    # Expressão regular que busca o padrão 'Em ... escreveu'
    pattern = r"Em\s.*escreveu:"

    return re.split(pattern, text, flags=re.DOTALL)[0].replace("\n", " ").replace("\r", " ").strip()

def escreve_csv(sender, subject, body, date, response_sender=None, response_body=None, response_date=None):
    """
    Appends the email data to a CSV file.
    """
    file_exists = os.path.isfile("emails.csv")

    with open("emails.csv", mode="a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Sender", "Subject", "Body", "Date", "ResponseSender", "ResponseBody", "ResponseDate"])
        
        writer.writerow([sender, subject, body, date, response_sender, response_body, response_date])

def parse_parts(parts):
    """
    Destrincha as partes do gmail
    """
    if parts:
        for part in parts:
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            if part.get("parts"):
                # Recursividade na funcao caso ainda haja partes
                parse_parts(part.get("parts"))
            if mimeType == "text/plain":
                # Se eh um texto de conteudo, a gente printa ele
                if data:
                    text = urlsafe_b64decode(data).decode()
                    text_clean = clean_email_text(text)
                    return clean_email_text(text_clean)
    return ""

def extract_email_address(sender):
    """
    Extrai só o email
    """
    
    match = re.search(r'<(.*?)>', sender)
    if match:
        return match.group(1)  # Retorna o email dentro dos < >
    return sender  

def le_thread(service):
    '''
    Isso que ira nos permitir treinar nosso modelo para responder automaticamente os email
    '''
    try:
        threads = (
            service.users().threads().list(userId="me").execute().get("threads", [])
        )
        for thread in threads:
            tdata = (
                service.users().threads().get(userId="me", id=thread["id"]).execute()
            )
            nmsgs = len(tdata["messages"])
            last = len(tdata['messages'])

            if nmsgs > 1:
                for i in range(last-1):
                    current_msg = tdata["messages"][i]["payload"]
                    current_parts = current_msg.get("parts")
                    current_subject = sender = date = ""
                    for header in current_msg["headers"]:
                        name = header.get("name")
                        if name.lower() == "from":
                            sender = extract_email_address(header["value"])
                        if name.lower() == "date":
                            date = header["value"]
                        if name.lower() == "subject":
                            current_subject = header["value"]
                    current_body = parse_parts(current_parts)

                    # Próxima mensagem (resposta)
                    next_msg = tdata["messages"][i+1]["payload"]
                    next_parts = next_msg.get("parts")
                    response_sender = response_body = response_date = ""
                    for header in next_msg["headers"]:
                        name = header.get("name")
                        if name.lower() == "from":
                            response_sender = extract_email_address(header["value"])
                        if name.lower() == "date":
                            response_date = header["value"]
                    response_body = parse_parts(next_parts)

                    # Escreve o par (email atual + resposta)
                    if current_subject and current_parts:  # Certifica-se de que há assunto e partes
                        escreve_csv(sender, current_subject, current_body, date, response_sender, response_body, response_date)
                

        return threads
    except Exception as error:
        print(f'Deu erro: {error}')

def le_msg_nova(service):
    try:
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages',[])#Lista de mensagens
        if not messages:
            print("Nao tem mensagens")
        else:
            for message in messages:
                #Essa linha solicita uma mensagem especifica do usuario autenticado para a API
                msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
                payload = msg['payload']#Destrincha a carga da mensagem
                headers = payload.get("headers")#Destrincha da mensagem o cabecalho
                parts = payload.get("parts")
                if headers:
                    for header in headers:
                        name = header.get("name")
                        value = header.get("value")

                        if name.lower() == "from:":
                            print("From: ", value)
                        if name.lower() == "to":
                            print("To:", value)
                        if name.lower() == "subject":
                            print("Subject:", value)
                        if name.lower() == "date":
                            print("Date:", value)
                parse_parts(parts)
                #Marca a mensagem como lida
                msg  = service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()
    except Exception as error:
        print(f'Deu erro: {error}')

le_thread(service)
