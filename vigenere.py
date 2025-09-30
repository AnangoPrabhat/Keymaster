from utilities import *
from caesar import *
def find_keys(text, maxlength=30):
    text = cleanup(text)
    kl = kasiski_analysis(text,maxlength=maxlength)
    l = []
    for key_length in kl:
        s=''
        for i in range(key_length):
            similarities = {}
            for letter in range(26):
                similarities[letter] = freq_analysis_similarity_2(caesar_shift(text[i::key_length], 26-letter))
            s+=ALPHABET[max(similarities, key=similarities.get)]
            #print(similarities)
                #make a caesar shift and check for spiral similarity
        l.append(s)
    return l

def vigenere_key(text, key, offset=0):
    text = cleanup(text)
    t = ''
    key = cleanup(key)
    lenkey=len(key)
    for i,e in enumerate(text):
        t+=ALPHABET[(INVERSE_ALPHABET[e]-INVERSE_ALPHABET[key[(i+offset)%lenkey]])%26]
    return t

def solve_vigenere(ciphertext, maxlength=30, silent=0):
    for i in find_keys(ciphertext, maxlength=maxlength):
        pt = vigenere_key(ciphertext, i)
        fit=fitness(pt)
        if not silent:
            print('Trying key:',i)
        if fit>FITNESS_CUTOFF:
            if not silent:
                print('Key Worked:',i)
                print('Fitness:',fit)
            return pt
        if not silent:
            print('Key Failed:',i)
            print('Fitness:',fit)
    return None

def solve_beaufort(ciphertext, maxlength=30,silent=0):
    ciphertext = ciphertext.translate({i:155-i for i in range(65,91)})
    return solve_vigenere(ciphertext, maxlength=maxlength, silent=0)