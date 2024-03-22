import PySimpleGUI as sg

layout= [ #Layout com 6 'linhas', cada colchete é uma dessas 'linhas'
    [sg.Text('Usuário')],
    [sg.Input(key='usuario')],
    [sg.Text('Senha')],
    [sg.Input(key='senha')],
    [sg.Button('Login')],
    [sg.Text('', key='mensagem')],
]

window = sg.Window('Login',layout=layout) #Cria a janela

while True: #Loop de eventos (Enquanto estiver aberto veja o quê está acontecendo)
    event, values = window.read()
    if event == sg.WIN_CLOSED: #Se clicarem no X é para fechar totalmente a aplicação
        break
    elif event == 'Login':
        senha_correta = '123'
        usuario_correto = 'Valdemar'
        usuario = values['usuario']
        senha = values['senha']
        if senha == senha_correta and usuario == usuario_correto:
            window['mensagem'].update("Login feito com sucesso!")
        else:
            window['mensagem'].update("Usuário ou senha incorreto(s)!")
