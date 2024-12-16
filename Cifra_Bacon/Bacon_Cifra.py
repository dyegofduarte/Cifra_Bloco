import sys

# GERA A TABELA DE CIFRA DE BACON, "I" E "J" SÃO O MESMO CÓDIGO IGUAL A "U" E "V"
def gerar_tabela_bacon():
    alfabeto = "ABCDEFGHIKLMNOPQRSTUWXYZ"  # I/J e U/V são combinados
    tabela = {}
    for i, letra in enumerate(alfabeto):
        binario = f"{i:05b}".replace("0", "A").replace("1", "B")
        tabela[letra] = binario
    return tabela

# CIFRA 
def cifra_texto_bacon(mensagem):
    tabela = gerar_tabela_bacon()
    mensagem = mensagem.upper().replace("J", "I").replace("V", "U")
    codificada = "".join(tabela[letra] for letra in mensagem if letra in tabela)
    return codificada


#############################################
# FUNÇÃO PARA MOSTRAR MANUAL
def manual():
    print("Formas de uso: python Bacon_Cifra.py <Chave> <Arquivo com texto a Cifrar>")
    sys.exit(1)


#############################################

def main():
    arquivo_texto = sys.argv[1]
    try:
        with open(arquivo_texto, 'r') as file:
            plain_text = file.read()

        resposta_texto_cifrado = cifra_texto_bacon(plain_text)

        with open("TEXTO_CIFRADO.txt", 'w') as arquivo_saida:
            arquivo_saida.write(resposta_texto_cifrado)

        print("Texto cifrado foi salvo em TEXTO_CIFRADO.txt")
    except FileNotFoundError:
        print("Arquivo de entrada não encontrado.")
        manual()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        manual()

if __name__ == "__main__":
    main()

