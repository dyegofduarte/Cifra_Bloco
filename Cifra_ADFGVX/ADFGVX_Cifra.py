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

def cifrar(entrada, chave):
    texto_claro = entrada
  
    substituido = substituir(texto_claro)
    texto_cifrado = transpor(substituido, chave)

    return texto_cifrado

#############################################
# FUNÇÃO PARA MOSTRAR MANUAL
def manual():
    print("Formas de uso: python Cifra_Texto.py <Chave> <Arquivo com texto a Cifrar>")
    sys.exit(1)


#############################################

# FUNÇÃO MAIN
if __name__ == "__main__":
    if len(sys.argv) < 3:
        manual()
    
    chave = sys.argv[1]
    arquivo_texto = sys.argv[2]

    try:
        with open(arquivo_texto, 'r') as file:
            texto_claro = file.read().strip()       # RECEBE TEXTO SEM ESPAÇOS EXTRAS
        
        resposta_texto_cifrado = cifrar(texto_claro, chave)
        
        with open("TEXTO_CIFRADO.txt", 'w') as arquivo_saida:
            arquivo_saida.write(resposta_texto_cifrado)
        
        print("Texto cifrado foi salvo em TEXTO_CIFRADO.txt")
    except FileNotFoundError:
        print("Arquivo de entrada não encontrado.")
        manual()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        manual()



    
