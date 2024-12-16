import sys, re


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
    # Inicializa a variável (como string) que será usada para a palavra-chave expandida
    palavra_chave_expandida = ""
    # Índice para acompanhar a posição atual na palavra-chave
    indice_palavra_chave = 0
    
    # Loop para repetir a palavra-chave, até que ela tenha o mesmo tamanho do texto
    for _ in range(len(texto)):
        # Adiciona a letra atual da palavra-chave na palavra-chave expandida
        palavra_chave_expandida += palavra_chave[indice_palavra_chave]
        # Incrementa o índice da palavra-chave e reinicia ao início dela, se necessário
        indice_palavra_chave = (indice_palavra_chave + 1) % len(palavra_chave)
        
    return palavra_chave_expandida

# ====================== FUNÇÕES PRINCIPAIS ======================

# Função principal que codifica o texto claro usando a Cifra de Vigenère
def cifra_texto_vigenere(texto_claro, palavra_chave):
    # Inicializa uma variável (como string) para armazenar o texto cifrado
    texto_cifrado = ""
    
    # Expande a palavra-chave até que ela tenha o mesmo comprimento que o texto
    palavra_chave_repetida = expandir_palavra_chave(texto_claro, palavra_chave)
    
    # Loop que percorre cada caractere do texto claro
    for i in range(len(texto_claro)):
        # ord(): função do Python que pega o valor ASCII da letra e subtrai o valor ASCII de "A" para obter um índice entre 0 e 25 (26 letras do alfabeto regular)
        indice_texto = ord(texto_claro[i]) - ord("A")
        indice_palavra_chave = ord(palavra_chave_repetida[i]) - ord("A")
        
        # Cifra o texto aplicando o índice da palavra-chave, e usa o mód 26 (índice entre 0 e 25))
        indice_cifrado = (indice_texto + indice_palavra_chave) % 26
        # chr(): função do Python que converte o índice numérico de volta para uma letra maiúscula
        letra_cifrada = chr(indice_cifrado + ord("A"))
        
        # Adiciona a letra cifrada ao texto cifrado
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
### FUNÇÃO PARA CIFRAR EM BLOCO
# USA AS CIFRAS DE BACON, ADFGVX E VIGENERE, NESTA ORDEM

def cifra_texto_bloco(text, key):
#    rodada = 2 

#    for i in range(rodada):
    Cifra_Bacon = cifra_texto_bacon(text)
    print(f"TEXTO CIFRADO EM BACON: {Cifra_Bacon}")
    Cifra_ADFGVX = cifra_texto_adfgvx(Cifra_Bacon, key)
    print(f"TEXTO CIFRADO EM ADFGVX: {Cifra_ADFGVX}")
    Cifra_Vigenere = cifra_texto_vigenere(Cifra_ADFGVX, key)
    print(f"TEXTO CIFRADO EM VIGENERE: {Cifra_Vigenere} ")
    Cifra_Bloco = Cifra_Vigenere
    text = Cifra_Bloco

    return Cifra_Bloco


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

    with open("TEXTO_CIFRADO.txt", 'w', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(resposta_texto_cifrado)

    print("Texto cifrado salvo em 'TEXTO_CIFRADO.txt'")
