import sys, re

#############################################
### FUNCOES PARA DECIFRAR TEXTO (Cifra de Bacon)

# GERA A TABELA DE CIFRA DE BACON, "I" E "J" SÃO O MESMO CÓDIGO IGUAL A "U" E "V"
def gerar_tabela_bacon():
    alfabeto = "ABCDEFGHIKLMNOPQRSTUWXYZ"  # I/J e U/V são combinados
    tabela = {}
    for i, letra in enumerate(alfabeto):
        binario = f"{i:05b}".replace("0", "A").replace("1", "B")
        tabela[letra] = binario
    #print(f"TABELA DE BACON DECIFRA {tabela}")
    return tabela
    
# DECIFRA 
def decifra_texto_bacon(codigo):
    tabela = gerar_tabela_bacon()
    inverso_tabela = {valor: chave for chave, valor in tabela.items()}
    blocos = [codigo[i:i + 5] for i in range(0, len(codigo), 5)]
    decodificada = "".join(inverso_tabela[bloco] for bloco in blocos if bloco in inverso_tabela)
    return decodificada

#############################################
### FUNCOES PARA DECIFRAR TEXTO (Cifra de Vigenere)

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
def decifra_texto_vigenere(texto_cifrado, palavra_chave):
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
# FUNCAO PARA DECIFRAR TEXTO (Cifra de Alberti)
def decifra_texto_alberti(text, key):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'       # ALFABETO ALFA-NUMERICO PARA SUPORTAR TEXTOS COM LETRA E NUMEROS
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
# USA AS CIFRAS DE BACON, VIGENERE E ALBERTI, NESTA ORDEM

def decifra_texto_bloco(text, key):
    #rodada = 2 

    #for i in range(rodada):
    Decifra_Bacon = decifra_texto_bacon(text)
    #print(f"TEXTO DECIFRADO EM BACON: {Decifra_Bacon} \n")
    Decifra_Vigenere = decifra_texto_vigenere(Decifra_Bacon, key)
    #print(f"TEXTO DECIFRADO EM VIGENERE: {Decifra_Vigenere} \n")
    Decifra_Alberti = decifra_texto_alberti(Decifra_Vigenere, key)
    #print(f"TEXTO DECIFRADO EM ALBERTI: {Decifra_Alberti} \n")
    Decifra_Bloco = Decifra_Alberti
    #text = Decifra_Bloco

    return Decifra_Bloco
    #return Decifra_Bacon

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
        #print(texto_cifrado)
        resposta_texto_decifrado = decifra_texto_bloco(texto_cifrado, key)
        print("O Texto decifrado eh: " + resposta_texto_decifrado)


        with open("TEXTO_DECIFRADO.txt", 'w') as arquivo_saida:
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
