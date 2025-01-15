text = input('What is your text? ')
custom_key = input('What about the key? ')

def vigenere(message, key, direction=1):
    key_index = 0
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    final_message = ''

    for char in message.lower():

        # Append any non-letter character to the message
        if not char.isalpha():
            final_message += char
        else:        
            # Find the right key character to encode/decode
            key_char = key[key_index % len(key)]
            key_index += 1

            # Define the offset and the encrypted/decrypted letter
            offset = alphabet.index(key_char)
            index = alphabet.find(char)
            new_index = (index + offset*direction) % len(alphabet)
            final_message += alphabet[new_index]
    
    return final_message

def encrypt(message, key):
    return vigenere(message, key)
    
def decrypt(message, key):
    return vigenere(message, key, -1)

encryption = encrypt(text, custom_key)
decryption = decrypt(text, custom_key)

option = input('Do you want to encrypt or decrypt your message? E or D: ')

if option == 'E':
    print(f'\nYour encrypted text is: {encryption}')
elif option == 'D':
    print(f'\nYour decrypted text is: {decryption}')
else:
    print('Sorry, your option is wrong')
