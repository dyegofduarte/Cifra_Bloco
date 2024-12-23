import sys, re, string
from unicodedata import normalize

#############################################
### FUNÇÕES PARA DECIFRAR TEXTO (Cifra de Affine)
def decifra_texto_affine(texto_cifrado, key):
    # Define o alfabeto estendido com letras, números e espaço
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
    m = len(alfabeto)  # Tamanho do alfabeto

    # Calcula os valores "a" e "b" a partir da chave
    a = sum(ord(char) for char in key) % m  # Usa a soma dos códigos ASCII da chave
    b = len(key) % m  # Usa o comprimento da chave como "b"

    # Garante que "a" seja coprimo a "m" (usando tentativa e erro simples)
    while gcd(a, m) != 1:
        a = (a + 1) % m

    # Calcula o inverso multiplicativo de "a" modulo "m"
    a_inv = mod_inverse(a, m)

    # Decifra cada caractere do texto cifrado usando a fórmula inversa da cifra de Afim
    texto_decifrado = ""
    for char in texto_cifrado:
        if char in alfabeto:
            y = alfabeto.index(char)
            x = (a_inv * (y - b)) % m
            texto_decifrado += alfabeto[x]
        else:
            texto_decifrado += char  # Mantém caracteres que não estão no alfabeto

    return texto_decifrado

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    # Calcula o inverso multiplicativo de "a" modulo "m" usando o algoritmo estendido de Euclides
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"O inverso multiplicativo de {a} mod {m} não existe.")


#############################################
### FUNÇÕES PARA DECIFRAR TEXTO (Cifra de Vigenere)

# ====================== FUNÇÕES AUXILIARES ======================

# Função para expandir a palavra-chave até o tamanho do texto
def expandir_palavra_chave(texto, palavra_chave):
    palavra_chave_expandida = ""
    indice_palavra_chave = 0
    for _ in range(len(texto)):
        palavra_chave_expandida += palavra_chave[indice_palavra_chave]
        indice_palavra_chave = (indice_palavra_chave + 1) % len(palavra_chave)
    return palavra_chave_expandida

# Função principal para decifrar com Vigenère
def decifra_texto_vigenere(texto_cifrado, palavra_chave):
    texto_decifrado = ""
    palavra_chave_repetida = expandir_palavra_chave(texto_cifrado, palavra_chave)
    for i in range(len(texto_cifrado)):
        char_texto = texto_cifrado[i]
        char_chave = palavra_chave_repetida[i]
        if char_texto.isalpha():
            indice_texto = ord(char_texto) - ord('A')
            indice_chave = ord(char_chave) - ord('A')
            indice_decifrado = (indice_texto - indice_chave) % 26
            letra_decifrada = chr(indice_decifrado + ord('A'))
        elif char_texto.isdigit():
            indice_texto = ord(char_texto) - ord('0')
            indice_chave = ord(char_chave) - ord('0')
            indice_decifrado = (indice_texto - indice_chave) % 10
            letra_decifrada = chr(indice_decifrado + ord('0'))
        else:
            letra_decifrada = char_texto
        texto_decifrado += letra_decifrada
    return texto_decifrado

#############################################
### FUNÇÕES PARA DECIFRAR TEXTO (Cifra de Alberti)
def decifra_texto_alberti(text, key):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    texto_decifrado = []
    chave_expandida = (key * (len(text) // len(key) + 1))[:len(text)]
    for i in range(len(text)):
        if text[i] in alfabeto:
            pos_cifrada = alfabeto.find(text[i])
            pos_chave = alfabeto.find(chave_expandida[i])
            pos_texto = (pos_chave - pos_cifrada) % len(alfabeto)
            texto_decifrado.append(alfabeto[pos_texto])
        else:
            texto_decifrado.append(text[i])
    return ''.join(texto_decifrado)

#############################################
### FUNÇÃO PARA DECIFRAR EM BLOCO
# REALIZA A DECIFRAGEM USANDO AS CIFRAS DE VIGENERE, AFFINE E ALBERTI NESTA ORDEM

def decifra_texto_bloco(text, key):
    tamanho_bloco=16
    blocos = [text[i:i + tamanho_bloco] for i in range(0, len(text), tamanho_bloco)]
    texto_decifrado = ""
    for bloco in blocos:
        rodada = 2
        for _ in range(rodada):
            bloco = decifra_texto_vigenere(bloco, key)
            bloco = decifra_texto_affine(bloco, key)
            bloco = decifra_texto_alberti(bloco, key)
        texto_decifrado += bloco
    return texto_decifrado

#############################################
### FUNÇÃO PARA MOSTRAR MANUAL
def manual():
    print("Formas de uso: python Decifra_Texto.py <Chave> <Arquivo com texto a Decifrar>")
    sys.exit(1)

#############################################
### FUNÇÃO MAIN
if __name__ == "__main__":
    if len(sys.argv) < 3:
        manual()
    chave = sys.argv[1]
    arquivo_texto = sys.argv[2]

    with open(arquivo_texto, 'r', encoding='utf-8') as texto:
        texto_cifrado = texto.read().strip()
    
    key = chave.upper()
    
    resposta_texto_decifrado = decifra_texto_bloco(texto_cifrado, key)
    
    print(f"TEXTO DECIFRADO: {resposta_texto_decifrado}")

    with open("TEXTO_DECIFRADO.txt", 'w', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(resposta_texto_decifrado)
    print("Texto decifrado salvo em 'TEXTO_DECIFRADO.txt'")

