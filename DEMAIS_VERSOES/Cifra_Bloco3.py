import sys, re
from unicodedata import normalize


#############################################
### FUNCOES PARA CIFRAR TEXTO (Cifra de Vigenere)

# ====================== FUNÇÕES AUXILIARES ======================

# Função para retirar da string os caracteres especiais e os espaços, além de colocar todas letras em maiúsculo
def processar_texto(texto):
    texto = normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII")
    texto = "".join(texto.split()).upper()
    return texto

# Função auxiliar para expandir a palavra-chave até o tamanho do texto
def expandir_palavra_chave(texto, palavra_chave):
    palavra_chave_expandida = ""
    indice_palavra_chave = 0
    
    for _ in range(len(texto)):
        palavra_chave_expandida += palavra_chave[indice_palavra_chave]
        indice_palavra_chave = (indice_palavra_chave + 1) % len(palavra_chave)
        
    return palavra_chave_expandida

# ====================== FUNÇÕES PRINCIPAIS ======================

# Função principal que codifica o texto claro usando a Cifra de Vigenère
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
### FUNCOES PARA CIFRAR TEXTO (Cifra de ADFGVX)
# Matriz da cifra ADFGVX (6x6), usando letras e dígitos
MATRIZ_ADFGVX = [
    ['A', 'B', 'C', 'D', 'E', 'F'],
    ['G', 'H', 'I', 'J', 'K', 'L'],
    ['M', 'N', 'O', 'P', 'Q', 'R'],
    ['S', 'T', 'U', 'V', 'W', 'X'],
    ['Y', 'Z', '0', '1', '2', '3'],
    ['4', '5', '6', '7', '8', '9']
]

LETTERS = ['A', 'D', 'F', 'G', 'V', 'X']


def encontrar_posicao(char):
    for i, linha in enumerate(MATRIZ_ADFGVX):
        if char in linha:
            return i, linha.index(char)
    raise ValueError(f"Caractere '{char}' não encontrado na matriz.")

def substituir(texto):
    resultado = ""
    for char in texto.upper():
        if char.isspace():
            resultado += " "
        elif char.isalnum():
            linha, coluna = encontrar_posicao(char)
            resultado += LETTERS[linha] + LETTERS[coluna]
    return resultado

def transpor(texto, CHAVE):
    colunas = sorted((CHAVE[i], i) for i in range(len(CHAVE)))
    texto_matriz = [texto[i:i + len(CHAVE)] for i in range(0, len(texto), len(CHAVE))]

    ultimo_tamanho = len(texto_matriz[-1])
    padding = len(CHAVE) - ultimo_tamanho
    if padding > 0:
        texto_matriz[-1] += 'X' * padding

    transposto = ""
    for _, indice in colunas:
        for linha in texto_matriz:
            if indice < len(linha):
                transposto += linha[indice]

    transposto += str(padding)  # Adicionar padding ao final
    return transposto

def cifra_texto_adfgvx(entrada, chave):
    texto_claro = entrada
   
    substituido = substituir(texto_claro)
    texto_cifrado = transpor(substituido, chave)

    return texto_cifrado

#############################################
### FUNCAO PARA CIFRAR TEXTO (Cifra de Alberti)
def cifra_texto_alberti(text, key):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'           # ALFABETO ALFA-NUMERICO PARA SUPORTAR TEXTOS COM LETRA E NUMEROS
    #alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'           # ALFABETO ALFA-NUMERICO PARA SUPORTAR TEXTOS COM LETRA E NUMEROS
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
            # Se o caractere não estiver no alfabeto, adicioná-lo sem cifragem
            texto_cifrado.append(conteudo[i])


    return ''.join(texto_cifrado)

#############################################
### FUNÇÃO PARA CIFRAR EM BLOCO
# USA AS CIFRAS DE ALBERT, ADFGVX E VIGENERE, NESTA ORDEM
# AMBAS CIFRAS DEVEM SUPORTAR OS MESMO TIPOS DE CARACTERES TANTO NA CIFRAGEM QUANTO NA DECIFRAGEM, AS USADAS AQUI SUPORTAM AS LETRAS DO ALFABETO E NÚMEROS DE 0 A 9, E ESPAÇOS EM BRANCO

def cifra_texto_bloco(text, key):
#    rodada = 2 

#    for i in range(rodada):
    Cifra_Alberti = cifra_texto_alberti(text, key)
    print(f"TEXTO CIFRADO EM ALBERTI: {Cifra_Alberti}")

    Cifra_ADFGVX = cifra_texto_adfgvx(Cifra_Alberti, key)
    print(f"TEXTO CIFRADO EM ADFGVX: {Cifra_ADFGVX}")

    Cifra_Vigenere = cifra_texto_vigenere(Cifra_ADFGVX, key)
    print(f"TEXTO CIFRADO EM VIGENERE: {Cifra_Vigenere} ")

    Cifra_Bloco = Cifra_Vigenere
    #text = Cifra_Bloco


    return Cifra_Bloco
    #return Cifra_ADFGVX
    

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

    with open(arquivo_texto, 'r', encoding='utf-8') as texto:         # ABRE O ARQUIVO
        texto_claro = texto.read().upper().strip()         # COPIA O CONTEUDO DO ARQUIVO DE TEXTO PARA A VARIAVEL CONTEUDO E COLOCA TUDO PARA MAIUSCULO REMOVENDO ESPAÇOS EXTRAS
    key = chave.upper()                             # COLOCA A CHAVE TUDO EM MAIUSCULO

    resposta_texto_cifrado = cifra_texto_bloco(texto_claro, key)
    #print(f"O Texto cifrado eh:  {resposta_texto_cifrado}")

    with open("TEXTO_CIFRADO.txt", 'w', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(resposta_texto_cifrado)

    print("Texto cifrado salvo em 'TEXTO_CIFRADO.txt'")
