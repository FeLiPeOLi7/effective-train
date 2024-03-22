# Objetivo é fazer um jogo da forca onde escolhemos uma palavra e tentamos acertar as letras, onde só
# podemos errar 7x
# Primeiro pegamos a palavra que queremos pelo sistema e se o user n escrever pedimos para ele
word = str(input("Me de uma palavra: "))
#Lista de letras que tem na palavra
founds_letter = []
#Depois decodificamos ela em traços de acordo com seu tamanho
for i in range(len(word)):
    founds_letter.append("-")

# Variáveis que dizem se vc ganhou, errou ou perdeu
acertou = False
erros = 0
enforcou = False

#Desenha a forca
def desenha_forca(erros):
    print("  _______     ")
    print(" |/      |    ")

    if(erros == 1):
        print(" |      (_)   ")
        print(" |            ")
        print(" |            ")
        print(" |            ")

    if(erros == 2):
        print(" |      (_)   ")
        print(" |      \     ")
        print(" |            ")
        print(" |            ")

    if(erros == 3):
        print(" |      (_)   ")
        print(" |      \|    ")
        print(" |            ")
        print(" |            ")

    if(erros == 4):
        print(" |      (_)   ")
        print(" |      \|/   ")
        print(" |            ")
        print(" |            ")

    if(erros == 5):
        print(" |      (_)   ")
        print(" |      \|/   ")
        print(" |       |    ")
        print(" |            ")

    if(erros == 6):
        print(" |      (_)   ")
        print(" |      \|/   ")
        print(" |       |    ")
        print(" |      /     ")

    if (erros == 7):
        print(" |      (_)   ")
        print(" |      \|/   ")
        print(" |       |    ")
        print(" |      / \   ")

    print(" |            ")
    print("_|___         ")
    print()

# Enquanto você não tiver acertado ou sido enforcado você pode jogar
while acertou == False and not enforcou:#Pega a letra que o user quer
    letter = str(input("Digite uma letra ou a palavra: "))
    acertou_letra = False #Evita que a mesma letra seje utilizada novamente

    if letter in word: #Se tem a letra na palavra
        #Cada letra certa que digitarmos deve trocar o traço por sua letra
        for i in range(len(word)):
            if word[i] == letter:
                founds_letter[i] = letter
                acertou_letra = True
        #Se a letra estiver certa, falar que acertou, se estiver certa mas já foi utilizada, informar isso ao usuário.
        print(founds_letter)
        if acertou_letra:
            print("Você acertou a letra!")
        else:
            print("Letra já encontrada!")
    else: #Caso a letra não esteje correta aumentar os números de erros e diminuir as chances
        erros += 1
        chances = 7 - erros
        print(f"Você errou a letra, restam {chances} chances")
        desenha_forca(erros)
# Verifica se ainda tem letras para serem descobertas
    if '-' not in founds_letter:
        acertou = True
# Verifica se o usuário será enforcado
    if erros == 7:
        enforcou = True
# Verifica se o usuário acertou
if acertou:
    print("Parabéns, você ganhou!")
else:
    print("Você foi enforcado! A palavra era:", word)
