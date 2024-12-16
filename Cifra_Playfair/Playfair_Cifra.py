import re, sys

def ajusta_chave(key):
    key = key.replace('J', 'I').upper()
    key = ''.join(dict.fromkeys(key + "ABCDEFGHIKLMNOPQRSTUVWXYZ"))
    return [key[i:i+5] for i in range(0, 25, 5)]  # Retorna uma matriz 5x5

def ajusta_texto(text):
    text = re.sub(r'[^A-Z ]', '', text.upper()).replace('J', 'I')
    prepared = ""
    i = 0
    while i < len(text):
        if text[i] == ' ':
            prepared += ' '
            i += 1
            continue
        prepared += text[i]
        if i + 1 < len(text) and text[i] == text[i + 1]:
            prepared += 'X'
        elif i + 1 < len(text) and text[i + 1] != ' ':
            prepared += text[i + 1]
            i += 1
        else:
            prepared += 'X'
        i += 1
    return prepared

def acha_posicao(matrix, char):
    for row_idx, row in enumerate(matrix):
        if char in row:
            return row_idx, row.index(char)
    return None

def cifra_par(pair, matrix):
    if ' ' in pair:
        return pair  # Mantém os espaços inalterados
    row1, col1 = acha_posicao(matrix, pair[0])
    row2, col2 = acha_posicao(matrix, pair[1])

    if row1 == row2:  # Mesma linha
        return matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
    elif col1 == col2:  # Mesma coluna
        return matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
    else:  # Retângulo
        return matrix[row1][col2] + matrix[row2][col1]

def cifra_texto_playfair(plain_text, key):
    matrix = ajusta_chave(key)
    texto = ajusta_texto(plain_text)
    
    texto_cifrado = ""
    i = 0
    while i < len(texto):
        if texto[i] == ' ':
            texto_cifrado += ' '
            i += 1
            continue
        if i + 1 < len(texto) and texto[i + 1] != ' ':
            texto_cifrado += cifra_par(texto[i:i+2], matrix)
            i += 2
        else:
            texto_cifrado += cifra_par(texto[i] + 'X', matrix)
            i += 1
    
    # Remove o 'X' final se ele não fizer parte da cifra
    if texto_cifrado[-1] == 'X' and len(texto_cifrado) % 2 != 0:
        texto_cifrado = texto_cifrado[:-1]
    
    return texto_cifrado


#############################################
# FUNÇÃO PARA MOSTRAR MANUAL
def manual():
    print("Formas de uso: python Cifra_Texto.py <Chave> <Arquivo com texto a Cifrar>")
    sys.exit(1)


#############################################

def main():
    chave = sys.argv[1]
    arquivo_texto = sys.argv[2]
    try:
        with open(arquivo_texto, 'r') as file:
            texto_claro = file.read()
        
        resposta_texto_cifrado = cifra_texto_playfair(texto_claro, chave)
        
        with open("TEXTO_CIFRADO.txt", 'w') as arquivo_saida:
            arquivo_saida.write(resposta_texto_cifrado)
        
        print("Texto cifrado foi salvo em TEXTO_CIFRADO.txt")
    except FileNotFoundError:
        print("Arquivo de entrada não encontrado.")
        manual()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        manual()

if __name__ == "__main__":
    main()
