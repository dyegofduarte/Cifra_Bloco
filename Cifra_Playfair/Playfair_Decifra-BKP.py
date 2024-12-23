import re, sys

def ajusta_chave(key):
    # Permite números e letras na chave
    key = key.replace('J', 'I').upper()
    key = ''.join(dict.fromkeys(key + "ABCDEFGHIKLMNOPQRSTUVWXYZ0123456789"))
    return [key[i:i+6] for i in range(0, 36, 6)]  # Retorna uma matriz 6x6

def ajusta_texto(text):
    # Permite números e letras no texto
    return re.sub(r'[^A-Z0-9 ]', '', text.upper())

def acha_posicao(matrix, char):
    for row_idx, row in enumerate(matrix):
        if char in row:
            return row_idx, row.index(char)
    return None

def decifra_par(pair, matrix):
    if ' ' in pair:  # Caso especial para espaço em branco
        return pair  # Retorna o par inalterado se contiver um espaço
    row1, col1 = acha_posicao(matrix, pair[0])
    row2, col2 = acha_posicao(matrix, pair[1])

    if row1 == row2:  # Mesma linha
        return matrix[row1][(col1 - 1) % 6] + matrix[row2][(col2 - 1) % 6]
    elif col1 == col2:  # Mesma coluna
        return matrix[(row1 - 1) % 6][col1] + matrix[(row2 - 1) % 6][col2]
    else:  # Retângulo
        return matrix[row1][col2] + matrix[row2][col1]

def playfair_decrypt(cipher_text, key):
    matrix = ajusta_chave(key)
    prepared_text = ajusta_texto(cipher_text)
    texto_decifrado = ""

    i = 0
    while i < len(prepared_text):
        if prepared_text[i] == ' ':  # Preserva os espaços no texto decifrado
            texto_decifrado += ' '
            i += 1
            continue
        pair = prepared_text[i:i+2]
        if len(pair) == 2:
            texto_decifrado += decifra_par(pair, matrix)
        else:
            texto_decifrado += pair  # Caso reste um único caractere
        i += 2

    return texto_decifrado

#############################################
# FUNÇÃO PARA MOSTRAR MANUAL
def manual():
    print("Formas de uso: python Decifra_Texto.py <Chave> <Arquivo com texto Cifrado>")
    sys.exit(1)
#############################################

def main():
    if len(sys.argv) < 3:
        manual()

    chave = sys.argv[1]
    arquivo_texto = sys.argv[2]
    try:
        with open(arquivo_texto, 'r') as file:
            cipher_text = file.read()
        
        resposta_texto_decifrado = playfair_decrypt(cipher_text, chave)
        
        print("Texto decifrado é: " + resposta_texto_decifrado)
    except FileNotFoundError:
        print("Arquivo de entrada não encontrado.")
        manual()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        manual()

if __name__ == "__main__":
    main()
