from utilities import *
def caesar_shift(ciphertext, shift):
    return ''.join(ALPHABET[(INVERSE_ALPHABET[i]+shift)%26] for i in ciphertext)
def solve_caesar(ciphertext):
    for shift in range(26):
        pt = caesar_shift(ciphertext, shift)
        if fitness(pt)>FITNESS_CUTOFF:
            return pt
    return -1

