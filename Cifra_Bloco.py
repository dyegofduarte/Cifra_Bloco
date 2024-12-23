import sys, re, string
from unicodedata import normalize

#############################################
### FUNÇÕES PARA CIFRAR TEXTO (Cifra de Affine)
def cifra_texto_affine(texto_claro, key):
    # Define o alfabeto estendido com letras, números e espaço
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
    m = len(alfabeto)  # Tamanho do alfabeto

    # Calcula os valores "a" e "b" a partir da chave
    a = sum(ord(char) for char in key) % m  # Usa a soma dos códigos ASCII da chave
    b = len(key) % m  # Usa o comprimento da chave como "b"

    # Garante que "a" seja coprimo a "m" (usando tentativa e erro simples)
    while gcd(a, m) != 1:
        a = (a + 1) % m

    # Mapeia cada caractere do texto claro usando a fórmula da cifra de Afim
    texto_cifrado = ""
    for char in texto_claro:
        if char in alfabeto:
            x = alfabeto.index(char)
            y = (a * x + b) % m
            texto_cifrado += alfabeto[y]
        else:
            texto_cifrado += char  # Mantém caracteres que não estão no alfabeto

    return texto_cifrado

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

#############################################
### FUNÇÕES PARA CIFRAR TEXTO (Cifra de Vigenere)

# ====================== FUNÇÕES AUXILIARES ======================

# Função para retirar caracteres especiais e espaços, além de colocar todas letras em maiúsculo
def processar_texto(texto):
    texto = normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII")
    texto = "".join(texto.split()).upper()
    return texto

# Função para expandir a palavra-chave até o tamanho do texto
def expandir_palavra_chave(texto, palavra_chave):
    palavra_chave_expandida = ""
    indice_palavra_chave = 0
    for _ in range(len(texto)):
        palavra_chave_expandida += palavra_chave[indice_palavra_chave]
        indice_palavra_chave = (indice_palavra_chave + 1) % len(palavra_chave)
    return palavra_chave_expandida

# Função principal para cifrar com Vigenère
def cifra_texto_vigenere(texto_claro, palavra_chave):
    texto_cifrado = ""
    palavra_chave_repetida = expandir_palavra_chave(texto_claro, palavra_chave)
    for i in range(len(texto_claro)):
        char_texto = texto_claro[i]
        char_chave = palavra_chave_repetida[i]
        if char_texto.isalpha():
            indice_texto = ord(char_texto) - ord('A')
            indice_chave = ord(char_chave) - ord('A')
            indice_cifrado = (indice_texto + indice_chave) % 26
            letra_cifrada = chr(indice_cifrado + ord('A'))
        elif char_texto.isdigit():
            indice_texto = ord(char_texto) - ord('0')
            indice_chave = ord(char_chave) - ord('0')
            indice_cifrado = (indice_texto + indice_chave) % 10
            letra_cifrada = chr(indice_cifrado + ord('0'))
        else:
            letra_cifrada = char_texto
        texto_cifrado += letra_cifrada
    return texto_cifrado


#############################################
### FUNÇÕES PARA CIFRAR TEXTO (Cifra de Alberti)
def cifra_texto_alberti(text, key):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    texto_cifrado = []
    conteudo = text
    chave_expandida = (key * (len(conteudo) // len(key) + 1))[:len(conteudo)]
    for i in range(len(conteudo)):
        if conteudo[i] in alfabeto:
            pos_texto = alfabeto.find(conteudo[i])
            pos_chave = alfabeto.find(chave_expandida[i])
            pos_cifrada = (pos_chave - pos_texto) % len(alfabeto)
            texto_cifrado.append(alfabeto[pos_cifrada])
        else:
            texto_cifrado.append(conteudo[i])
    return ''.join(texto_cifrado)

#############################################
### FUNÇÃO PARA CIFRAR EM BLOCO
# REALIZA A CIFRAGEM USANDO AS CIFRAS DE ALBERTI, AFFINE E VIGENERE NESTA ORDEM

def cifra_texto_bloco(text, key):
    tamanho_bloco=16
    blocos = [text[i:i + tamanho_bloco] for i in range(0, len(text), tamanho_bloco)]
    texto_cifrado = ""
    for bloco in blocos:
        rodada = 2
        for _ in range(rodada):
            bloco = cifra_texto_alberti(bloco, key)
            bloco = cifra_texto_affine(bloco, key)
            bloco = cifra_texto_vigenere(bloco, key)
        texto_cifrado += bloco
    return texto_cifrado

#############################################
### FUNÇÃO PARA MOSTRAR MANUAL
def manual():
    print("Formas de uso: python Cifra_Texto.py <Chave> <Arquivo com texto a Cifrar>")
    sys.exit(1)

#############################################
### FUNÇÃO MAIN
if __name__ == "__main__":
    if len(sys.argv) < 3:
        manual()
    chave = sys.argv[1]
    arquivo_texto = sys.argv[2]

    with open(arquivo_texto, 'r', encoding='utf-8') as texto:
        texto_claro = texto.read().upper().strip()
    key = chave.upper()

    resposta_texto_cifrado = cifra_texto_bloco(texto_claro, key)
    
    print(f"TEXTO CIFRADO: {resposta_texto_cifrado}")

    with open("TEXTO_CIFRADO.txt", 'w', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(resposta_texto_cifrado)
    print("Texto cifrado salvo em 'TEXTO_CIFRADO.txt'")

