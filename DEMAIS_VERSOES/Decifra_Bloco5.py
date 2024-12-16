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
    return tabela
    
# DECIFRA 
def decifra_texto_bacon(codigo):
    tabela = gerar_tabela_bacon()
    inverso_tabela = {valor: chave for chave, valor in tabela.items()}
    blocos = [codigo[i:i + 5] for i in range(0, len(codigo), 5)]
    decodificada = "".join(inverso_tabela[bloco] for bloco in blocos if bloco in inverso_tabela)
    return decodificada

#############################################
### FUNCOES PARA DECIFRAR TEXTO (Cifra de ADFGVX)

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

def decifra_texto_adfgvx(texto_cifrado, chave):

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
# USA AS CIFRAS DE BACON, ADFGVX E ALBERT, NESTA ORDEM

def decifra_texto_bloco(text, key):
    #rodada = 2 

    #for i in range(rodada):
    Decifra_Bacon = decifra_texto_bacon(text)
    print(f"TEXTO DECIFRADO EM BACON: {Decifra_Bacon} \n")
    print(f"O TIPO DO TEXTO DECIFRADO EM BACON EH: {type(Decifra_Bacon)}\n\n")
    #Decifra_ADFGVX = decifra_texto_adfgvx(text, key)   # TESTE REMOVER DEPOIS 
    #Decifra_ADFGVX = decifra_texto_adfgvx(Decifra_Bacon, key)                   
    #print(f"TEXTO DECIFRADO EM ADFGVX: {Decifra_ADFGVX} \n")
    #print(f"O TIPO DO TEXTO DECIFRADO EM ADFGVX EH: {type(Decifra_ADFGVX)}\n\n")
    #Decifra_Alberti = decifra_texto_alberti(Decifra_ADFGVX, key)
    Decifra_Alberti = decifra_texto_alberti(Decifra_Bacon, key)    # TESTE REMOVER DEPOIS 
    print(f"TEXTO DECIFRADO EM ALBERTI: {Decifra_Alberti} \n")
    print(f"O TIPO DO TEXTO DECIFRADO EM ALBERTI EH: {type(Decifra_Alberti)}\n\n")
    Decifra_Bloco = Decifra_Alberti
    text = Decifra_Bloco

    return Decifra_Bloco

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
        
        print(f"TEXTO CIFRADO: {texto_cifrado}")
        print(f"O TIPO DO TEXTO CIFRADO EH: {type(texto_cifrado)}\n\n")
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
