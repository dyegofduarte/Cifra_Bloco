import sys, re


#############################################
### FUNCOES PARA CIFRAR TEXTO (Cifra de Bacon)

# GERA A TABELA DE CIFRA DE BACON, "I" E "J" SÃO O MESMO CÓDIGO IGUAL A "U" E "V"
def gerar_tabela_bacon():
    alfabeto = "ABCDEFGHIKLMNOPQRSTUWXYZ"  # I/J e U/V são combinados
    tabela = {}
    for i, letra in enumerate(alfabeto):
        binario = f"{i:05b}".replace("0", "A").replace("1", "B")
        tabela[letra] = binario
    return tabela

# CIFRA 
def cifra_texto_bacon(mensagem):
    tabela = gerar_tabela_bacon()
    mensagem = mensagem.upper().replace("J", "I").replace("V", "U")
    codificada = "".join(tabela[letra] for letra in mensagem if letra in tabela)
    return codificada


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
# USA AS CIFRAS DE ALBERT, ADFGVX E BACON, NESTA ORDEM

def cifra_texto_bloco(text, key):
#    rodada = 2 

#    for i in range(rodada):
    Cifra_Alberti = cifra_texto_alberti(text, key)
    print(f"TEXTO CIFRADO EM ALBERTI: {Cifra_Alberti}")
    Cifra_ADFGVX = cifra_texto_adfgvx(Cifra_Alberti, key)
    print(f"TEXTO CIFRADO EM ADFGVX: {Cifra_ADFGVX}")
    Cifra_Bacon = cifra_texto_bacon(Cifra_ADFGVX)
    #print(f"TEXTO CIFRADO EM BACON: {Cifra_Bacon} ")
    #Cifra_Bloco = Cifra_Bacon
    #text = Cifra_Bloco

    #return Cifra_Bloco
    return Cifra_ADFGVX


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

    with open(arquivo_texto, 'r') as texto:         # ABRE O ARQUIVO
        texto_claro = texto.read().upper().strip()         # COPIA O CONTEUDO DO ARQUIVO DE TEXTO PARA A VARIAVEL CONTEUDO E COLOCA TUDO PARA MAIUSCULO REMOVENDO ESPAÇOS EXTRAS
    key = chave.upper()                             # COLOCA A CHAVE TUDO EM MAIUSCULO

    resposta_texto_cifrado = cifra_texto_bloco(texto_claro, key)
    #print(f"O Texto cifrado eh:  {resposta_texto_cifrado}")

    with open("TEXTO_CIFRADO.txt", 'w') as arquivo_saida:
        arquivo_saida.write(resposta_texto_cifrado)

    print("Texto cifrado salvo em 'TEXTO_CIFRADO.txt'")
