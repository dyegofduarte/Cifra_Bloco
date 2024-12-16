import sys, re
from unicodedata import normalize

#############################################
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

# Função para decodificar uma mensagem cifrada usando a Cifra de Vigenère
def decifra_texto_vigenere(texto_cifrado, palavra_chave):
    texto_decifrado = ""
    palavra_chave_repetida = expandir_palavra_chave(texto_cifrado, palavra_chave)
    
    for i in range(len(texto_cifrado)):
        char_texto = texto_cifrado[i]
        char_chave = palavra_chave_repetida[i]
        
        if char_texto.isalpha():
            indice_texto = ord(char_texto) - ord('A')
            indice_chave = ord(char_chave) - ord('A')
            indice_decifrado = (indice_texto - indice_chave + 26) % 26
            letra_decifrada = chr(indice_decifrado + ord('A'))
        elif char_texto.isdigit():
            indice_texto = ord(char_texto) - ord('0')
            indice_chave = ord(char_chave) - ord('0')
            indice_decifrado = (indice_texto - indice_chave + 10) % 10
            letra_decifrada = chr(indice_decifrado + ord('0'))
        else:
            letra_decifrada = char_texto
        
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
# FUNCAO PARA DECIFRAR TEXTO (Cifra de Alberti)
def decifra_texto_alberti(text, key):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'       # ALFABETO ALFA-NUMERICO PARA SUPORTAR TEXTOS COM LETRA E NUMEROS
    #alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'       # ALFABETO ALFA-NUMERICO PARA SUPORTAR TEXTOS COM LETRA E NUMEROS
    texto_decifrado = []
    conteudo_cifrado = text

    chave_expandida = (key * (len(conteudo_cifrado) // len(key) + 1))[:len(conteudo_cifrado)]
    
    for i in range(len(conteudo_cifrado)):
        if conteudo_cifrado[i] in alfabeto:
            pos_cifrada = alfabeto.index(conteudo_cifrado[i])
            pos_chave = alfabeto.index(chave_expandida[i])
            pos_decifrada = (pos_chave - pos_cifrada) % len(alfabeto)
            texto_decifrado.append(alfabeto[pos_decifrada])
        else:
            # Adiciona caracteres não alfabéticos sem decifragem
            texto_decifrado.append(conteudo_cifrado[i])

    return ''.join(texto_decifrado)

#############################################
### FUNÇÃO PARA DECIFRAR EM BLOCO
# USA AS CIFRAS DE VIGENERE, ADFGVX E ALBERT, NESTA ORDEM
# AMBAS CIFRAS DEVEM SUPORTAR OS MESMO TIPOS DE CARACTERES TANTO NA CIFRAGEM QUANTO NA DECIFRAGEM, AS USADAS AQUI SUPORTAM AS LETRAS DO ALFABETO E NÚMEROS DE 0 A 9, E ESPAÇOS EM BRANCO

def decifra_texto_bloco(text, key):
    #rodada = 2 
    
    #for i in range(rodada):
    Decifra_Vigenere = decifra_texto_vigenere(text, key)
    print(f"TEXTO DECIFRADO EM VIGENERE: {Decifra_Vigenere}")
    
    Decifra_ADFGVX = decifra_texto_adfgvx(Decifra_Vigenere, key)
    print(f"TEXTO DECIFRADO EM ADFGVX: {Decifra_ADFGVX}")
    
    Decifra_Alberti = decifra_texto_alberti(Decifra_ADFGVX, key)
    print(f"TEXTO DECIFRADO EM ALBERTI: {Decifra_Alberti}")
    
    Decifra_Bloco = Decifra_Alberti
    #text = Decifra_Bloco

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

        resposta_texto_decifrado = decifra_texto_bloco(texto_cifrado, key)
        print("O Texto decifrado eh: " + resposta_texto_decifrado)


        with open("TEXTO_DECIFRADO.txt", 'w', encoding='utf-8') as arquivo_saida:
            arquivo_saida.write(resposta_texto_decifrado)

        print("Texto decifrado salvo em 'TEXTO_DECIFRADO.txt'")

    except FileNotFoundError as e:
        print(f"ARQUIVO NAO ENCONTRADO {e}")
        #print("TEXTO OU CHAVE ERRADA")
        sys.exit(1)
    except ValueError as e:
        print(f"ERRO DE VALOR {e}")
        #print("TEXTO OU CHAVE ERRADA")
        sys.exit(1)
