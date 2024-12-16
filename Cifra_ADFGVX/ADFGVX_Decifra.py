import sys

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

def decifra_texto(texto_cifrado, chave):

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
 
        resposta_texto_decifrado = decifra_texto(texto_cifrado, key)
        print(f"O Texto decifrado eh:  {resposta_texto_decifrado}")


        with open("TEXTO_DECIFRADO.txt", 'w') as arquivo_saida:
            arquivo_saida.write(resposta_texto_decifrado)

        print("Texto decifrado salvo em 'TEXTO_DECIFRADO.txt'")

    except FileNotFoundError:
        print("ARQUIVO NAO ENCONTRADO")
        #print("TEXTO OU CHAVE ERRADA")
        sys.exit(1)
    except ValueError:
        print("ERRO DE VALOR")
        #print("TEXTO OU CHAVE ERRADA")
        sys.exit(1)
