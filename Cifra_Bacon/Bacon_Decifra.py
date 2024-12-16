import sys

# GERA A TABELA DE CIFRA DE BACON, "I" E "J" SÃO O MESMO CÓDIGO IGUAL A "U" E "V"
def gerar_tabela_bacon():
    alfabeto = "ABCDEFGHIKLMNOPQRSTUWXYZ"  # I/J e U/V são combinados
    tabela = {}
    for i, letra in enumerate(alfabeto):
        binario = f"{i:05b}".replace("0", "A").replace("1", "B")
        tabela[letra] = binario
    return tabela
    
# DECIFRA 
def bacon_decrypt(codigo):
    tabela = gerar_tabela_bacon()
    inverso_tabela = {valor: chave for chave, valor in tabela.items()}
    blocos = [codigo[i:i + 5] for i in range(0, len(codigo), 5)]
    decodificada = "".join(inverso_tabela[bloco] for bloco in blocos if bloco in inverso_tabela)
    return decodificada


#############################################
# FUNÇÃO PARA MOSTRAR MANUAL
def manual():
    print("Formas de uso: python Bacon_Cifra.py <Chave> <Arquivo com texto a Decifrar>")
    sys.exit(1)


#############################################

def main():
    arquivo_texto = sys.argv[1]
    try:
        with open(arquivo_texto, 'r') as file:
            plain_text = file.read()

        resposta_texto_decifrado = bacon_decrypt(plain_text)
        print(resposta_texto_decifrado)
    except FileNotFoundError:
        print("Arquivo de entrada não encontrado.")
        manual()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        manual()

if __name__ == "__main__":
    main()

