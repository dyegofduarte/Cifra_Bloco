import string
import sys

def gerar_matriz_adfgvx():
    """
    Gera a matriz de substituição para a cifra ADFGVX.
    """
    alfabeto = string.ascii_uppercase + string.digits
    matriz = {}
    linhas = ['A', 'D', 'F', 'G', 'V', 'X']
    valores = list(alfabeto)
    
    for i, linha in enumerate(linhas):
        for j, coluna in enumerate(linhas):
            if valores:
                matriz[f"{linha}{coluna}"] = valores.pop(0)
    return matriz


def inverter_matriz(matriz):
    """
    Inverte a matriz ADFGVX para que as combinações ADFGVX sejam as chaves
    e os caracteres originais sejam os valores.
    """
    return {v: k for v, k in matriz.items()}


def reverter_transposicao(texto, chave):
    """
    Reverte a transposição baseada na chave.
    """
    chave_ordenada = sorted(list(chave))
    colunas = {letra: [] for letra in chave}
    
    # Determinar o tamanho das colunas
    comprimento = len(texto)
    tamanho_colunas = [comprimento // len(chave)] * len(chave)
    sobra = comprimento % len(chave)
    
    for i in range(sobra):
        tamanho_colunas[chave_ordenada.index(chave[i])] += 1
    
    # Dividir o texto conforme os tamanhos das colunas
    inicio = 0
    for letra in chave_ordenada:
        tamanho = tamanho_colunas.pop(0)
        colunas[letra] = list(texto[inicio:inicio + tamanho])
        inicio += tamanho
    
    # Recriar o texto original
    texto_original = []
    for i in range(len(texto)):
        texto_original.append(colunas[chave[i % len(chave)]].pop(0))
    
    return "".join(texto_original)


def substituir_por_texto(texto, matriz_invertida):
    """
    Substitui combinações ADFGVX pelo texto original.
    Restaurando espaços no processo.
    """
    texto_decifrado = ""
    for i in range(0, len(texto), 2):
        combinacao = texto[i:i+2]
        if combinacao == "..":
            texto_decifrado += " "  # Restaura o espaço
            print(f"ESPAÇO: {texto_cifrado}")
        elif combinacao in matriz_invertida:
            texto_decifrado += matriz_invertida[combinacao]
        else:
            print(f"Combinação não encontrada na matriz: {combinacao}")
            texto_decifrado += "?"  # Ou algum outro caractere para indicar erro
    return texto_decifrado


def decifra(texto_cifrado, chave):
    """
    Realiza a decifragem de um texto cifrado utilizando a cifra de ADFGVX.
    """
    matriz = gerar_matriz_adfgvx()
    matriz_invertida = inverter_matriz(matriz)
    
    # Reverte a transposição com a chave
    texto_transposto = reverter_transposicao(texto_cifrado, chave)
    

    # Substitui as combinações ADFGVX pelo texto original
    texto_decifrado = substituir_por_texto(texto_transposto, matriz_invertida)
    
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

    try: 
        with open(arquivo_texto_cifrado, 'r') as texto:         # ABRE O ARQUIVO
            texto_cifrado = texto.read().upper()                # COPIA O CONTEUDO DO ARQUIVO DE TEXTO PARA A VARIAVEL CONTEUDO E COLOCA TUDO PARA MAIUSCULO
        key = chave.upper()                                     # GARANTE QUE A CHAVE VAI ESTAR EM MAIUSCULO ANTES DE PASSAR PARA AS FUNÇÕES DE DECIFRAGEM
 
        resposta_texto_decifrado = decifra(texto_cifrado, key)  # Chama a função decifra com os argumentos corretos
        print(f"O Texto decifrado é: {resposta_texto_decifrado}")

        with open("TEXTO_DECIFRADO.txt", 'w') as arquivo_saida:
            arquivo_saida.write(resposta_texto_decifrado)

        print("Texto decifrado salvo em 'TEXTO_DECIFRADO.txt'")

    except FileNotFoundError:
        print("Arquivo não encontrado.")
        manual()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        manual()
