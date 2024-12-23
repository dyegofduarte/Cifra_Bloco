# Formas de Uso:

## Cifrar texto 
`python Cifra_Texto.py <Chave> <Arquivo com texto a Cifrar>`


## Decifrar texto
`python decifra_Texto.py <Chave usada para cifrar> <Arquivo com texto a Decifrar>`


**OBS**: Os arquivos txt podem ser deletados <br>
**OBS**: Necessário somente um arquivo com o texto claro para cifrar <br>
**OBS**: A cifragem e decifragem suporta letras do alfabeto "ABCDEFGHIJKLMNOPQRSTUVWXYZ", números "0123456789" e espaços embranco entre as palavras<br>
**OBS**: Independente de o texto ser minúsculo, a decifragem sempre será maiúscula

### O Script Cifra de Bloco usa as cifras de Alberti, ADFGVX e VIGENERE

### Links para validar a cifragem e decifragem

Alberti
https://www.dcode.fr/alberti-cipher

Playfair 
https://planetcalc.com/7751/

Bacon, Vigenere, ADFGVX
https://cryptii.com/pipes/

<br><br>

# Dentro da pasta do script Cifra de Bloco existem:
- Implementações funcionais separadamente, das 5 cifras usadas e cogitadas para a implementação

- A pasta *DEMAIS_VERSOES* tem tentativas de implementações de Cifras em Bloco que não foram concluídas

<br><br>
# Relatório de entrega

•	Os métodos de cifragem clássicos empregados e como os metodos foram empregados
Usa as cifras de **ALBERT**, **AFFINE** e **VIGENERE**

•	A estrutura da rede de Feistel empregada
Realiza a cifragem e decifragem com 2 rodadas, podendo ajustar a quantidade de rodadas mudando a variável rodada dentro da função cifra_texto_bloco()

•	A estrutura da chave de cifragem / decifragem

•	A cifragem é realiza usando as cifras na seguinte ordem 
**ALBERT**, **AFFINE** e **VIGENERE**

•	A decifragem é realiza usando as cifras na seguinte ordem 
**VIGENERE**, **AFFINE** e **ALBERT**

•	Cada cifra tem seu conjunto de funções separadas, demarcadas por um comentário auto explicativo demonstrado abaixo, de modo que é possível adaptar qualquer outra cifra colando o código dentro do script e chamando sua respectiva função *decifra_texto_bloco()*

#############################################
### FUNÇÃO PARA CIFRAR EM BLOCO
...
<br>
*def decifra_texto_bloco(text, key):*
<br>
....
<br>
#############################################



•	O método de cifra de blocos empregado, o tamanho de bloco usado, modo de operação, uso de padding, etc.

•	Usado blocos de 16 caracteres, especificado na variável *tamanho_bloco*

•	Modo de chamada:
python Cifra_Bloco.py chave TEXTO_CLARO.txt
python Decifra_Bloco.py chave TEXTO_CIFRADO.txt
