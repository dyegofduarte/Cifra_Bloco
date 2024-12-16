import sys, re


#############################################
### FUNCOES PARA CIFRAR TEXTO (Cifra de Bacon)

# GERA A TABELA DE CIFRA DE BACON, "I" E "J" SÃO O MESMO CÓDIGO IGUAL A "U" E "V"
def gerar_tabela_bacon():
    alfabeto = "ABCDEFGHIKLMNOPQRSTUWXYZ"  # I/J e U/V são combinados
    tabela = {}
    for i, letra in enumerate(alfabeto):
        binario = f"{i:05b}".replace("0", "A").replace("1", "B")
        tabela[letra] = binario
    #print(f"TABELA DE BACON CIFRA {tabela}")
    return tabela

# CIFRA 
def cifra_texto_bacon(mensagem):
    tabela = gerar_tabela_bacon()
    mensagem = mensagem.upper().replace("J", "I").replace("V", "U")
    codificada = "".join(tabela[letra] for letra in mensagem if letra in tabela)
    return codificada


#############################################
### FUNCOES PARA CIFRAR TEXTO (Cifra de Vigenere)

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
def cifra_texto_vigenere(texto_claro, palavra_chave):
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
### FUNCAO PARA CIFRAR TEXTO (Cifra de Alberti)
def cifra_texto_alberti(text, key):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'           # ALFABETO ALFA-NUMERICO PARA SUPORTAR TEXTOS COM LETRA E NUMEROS
    texto_cifrado = []
    conteudo = text

    chave_expandida = (key * (len(conteudo) // len(key) + 1))[:len(conteudo)]

    for i in range(len(conteudo)):
        if conteudo[i] in alfabeto:
            pos_texto = alfabeto.find(conteudo[i])
            pos_chave = alfabeto.find(chave_expandida[i])
            pos_cifrada = (pos_chave - pos_texto) % len(alfabeto)
            texto_cifrado.append(alfabeto[pos_cifrada])
        else:
            # Se o caractere não estiver no alfabeto, adicioná-lo sem cifragem
            texto_cifrado.append(conteudo[i])


    return ''.join(texto_cifrado)

#############################################
### FUNÇÃO PARA CIFRAR EM BLOCO
# USA AS CIFRAS DE ALBERT, ADFGVX E BACON, NESTA ORDEM

def cifra_texto_bloco(text, key):
#    rodada = 2 

#    for i in range(rodada):
    Cifra_Alberti = cifra_texto_alberti(text, key)
    print(f"TEXTO CIFRADO EM ALBERTI: {Cifra_Alberti}")
    Cifra_Vigenere = cifra_texto_vigenere(Cifra_Alberti, key)
    print(f"TEXTO CIFRADO EM VIGENERE: {Cifra_Vigenere}")
    Cifra_Bacon = cifra_texto_bacon(Cifra_Vigenere)
    print(f"TEXTO CIFRADO EM BACON: {Cifra_Bacon} ")
    Cifra_Bloco = Cifra_Bacon
    #text = Cifra_Bloco

    return Cifra_Bloco
    #return Cifra_Bacon

#############################################
### FUNÇÃO PARA MOSTRAR MANUAL
def manual():
    print("Formas de uso: python Cifra_Texto.py <Chave> <Arquivo com texto a Cifrar>")
    sys.exit(1)


#############################################
### FUNÇÃO MAIN
if __name__ == "__main__":
    if len(sys.argv) < 3:
        manual()
    
    chave = sys.argv[1]
    arquivo_texto = sys.argv[2]

    with open(arquivo_texto, 'r') as texto:         # ABRE O ARQUIVO
        texto_claro = texto.read().upper().strip()         # COPIA O CONTEUDO DO ARQUIVO DE TEXTO PARA A VARIAVEL CONTEUDO E COLOCA TUDO PARA MAIUSCULO REMOVENDO ESPAÇOS EXTRAS
    key = chave.upper()                             # COLOCA A CHAVE TUDO EM MAIUSCULO

    resposta_texto_cifrado = cifra_texto_bloco(texto_claro, key)
    #print(f"O Texto cifrado eh:  {resposta_texto_cifrado}")

    with open("TEXTO_CIFRADO.txt", 'w') as arquivo_saida:
        arquivo_saida.write(resposta_texto_cifrado)

    print("Texto cifrado salvo em 'TEXTO_CIFRADO.txt'")
