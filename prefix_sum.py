from utilities import *
import substitution
def solve_prefix_sum(ciphertext):
    differences = []
    for i in range(len(ciphertext)-1):
        differences.append(ALPHABET[(INVERSE_ALPHABET[ciphertext[i]]+INVERSE_ALPHABET[ciphertext[i+1]])%26])
    answer = ''.join(differences)
    if IOC(answer)>IOC_CUTOFF:
        return substitution.solve_substitution(answer)
    differences = []
    for i in range(len(ciphertext)-1):
        differences.append(ALPHABET[(INVERSE_ALPHABET[ciphertext[i]]-INVERSE_ALPHABET[ciphertext[i+1]])%26])
    answer = ''.join(differences)
    if IOC(answer)>IOC_CUTOFF:
        return substitution.solve_substitution(answer)
    return None
    