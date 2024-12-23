import sys

#############################################
### FUNÇÕES PARA CIFRAR TEXTO (Cifra de Affine)
def cifra_texto_affine(texto_claro, key):
    # Define o alfabeto estendido com letras, números e espaço
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
    m = len(alfabeto)  # Tamanho do alfabeto

    # Calcula os valores "a" e "b" a partir da chave
    a = sum(ord(char) for char in key) % m  # Usa a soma dos códigos ASCII da chave
    b = len(key) % m  # Usa o comprimento da chave como "b"

    # Garante que "a" seja coprimo a "m" (usando tentativa e erro simples)
    while gcd(a, m) != 1:
        a = (a + 1) % m

    # Mapeia cada caractere do texto claro usando a fórmula da cifra de Afim
    texto_cifrado = ""
    for char in texto_claro:
        if char in alfabeto:
            x = alfabeto.index(char)
            y = (a * x + b) % m
            texto_cifrado += alfabeto[y]
        else:
            texto_cifrado += char  # Mantém caracteres que não estão no alfabeto

    return texto_cifrado

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

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
    arquivo_texto = sys.argv[2]

    with open(arquivo_texto, 'r', encoding='utf-8') as texto:
        texto_claro = texto.read().upper().strip()
    key = chave.upper()

    resposta_texto_cifrado = cifra_texto_affine(texto_claro, key)

    print(f"TEXTO CIFRADO: {resposta_texto_cifrado}")

    with open("TEXTO_CIFRADO.txt", 'w', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(resposta_texto_cifrado)
    print("Texto cifrado salvo em 'TEXTO_CIFRADO.txt'")

