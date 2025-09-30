import numpy as np
from utilities import *
from itertools import permutations, product


#Credit: ChatGPT for some parts the implementation in this file (gcd_extended, mod_inverse, hill_decrypt)
def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y
def mod_inverse(matrix, mod):
    # Calculate the determinant
    det = int(round(np.linalg.det(matrix)))  # Get the determinant
    
    # Find the modular multiplicative inverse of the determinant
    

    gcd, inv_det, _ = gcd_extended(det, mod)
    
    if abs(gcd) != 1:
        raise ValueError("Matrix is not invertible under the given modulus.")
    
    inv_det = inv_det % mod  # Ensure the inverse is positive
    
    # Calculate the adjugate matrix
    adjugate = np.round(np.linalg.inv(matrix)).astype(int) % mod
    
    # Calculate the modular inverse
    inverse_matrix = (adjugate) % mod
    return inverse_matrix
    
def hill_decrypt(ciphertext, hill_matrix):
    # Clean and prepare ciphertext
    cleaned_text = cleanup(ciphertext)

    # Ensure the matrix is square
    n = hill_matrix.shape[0]
    if hill_matrix.shape[0] != hill_matrix.shape[1]:
        raise ValueError("The Hill matrix must be square.")

    # Check if the matrix is invertible
    try:
        inverse_matrix = mod_inverse(hill_matrix, 26)
    except ValueError as e:
        #print(e)
        return None
    #print(hill_matrix)
    #print(inverse_matrix)
    # Convert the cleaned text to numerical values (A=0, B=1, ..., Z=25)
    ciphertext_nums = [ord(char) - ord('A') for char in cleaned_text]
    
    # Ensure ciphertext length is a multiple of n
    while len(ciphertext_nums) % n != 0:
        ciphertext_nums.append(0)  # Padding with 'A' (0)

    # Reshape ciphertext into vectors of size n
    ciphertext_vectors = np.array(ciphertext_nums).reshape(-1, n).T
    # Decrypt the ciphertext
    plaintext_vectors = inverse_matrix @ ciphertext_vectors
    plaintext_vectors = np.mod(plaintext_vectors, 26).astype(int)
    # Flatten the plaintext vectors and convert back to characters
    plaintext_nums = []
    for i in range(len(plaintext_vectors[0])):
        for j in range(len(plaintext_vectors)):
            plaintext_nums.append(plaintext_vectors[j][i])
    plaintext = ''.join(chr(num + ord('A')) for num in plaintext_nums)

    return plaintext


def solve_hill(ciphertext, lite=1):
    '''use lite mode for increased speed'''
    print('Solving Hill Cipher')
    maxima = [-1, -1, 7, 1, 0]
    maxima_2 = [-1, -1, 10, 2, 1]
    if not lite:
        maxima = maxima_2
    for size in range(2,5):
        print(f'Size={size}, maximum entry: {maxima[size]}')
        for matrix in product(list(product(list(range(maxima[size]+1)),repeat=size)),repeat=size):
            mat = np.array(matrix)
            try:
                result = hill_decrypt(ciphertext, mat)
            except ValueError:
                continue
            if not result:
                continue
            if fitness(result)>FITNESS_CUTOFF:
                print('Found!',matrix, mod_inverse(mat,26))
                return result
    return None
  