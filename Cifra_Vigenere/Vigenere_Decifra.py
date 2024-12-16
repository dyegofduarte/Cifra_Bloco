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

# Função para decodificar uma mensagem cifrada usando a Cifra de Vigenère
def decifra_texto(texto_cifrado, palavra_chave):
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


    with open(arquivo_texto_cifrado, 'r', encoding='utf-8') as f:
        texto_cifrado = f.read()
    texto_cifrado = processar_texto(texto_cifrado)


    #resposta_texto_decifrado = decifra_texto(arquivo_texto_cifrado, chave)
    #print(f"O Texto decifrado eh: {resposta_texto_decifrado}")


    # Imprime na tela o texto cifrado
    print("Texto Cifrado:\t\t", texto_cifrado)

    # Decodifica o texto cifrado usando a função inversa da Cifra de Vigenère
    texto_decifrado = decifra_texto(texto_cifrado, chave)
    print("Texto Decifrado:\t\t", texto_decifrado)

    # Salva o texto decifrado no arquivo de saída
    with open("TEXTO_DECIFRADO.txt", 'w', encoding='utf-8') as f:
        f.write(texto_decifrado)
    print("Texto decifrado salvo no arquivo TEXTO_DECIFRADO.txt")





    

