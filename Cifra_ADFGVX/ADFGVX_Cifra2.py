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


def substituir_por_adfgvx(texto, matriz):
    """
    Substitui cada caractere do texto pela correspondente combinação ADFGVX.
    Mantém espaços no texto com um caractere especial.
    """
    texto = texto.upper()
    texto_cifrado = ""
    for caractere in texto:
        if caractere == " ":
            print(f"ESPAÇO: {texto_cifrado}")
            texto_cifrado += ".."  # Substitui o espaço por ".."
            #print(f"ESPAÇO: {texto_cifrado}")
        else:
            for key, value in matriz.items():
                if caractere == value:
                    texto_cifrado += key
                    break
    return texto_cifrado


def transpor(texto, chave):
    """
    Realiza a transposição do texto com base na chave fornecida.
    """
    chave_ordenada = sorted(list(chave))
    colunas = {letra: [] for letra in chave}
    
    for i, caractere in enumerate(texto):
        colunas[chave[i % len(chave)]].append(caractere)
    
    texto_transposto = ""
    for letra in chave_ordenada:
        texto_transposto += "".join(colunas[letra])
    
    return texto_transposto


def cifrar(texto, chave):
    """
    Realiza a cifragem de um texto utilizando a cifra de ADFGVX.
    """
    matriz = gerar_matriz_adfgvx()
    
    # Substitui os caracteres por combinações ADFGVX
    texto_substituido = substituir_por_adfgvx(texto, matriz)
    
    # Realiza a transposição com a chave
    texto_cifrado = transpor(texto_substituido, chave)
    
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

    try:
        with open(arquivo_texto, 'r') as file:
            texto_claro = file.read().strip()       # RECEBE TEXTO SEM ESPAÇOS EXTRAS
        
        resposta_texto_cifrado = cifrar(texto_claro, chave)
        
        with open("TEXTO_CIFRADO.txt", 'w') as arquivo_saida:
            arquivo_saida.write(resposta_texto_cifrado)
        print(f"Texto cifrado eh: {resposta_texto_cifrado}")
        print("Texto cifrado foi salvo em TEXTO_CIFRADO.txt")
    except FileNotFoundError:
        print("Arquivo de entrada não encontrado.")
        manual()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        manual()

