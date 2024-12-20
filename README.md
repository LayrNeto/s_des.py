# Simplified DES Encryption Program

* [Descrição do Projeto](#descrição-do-projeto)
* [Funcionalidades](#funcionalidades)
* [Estrutura do Código](#estrutura-do-código)
  * [Geração de Chaves](#geração-de-chaves)
  * [Permutações](#permutações)
  * [Funções de Expansão e Substituição](#funções-de-expansão-e-substituição)
  * [Função de Rodada](#função-de-rodada)
  * [Criptografia e Descriptografia](#criptografia-e-descriptografia)
  * [Divisão de Bloco Binário](#divisão-de-bloco-binário)
* [Como Utilizar](#como-utilizar)
* [Exemplo de Uso](#exemplo-de-uso)
  * [Criptografar uma Mensagem](#criptografar-uma-mensagem)
  * [Descriptografar uma Mensagem](#descriptografar-uma-mensagem)
* [Conclusão](#conclusão)

## Descrição do Projeto

Este programa implementa um sistema de criptografia e descriptografia utilizando o algoritmo **Simplified DES (S-DES)**, uma versão simplificada do algoritmo **Data Encryption Standard (DES)** criada para fins educacionais. Ele foi projetado para operar com blocos de 8 bits e uma chave principal de 10 bits, fornecendo duas operações principais: criptografar e descriptografar mensagens binárias. O programa utiliza permutações, expansões, e substituições para simular o funcionamento básico do DES. O valor da chave principal é pré-definido, mas permite o teste em diferentes blocos de 8 bits.



## Funcionalidades

1. **Geração de Chaves:**  
   Utiliza permutações e deslocamentos circulares para gerar duas chaves, `K1` e `K2` de 8 bits, derivadas de uma chave principal de 10 bits.

2. **Permutações Iniciais e Finais:**  
   Aplica uma permutação inicial aos blocos de dados antes do processamento e uma permutação final após o processamento.

3. **Função de Expansão e Substituição:**  
   Expande blocos de 4 bits para 8 bits e utiliza tabelas S-box para realizar substituições.

4. **Função de Criptografia e Descriptografia:**  
   Processa os blocos de dados com base em duas rodadas de substituição e permutação, utilizando as chaves geradas.

5. **Interface de Menu:**  
   O programa apresenta um menu interativo para escolher entre criptografar uma mensagem, descriptografar ou encerrar o programa.



## Estrutura do Código

1. **Geração de Chaves**
    ```py
    def permutation10(key):
        return [key[i] for i in [2,4,1,6,3,9,0,8,7,5]]

    def permutation8(key):
    return [key[i] for i in [5,2,6,3,7,4,9,8]]    
    ```
   - Função `permutation10`: Aplica uma permutação de 10 bits à chave principal.

   - Função `permutation8`: Aplica uma permutação de 8 bits à uma chave de 10 bits para gerar as subchaves `K1` e `K2`.

    ```py
    def left_shift1(left_key, right_key):
        left_key = left_key[1:] + left_key[:1]
        right_key = right_key[1:] + right_key[:1]
        return left_key + right_key

    def left_shift2(left_key, right_key):
        left_key = left_key[2:] + left_key[:2]
        right_key = right_key[2:] + right_key[:2]
        return left_key + right_key
    ```
   - Função `left_shift1`: Realiza deslocamento circular à esquerda em 1 bits. 

   - Função`left_shift2`: Realiza deslocamento circular à esquerda em 2 bits.

   
---
2. **Permutações**
    ```py
    def initial_permutation(text):
        return [text[i] for i in [1,5,2,0,3,7,4,6]]

    def final_permutation(text):
        return [text[i] for i in [3,0,2,4,6,1,7,5]]
    ```
   - Função `initial_permutation`: Realiza a permutação inicial nos blocos de dados.

   - Função `final_permutation`: Realiza a permutação final nos blocos após o processamento.

---
3. **Funções de Expansão e Substituição**
    ```py
    def expansion_function(block, key):
        expansion = [block[i] for i in [3,0,1,2,1,2,3,0]]
        return [a^b for a,b in zip(expansion, key)]
    ```
   - Função `expansion_function`: Expande a metade esquerda após a permutação inicial de 4 para 8 bits, e realiza XOR com a subchave.
   
    ```py
    def get_decimal_indexes(left, right):
        left_row = [left[0], left[3]]
        left_row = int("".join(map(str, left_row)), 2)
        left_column = [left[1], left[2]]
        left_column = int("".join(map(str, left_column)), 2)

        right_row = [right[0], right[3]]
        right_row = int("".join(map(str, right_row)), 2)
        right_column = [right[1], right[2]]
        right_column = int("".join(map(str, right_column)), 2)

        return (left_row, left_column), (right_row, right_column) 
    ```
    - Função `get_decimal_indexes`: recebe o bloco expandido separado em esquerda e direita. Concatena e transforma os bits `0` e `3` de cada metade em um valor decimal que será usado como indíce de linha da matriz. Semelhantemente concatena e transforma os bits `1` e `2`, mas estes serão usados como indíce de coluna da matriz. 

    ```py
    def matrix_function(left_indexes, right_indexes):
        s0 = [
            [1, 0, 3, 2],
            [3, 2, 1, 0],
            [0, 2, 1, 3],
            [3, 1, 3, 2],
        ]
        s1 = [
            [0, 1, 2, 3],
            [2, 0, 1, 3],
            [3, 0, 1, 0],
            [2, 1, 0, 3],
        ]

        left_row, left_column = left_indexes
        right_row, right_column = right_indexes
        left_decimals = s0[left_row][left_column]
        right_decimals = s1[right_row][right_column]

        return left_decimals, right_decimals
    ```
    - Função `matrix_function`: pega os índices originários da metade esquerda do bloco expandido para pegar um valor da S-box `s0`, enquanto usa os índices do lado direito para obter um valor da S-box `s1`. 

    ```py
    def decimal_to_bits(left, right):
        left_bits = list(map(int, bin(left)[2:].zfill(2)))
        right_bits = list(map(int, bin(right)[2:].zfill(2)))

        return left_bits + right_bits
    ```
   - Função `decimal_to_bits`: Transforma os valores obtidos das S-boxes em bits de tamanho 2, e concatena-os. 

    ```py
    def permutation4(bits):
        return [bits[i] for i in [1,3,2,0]]
    ```
   - Função `permutation4`: Aplica uma permutação de 4 bits ao bloco após as substituições.

---
4. **Função de Rodada**
    ```py
    def round_function(left, bits):
        return [a^b for a,b in zip(left, bits)]
    ```
   - Função `round_function`: Realiza XOR entre o bloco esquerdo da permutação inicial e o bloco que passou pelas substituições.

---
5. **Criptografia e Descriptografia**
    ```py
    def encryption(block, keys):
        ip = initial_permutation(block)
        key = keys[0]

        for i in range(2):
            print(ip)
            initial_left, initial_right = split_binary_list(ip)
            exp = expansion_function(initial_right, key)
            idx = get_decimal_indexes(*split_binary_list(exp))
            p4 = permutation4(decimal_to_bits(*matrix_function(*idx)))
            left = round_function(initial_left, p4)
            if i == 0:
                ip = switch(left, initial_right)
                print("After switch:", ip)
                key = keys[1]

        cy = left + initial_right
        return final_permutation(cy)
    ```
   - Função `encryption`: Implementa as duas rodadas de algoritmo S-DES. Vale ressaltar que a diferença entre os processos de criptografia e descriptografia é a ordem das subchaves, sendo (k1, k2) para encrypt e (k2, k1) para decrypt. Seu funcionamento se dá pelos seguintes passos:
        
        1. Realiza a permutação inicial, define a subchave como k1 e realiza dois rounds de criptografia:
            ```py
            ip = initial_permutation(block)
            key = keys[0]

            for i in range(2):
            ```
        2. Divide a permutação inicial em direita e esquerda, e aplica a função de expansão no bloco direito:
            ```py
            initial_left, initial_right = split_binary_list(ip)
            exp = expansion_function(initial_right, key)
            ```   
        3. Aplica a função de substituição via S-boxes, e faz uma permutação de 4 bits      
            ```py
            idx = get_decimal_indexes(*split_binary_list(exp))
            p4 = permutation4(decimal_to_bits(*matrix_function(*idx)))
            ```
        4. Realiza a função do round no bloco esquerdo inicial 
            ```py
            left = round_function(initial_left, p4)
            ```    
        5. Se ainda for o primeiro round, troca os blocos esquerda e direita entre si e trata esta troca como equivalente da permutação inicial. Imprime o bloco após o termino do primeiro round e define a subchave como k2:
            ```py
            if i == 0:
                ip = switch(left, initial_right)
                print("After switch:", ip)
                key = keys[1]
            ```  
        6. Concatena os blocos da esquerda e da direita, e retorna os bits criptografados.
            ```py
            cy = left + initial_right
            return final_permutation(cy)
            ```

6. **Divisão de bloco binário**
    ```py
    def split_binary_list(binary):
        mid = len(binary) // 2
        return binary[:mid], binary[mid:] 
    ```
   - Função `split_binary_list`: Divide um bloco binário em direita e esquerda. Essa função foi amplamente utilizada no programa, tanto para geração das subchaves quanto para o algoritmo de criptografia em si.



## Como Utilizar

1. **Preparação do Ambiente:**  
   Certifique-se de ter o Python 3 instalado.

2. **Execução do Programa:**  
   Execute o programa no terminal com o comando:
   ```bash
   python nome_do_arquivo.py
   ```

3. **Navegação no Menu:**  
   - Digite `1` para criptografar uma mensagem.
   - Digite `2` para descriptografar uma mensagem.
   - Digite `3` para encerrar o programa.

---

## Exemplo de Uso

### Criptografar uma Mensagem
Entrada:
```plaintext
==============================================================================================================
Type (1) to encrypt a message.
Type (2) to decrypt a message.
Type (3) to finish the program.
==============================================================================================================
Choose one of the options above: 1
Write a message: [1, 1, 0, 1, 0, 1, 1, 1]
```
Saída:
```plaintext
After switch: [1, 1, 0, 1, 0, 0, 1, 0]
The encrypted message is: [1, 0, 1, 0, 1, 0, 0, 0]
Type Enter to go back to the menu:
```

### Descriptografar uma Mensagem
Entrada:
```plaintext
==============================================================================================================
Type (1) to encrypt a message.
Type (2) to decrypt a message.
Type (3) to finish the program.
==============================================================================================================
Choose one of the options above: 2
Write the encrypted text: [1, 0, 1, 0, 1, 0, 0, 0]
```
Saída:
```plaintext
After switch: [0, 0, 1, 0, 1, 1, 0, 1]
The original message is: [1, 1, 0, 1, 0, 1, 1, 1]
Type Enter to go back to the menu: 
```

## Conclusão
A implementação do algoritmo Simplified Data Encryption Standard (S-DES) neste projeto demonstra de maneira prática e eficiente os conceitos fundamentais da criptografia de bloco. O S-DES, embora simplificado, oferece uma excelente introdução às técnicas de criptografia, incluindo permutações, deslocamentos de bits e operações de S-box. Este projeto não só ajuda a entender o funcionamento interno de algoritmos de criptografia mais complexos, como o DES, mas também serve como uma ferramenta educacional valiosa.

Através da modularização das funções, o programa permite fácil manutenção e extensão, facilitando experimentações e melhorias. A interação com o usuário via terminal torna o sistema acessível e fácil de usar, permitindo criptografar e descriptografar mensagens de forma intuitiva.
