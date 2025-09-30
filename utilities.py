from collections import Counter, defaultdict
from math import log
#this is a collection of useful functions when dealing with ciphertexts
#no solvers are here, look in the other files!
#contents:
#Section 0 - general functions
#Section 1 - sanitisation
#Section 2 - statistical measures
#Section 3 - n-gram analytic functions

with open("quadgrams.txt",'r') as f:
    quadgram_frequencies = f.read().split('\n')

TOTAL_QUADGRAMS = 4224127912
BASE_FITNESS = -17.780708634424595
quadgram_fitness = defaultdict(lambda:-8)
for quadgram in quadgram_frequencies:
    line = quadgram.split()
    quadgram_fitness[line[0]] = log(int(line[1])/TOTAL_QUADGRAMS)-BASE_FITNESS

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
INVERSE_ALPHABET = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}
MODEL_LETTER_FREQ = {'E': 0.12003601080324099, 'T': 0.09102730819245775, 'A': 0.08122436731019306, 'O': 0.07682304691407423, 'I': 0.0731219365809743, 'N': 0.06952085625687708, 'S': 0.06281884565369612, 'R': 0.06021806541962589, 'H': 0.05921776532959889, 'D': 0.04321296388916676, 'L': 0.03981194358307493, 'U': 0.028808642592777836, 'C': 0.027108132439731925, 'M': 0.026107832349704915, 'F': 0.02300690207062119, 'Y': 0.021106331899569872, 'W': 0.02090627188156447, 'G': 0.020306091827548264, 'P': 0.01820546163849155, 'B': 0.014904471341402423, 'V': 0.011103330999299792, 'K': 0.006902070621186356, 'X': 0.0017005101530459142, 'Q': 0.0011003300990297092, 'J': 0.0010003000900270084, 'Z': 0.0007002100630189059}
#Section 0
def arithmetic_mean(iterable):
    return sum(iterable)/len(iterable)

#Section 1
def cleanup(text):
    '''converts the text to uppercase and removes non-alphabetical characters'''
    text = text.upper()
    text = ''.join(i for i in text if i in ALPHABET)
    return text

#Section 2
KASISKI_CUTOFF = 0.057
IOC_CUTOFF = 0.057
FITNESS_CUTOFF = 6.7
def kasiski(ciphertext, maxlength = 30):
    '''ans[i] = the average IOC of every ith character'''
    answers=[-1]
    for length in range(1,maxlength+1):
        
        answers.append(arithmetic_mean([IOC(ciphertext[j::length]) for j in range(length)]))
    return answers



def kasiski_analysis(ciphertext, maxlength = 30):
    iocs = kasiski(ciphertext, maxlength)
    answers = []
    for i in range(1,maxlength+1):
        if iocs[i]>KASISKI_CUTOFF:
            answers.append(i)
    if not len(answers):
        return answers;
    lowest = answers[0]
    for i in answers:
        if i>lowest and i%lowest and not (iocs[i]>iocs[lowest]+0.005):
            answers.remove(i)
    return answers

def fitness(text):
    '''references an assumed variable quaddict, containing quadgram data'''
    text=text.upper()
    text = ''.join(i for i in text if i in ALPHABET)
    s = 0
    lt = len(text)
    for i in range(lt-4):
        s+=quadgram_fitness[text[i:i+4]]
    return s/(lt-4)

def freq_analysis_similarity_1(text):
    #english frequencies have around -0.001 or higher
    #if it's not english it's probably around -0.01 ot lower
    text = cleanup(text)
    s = 0
    lt = len(text)
    freq = Counter(text)
    fr2 = {i:freq[i]/lt for i in freq}
    for i in ALPHABET:
        s+=((fr2[i] if i in fr2 else 0)-MODEL_LETTER_FREQ[i])**2
    return -s

def freq_analysis_similarity_2(text):
    #checks if the sorted list of frequencies is approximately equal to english
    #similar metrics as the other function
    #english substitution frequencies have around -0.001 or higher
    #if it's not english it's probably around -0.003 or lower
    #this is good for checking if it's a likely substitution or transposition
    text = cleanup(text)
    s = 0
    lt = len(text)
    freq = Counter(text)
    fr2 = {i:freq[i]/lt for i in freq}
    for i in ALPHABET:
        s+=((fr2[i] if i in fr2 else 0)-MODEL_LETTER_FREQ[i])**2
    return -s

def IOC(text):
    '''computes the index of coincidence of a ciphertext of upper case letters'''
    s = 0
    freq = Counter(text) 
    for i in ALPHABET:
        s+=freq[i]**2
    return s/len(text)**2

#Section 3
def bigram_IOC(text,sliding_window=0):
    #the cutoff for bigram substitution type ciphers is ~0.005
    bigrams=[]
    for i in range(0,len(text)-1,(2 if sliding_window==0 else 1)):
        #ERROR
        bigrams.append(text[i:i+2])
    s = 0
    freq = Counter(bigrams) 
    for i in set(bigrams):
        s+=freq[i]**2
    return s/len(bigrams)**2

def bigram_frequencies(text, sliding_window = 0):
    bigrams=[]
    for i in range(0,len(text)-1,(2 if sliding_window==0 else 1)):
        bigrams.append(text[i:i+2])
    s = 0
    freq = Counter(bigrams) 
    return freq

def n_grams_blocks(ciphertext,n):
    lt = len(ciphertext)
    ngrams=[]
    for i in range(0,lt-n+1,n):
        ngrams.append(ciphertext[i:i+n])
    return ngrams
def n_grams_sliding_window(ciphertext,n):
    lt = len(ciphertext)
    ngrams=[]
    for i in range(0,lt-n+1,1):
        ngrams.append(ciphertext[i:i+n])
    return ngrams
    
def n_grams_freqs_blocks(ciphertext,n):
    return Counter(n_grams_blocks(ciphertext,n))

def n_grams_freqs_sliding_window(ciphertext,n):
    lt = len(ciphertext)    
    return Counter(n_grams_sliding_window(ciphertext,n))

def largest_repeating_n_gram(ciphertext):
    lt=len(ciphertext)
    for n in range(1,lt+1):
        ctr = n_grams_freqs_sliding_window(ciphertext,n)
        cmc = ctr.most_common()
        if cmc[0][1]==1:
            break
    n-=1
    ctr = n_grams_freqs_sliding_window(ciphertext,n)
    cmc = ctr.most_common()
    positions = []
    assert(cmc[0][1]>1)
    for i in range(lt-n+1):
        if ciphertext[i:i+n]==cmc[0][0]:
            positions.append(i)
    return (cmc[0][0],n,positions)

