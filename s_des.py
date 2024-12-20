def permutation10(key):
    return [key[i] for i in [2,4,1,6,3,9,0,8,7,5]]

def split_binary_list(binary):
    mid = len(binary) // 2
    return binary[:mid], binary[mid:] 

def left_shift1(left_key, right_key):
    left_key = left_key[1:] + left_key[:1]
    right_key = right_key[1:] + right_key[:1]
    return left_key + right_key

def permutation8(key):
    return [key[i] for i in [5,2,6,3,7,4,9,8]]

def left_shift2(left_key, right_key):
    left_key = left_key[2:] + left_key[:2]
    right_key = right_key[2:] + right_key[:2]
    return left_key + right_key
#===================================================================    
def initial_permutation(text):
    return [text[i] for i in [1,5,2,0,3,7,4,6]]

def final_permutation(text):
    return [text[i] for i in [3,0,2,4,6,1,7,5]]
#===================================================================
def expansion_function(block, key):
    expansion = [block[i] for i in [3,0,1,2,1,2,3,0]]
    return [a^b for a,b in zip(expansion, key)]

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

def decimal_to_bits(left, right):
    left_bits = list(map(int, bin(left)[2:].zfill(2)))
    right_bits = list(map(int, bin(right)[2:].zfill(2)))

    return left_bits + right_bits

def permutation4(bits):
    return [bits[i] for i in [1,3,2,0]]

def round_function(left, bits):
    return [a^b for a,b in zip(left, bits)]

def switch(left, right):
    return right + left


def key_generator(main_key):
    p10 = permutation10(main_key)
    ls1 = left_shift1(*split_binary_list(p10))
    k1 = permutation8(ls1)
    ls2 = left_shift2(*split_binary_list(ls1))
    k2 = permutation8(ls2)

    return (k1, k2)

def encryption(block, keys):
    ip = initial_permutation(block)
    key = keys[0]

    for i in range(2):
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

def main():
    key = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
    data_block = [1, 1, 0, 1, 0, 1, 1, 1]    
    k1, k2 = key_generator(key)

    while True:
        print("==============================================================================================================")
        print("Type (1) to encrypt a message.")
        print("Type (2) to decrypt a message.")
        print("Type (3) to finish the program.")
        print("==============================================================================================================")
        option = int(input("Choose one of the options above: "))
        
        match option:
            # Criptografar mensagem.
            case 1:
                input_data = input("Write a message: ")
                print("==============================================================================================================")
                input_data = input_data.replace('[', '').replace(']', '').split(',')
                message = [int(i) for i in input_data]
                ciphertext = encryption(message, (k1, k2))
                print(f"The encrypted message is: {ciphertext}")
                input("Type Enter to go back to the menu: ")
            
            # Descriptograr mensagem.
            case 2:
                input_data = input("Write the encrypted text: ")
                print("==============================================================================================================")
                input_data = input_data.replace('[', '').replace(']', '').split(',')
                ciphertext = [int(i) for i in input_data]
                plaintext = encryption(ciphertext, (k2, k1))
                print(f"The original message is: {plaintext}")
                input("Type Enter to go back to the menu: ")
            
            # Encerrar programa.
            case 3:
                print("==============================================================================================================")
                print("The program has ended")
                break

            # Caso de resposta inválida.    
            case _:
                print("==============================================================================================================")
                print("You have to choose between (1), (2), or (3). Try again!")
                input("Type Enter to go back to the menu: ")

main()