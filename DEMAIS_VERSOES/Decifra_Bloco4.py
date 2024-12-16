import sys, re

#############################################
### FUNCOES PARA DECIFRAR TEXTO (Cifra de Vigenere)

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

# Função para decodificar uma mensagem cifrada usando a Cifra de Vigenère
def decifra_texto_vigenere(texto_cifrado, palavra_chave):
    # Inicializa uma variável (como string) para armazenar o texto decifrado
    texto_decifrado = ""
    
    # Expande a palavra-chave para que tenha o mesmo comprimento que o texto cifrado
    palavra_chave_repetida = expandir_palavra_chave(texto_cifrado, palavra_chave)
    
    # Loop que percorre cada caractere do texto cifrado
    for i in range(len(texto_cifrado)):
        # Converte a letra em seu índice ASCII, subtraindo o índice ASCII da palavra-chave para "reverter" a cifra e obter a palavra original
        indice_texto = ord(texto_cifrado[i]) - ord("A")
        indice_palavra_chave = ord(palavra_chave_repetida[i]) - ord("A")
        
        # Decifra o texto cifrado aplicando a subtração e usa o mód 26 (índice entre 0 e 25)
        indice_decifrado = (indice_texto - indice_palavra_chave + 26) % 26
        letra_decifrada = chr(indice_decifrado + ord("A"))
        
        # Adiciona a letra decifrada ao texto decifrado
        texto_decifrado += letra_decifrada
        
    return texto_decifrado


#############################################
### FUNCOES PARA DECIFRAR TEXTO (Cifra de ADFGVX)

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

CHAVE = "EXEMPLO"

def inverter_chave(CHAVE):
    return sorted(range(len(CHAVE)), key=lambda k: CHAVE[k])

def destranspor(texto, CHAVE):
    colunas = len(CHAVE)
    linhas = len(texto) // colunas
    sobra = len(texto) % colunas
    indices = inverter_chave(CHAVE)
    matriz = [''] * colunas

    posicao = 0
    for i, indice in enumerate(indices):
        num_linhas = linhas + 1 if i < sobra else linhas
        matriz[indice] = texto[posicao:posicao + num_linhas]
        posicao += num_linhas

    return ''.join(''.join(linha) for linha in zip(*matriz))

def reverter_substituicao(texto):
    resultado = ""
    i = 0
    while i < len(texto) - 1:
        if texto[i].isspace():
            resultado += " "
            i += 1
        else:
            linha = LETTERS.index(texto[i])
            coluna = LETTERS.index(texto[i + 1])
            resultado += MATRIZ_ADFGVX[linha][coluna]
            i += 2
    return resultado

def decifra_texto_adfgvx(texto_cifrado, chave):

    if not texto_cifrado[-1].isdigit():
        raise ValueError("O texto cifrado não contém um padding válido.")

    padding = int(texto_cifrado[-1])
    texto_cifrado = texto_cifrado[:-1]

    if len(texto_cifrado) % 2 != 0:
        raise ValueError("O texto cifrado não tem um número par de caracteres após remoção do padding.")

    transposto = destranspor(texto_cifrado, chave)

    if padding > 0:
        transposto = transposto[:-padding]

    texto_decifrado = reverter_substituicao(transposto)
    return texto_decifrado

#############################################
### FUNCOES PARA DECIFRAR TEXTO (Cifra de Bacon)

# GERA A TABELA DE CIFRA DE BACON, "I" E "J" SÃO O MESMO CÓDIGO IGUAL A "U" E "V"
def gerar_tabela_bacon():
    alfabeto = "ABCDEFGHIKLMNOPQRSTUWXYZ"  # I/J e U/V são combinados
    tabela = {}
    for i, letra in enumerate(alfabeto):
        binario = f"{i:05b}".replace("0", "A").replace("1", "B")
        tabela[letra] = binario
    return tabela
    
# DECIFRA 
def decifra_texto_bacon(codigo):
    tabela = gerar_tabela_bacon()
    inverso_tabela = {valor: chave for chave, valor in tabela.items()}
    blocos = [codigo[i:i + 5] for i in range(0, len(codigo), 5)]
    decodificada = "".join(inverso_tabela[bloco] for bloco in blocos if bloco in inverso_tabela)
    return decodificada

#############################################
### FUNÇÃO PARA DECIFRAR EM BLOCO
# USA AS CIFRAS DE VIGENERE, ADFGVX E BACON, NESTA ORDEM

def decifra_texto_bloco(text, key):
    #rodada = 2 

    #for i in range(rodada):
    Decifra_Vigenere = decifra_texto_vigenere(text, key)
    print(f"TEXTO DECIFRADO EM VIGENERE: {Decifra_Vigenere} \n")
    Decifra_ADFGVX = decifra_texto_adfgvx(Decifra_Vigenere, key)
    print(f"TEXTO DECIFRADO EM ADFGVX: {Decifra_ADFGVX} \n")
    Decifra_Bacon = decifra_texto_bacon(Decifra_ADFGVX, key)
    print(f"TEXTO DECIFRADO EM BACON: {Decifra_Bacon} \n")
    Decifra_Bloco = Decifra_Bacon
    text = Decifra_Bloco

    return Decifra_Bloco

#############################################
# FUNÇÃO PARA MOSTRAR MANUAL
def manual():
    print("Formas de uso: python decifra_Texto.py <Chave usada para cifrar> <Arquivo com texto a Decifrar>")
    sys.exit(1)


#############################################

# FUNÇÃO MAIN
if __name__ == "__main__":
    if len(sys.argv) < 3:
        manual()
    
    chave = sys.argv[1]
    arquivo_texto_cifrado = sys.argv[2]
    try: 
        with open(arquivo_texto_cifrado, 'r') as texto:         # ABRE O ARQUIVO
            texto_cifrado = texto.read().upper()                # COPIA O CONTEUDO DO ARQUIVO DE TEXTO PARA A VARIAVEL CONTEUDO E COLOCA TUDO PARA MAIUSCULO
        key = chave.upper()                                     # GARANTE QUE A CHAVE VAI ESTAR EM MAIUSCULO ANTES DE PASSAR PARA AS FUNÇÕES DE DECIFRAGEM
        print(texto_cifrado)
        resposta_texto_decifrado = decifra_texto_bloco(texto_cifrado, key)
        print("O Texto decifrado eh: " + resposta_texto_decifrado)


        with open("TEXTO_DECIFRADO.txt", 'w', encoding='utf-8') as arquivo_saida:
            arquivo_saida.write(resposta_texto_decifrado)

        print("Texto decifrado salvo em 'TEXTO_DECIFRADO.txt'")

    except FileNotFoundError:
        print("ARQUIVO NAO ENCONTRADO")
        #print("TEXTO OU CHAVE ERRADA")
        sys.exit(1)
    except ValueError as e:
        print(f"ERRO DE VALOR {e}")
        #print("TEXTO OU CHAVE ERRADA")
        sys.exit(1)
