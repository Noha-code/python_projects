# Let's import the tools we need
import random
import math
from sympy import mod_inverse

# Function to check if our number is prime
def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(number / 2) + 1):
        if number % i == 0:
            return False
    return True

# Function to generate a random prime number (for public key)
def random_prime(min, max):
    prime = random.randint(min, max)
    while not is_prime(prime):
        prime = random.randint(min, max)
    return prime

# Function to generate the keys
def make_keys():
    p, q = random_prime(100, 1000), random_prime(100, 1000)

    while p == q:
        q = random_prime(100, 1000)
    
    n = p * q
    phi_of_n = (p-1) * (q-1)

    # The public key with the condition 2 < e < phi(n)
    e = random.randint(3, phi_of_n - 1)
    while math.gcd(e, phi_of_n) != 1:
        e = random.randint(3, phi_of_n - 1)
    
    # The private key, modular inverse of e
    d = mod_inverse(e, phi_of_n)

    return ((e, n), (d, n))

# Function to encrypt the message
def encrypt(public_key, message):
    e, n = public_key
    
    # ord's job is to turn characters into ascii
    ascii_message = [ord(ch) for ch in message]
    cipher = [(ch**e) % n for ch in ascii_message]
    
    # Joining the cipher list into one long string
    return " ".join(map(str, cipher))  

#Function to decrypt the message
def decrypt(private_key, cipher):
    d, n = private_key
    
    # Convert the string of numbers back to a list of integers
    cipher_numbers = list(map(int, cipher.split()))
    ascii_message = [(ch**d) % n for ch in cipher_numbers]  
    
    # chr's job is the opposite of ord (from ascii to letters)
    message = "".join(chr(ch) for ch in ascii_message)  
    return message


# Now, let's put it into practice

# ask for the message
message = input("What do you want to encrypt? ")

# generate the pair of keys
public_key, private_key = make_keys()  

# store and display the encryption
cipher = encrypt(public_key, message)  
print("Encryption done: ", cipher)

# ask if the user wants to decrypt and do as told
continue_response = input("Would you like to decrypt it? y or n: ")
if continue_response.lower() == "y":  
    print("Decryption done: ", decrypt(private_key, cipher))
else:
    print("Okay, Have a good day!!")
