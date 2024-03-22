palavra_secreta = "banana".upper()
letras_descobertas = []
enforcou = False
acertou = False
erros = 0

print("    Jogo da Forca    ")

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

for i in range(0, len(palavra_secreta)):
    letras_descobertas.append("_")

while acertou == False:
    letra = str(input("Digite a letra: "))
    letra = letra.upper()

    for i in range(0, len(palavra_secreta)):
        if letra in palavra_secreta[i]:
            letras_descobertas[i] = letra
        else:
            erros += 1
            chances = 7 - erros
            enforcou = erros == 7
            acertou = "_" not in letras_descobertas
            desenha_forca(erros)
            print(letras_descobertas[i])
            print(f"Você errou a letra, restam {chances} chances")

if acertou:
            print("Parabéns! Você acertou! A palavra era: {}".format(palavra_secreta))
elif enforcou:
            print("Você foi enforcado...")

print("Fim do jogo")
