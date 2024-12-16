import os
import sys
from unicodedata import normalize

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
def cifra_texto(texto_claro, palavra_chave):
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

    # Leitura do texto claro a partir do arquivo de entrada
    with open(arquivo_texto, 'r', encoding='utf-8') as f:
        texto_claro = f.read()
    texto_claro = processar_texto(texto_claro)

    # Codifica o texto usando a Cifra de Vigenère
    texto_cifrado = cifra_texto(texto_claro, chave)
    print(f"TEXTO CIFRADO EH: {texto_cifrado}")
    
    # Salva o texto cifrado no arquivo de saída
    with open("TEXTO_CIFRADO.txt", 'w', encoding='utf-8') as f:
        f.write(texto_cifrado)
    print("Texto cifrado salvo no arquivo TEXTO_CIFRADO.txt")
