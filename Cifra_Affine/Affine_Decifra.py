import sys


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



#############################
# FUNÇÃO MANUAL
def manual():
    print("""
Uso: python script.py <chave> <arquivo_texto>

- <chave>: String que será usada como chave para a cifra.
- <arquivo_texto>: Caminho do arquivo contendo o texto a ser cifrado.
    """)
    sys.exit(1)

############################
# FUNÇÃO PRINCIPAL    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        manual()
    chave = sys.argv[1]
    arquivo_texto_cifrado = sys.argv[2]

    with open(arquivo_texto_cifrado, 'r', encoding='utf-8') as texto:
        texto_cifrado = texto.read().upper().strip()
    key = chave.upper()

    resposta_texto_decifrado = decifra_texto_affine(texto_cifrado, key)

    print(f"TEXTO DECIFRADO: {resposta_texto_decifrado}")

    with open("TEXTO_DECIFRADO.txt", 'w', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(resposta_texto_decifrado)
    print("Texto decifrado salvo em 'TEXTO_DECIFRADO.txt'")

