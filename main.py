from utilities import *
import substitution
import vigenere
import prefix_sum
import transposition
import hill
from itertools import permutations
from time import perf_counter as time
from sympy import factorint
start_time = time()


def try_transposition(ciphertext, cribs):
    result = transposition.solve_transposition(ciphertext)
    if result!=None:
        return result

    print('High IOC, high frequency similarity but could not solve as a transposition cipher. This means the solver is unlikely to work. Solve manually. However it will keep trying other ciphers, though a solution is unlikely.')

    

def try_substitution(ciphertext, cribs):
    for attempt in range(1,4):
        if attempt!=3:
            result = substitution.solve_substitution(ciphertext, iterations=attempt*10000, print_inc = 1000)
        else:
            result = substitution.solve_substitution_2(ciphertext, iterations=30000, print_inc = 1000)
        fit=(fitness(result) if result else -100)
        if fit>FITNESS_CUTOFF:
            return result
        else:
            print('Failed to solve substitution cipher, fitness',fit)
            print(result[:100]+'...')
            print(f'Retrying (attempt {attempt+1} of 3)')
    print('High IOC, low frequency similarity but could not solve as a substitution cipher. This means the solver is unlikely to work. Solve manually. However it will keep trying other ciphers, though a solution is unlikely.')
    return None

def analyse(ciphertext, cribs=[]):
    orig_text = ciphertext
    ciphertext = cleanup(ciphertext)
    ioc = IOC(ciphertext)
    freqs = Counter(ciphertext)
    n = len(ciphertext)
    print('Length of ciphertext:',n, ', factors',factorint(n))
    print('Frequency Analysis:')
    print(freqs.most_common())
    if n==0:
        pass
        #likely some number cipher
        #implement the 2 standard number ciphers and then analyse
        #along with nihilist
    elif n==5:
        pass
        #likely adfgx type, either without transposition or with
        #implement the 2 standard types like the number ciphers then analyse


    print('Index of coincidence:',ioc)
    if ioc>IOC_CUTOFF:
        print('High index of coincidence, so this is likely to be a substitution or transposition type cipher')
        #this section deals with:
        #substitution, various transposition, rail fence, caesar box, scytale
        #now we need to check if the frequencies are english like
        fsim_1 = freq_analysis_similarity_1(ciphertext)
        print('English frequency similarity score is',fsim_1)
        if fsim_1>-0.004:
            print('This is a high similarity score. Therefore, we will attempt to solve a transposition cipher.')
            result = try_transposition(ciphertext, cribs)
            fit = (fitness(result) if result else -100)
            if fit>FITNESS_CUTOFF:
                return result
            print('It\'s not even a low similarity score but we might as well try substitution now')
            result = try_substitution(ciphertext, cribs)
            fit = (fitness(result) if result else -100)
            if fit>FITNESS_CUTOFF:
                return result
        else:
            print('This is a low similarity score. Therefore, we will attempt to solve a substitution cipher.')
            result = try_substitution(ciphertext, cribs)
            fit = (fitness(result) if result else -100)
            if fit>FITNESS_CUTOFF:
                return result
            print('It\'s not even a high similarity score but we might as well try transposition now')
            result = try_transposition(ciphertext, cribs)
            fit = (fitness(result) if result else -100)
            if fit>FITNESS_CUTOFF:
                return result
    print('Let\'s now check if it might be a Vigenere')
    print('Kasiski analysis results:')
    kar = kasiski(ciphertext)
    ka = kasiski_analysis(ciphertext)
    for i in range(1,21):
        print(i,kar[i])
    print('Likely key lengths:',ka)
    if len(ka):
        print('Trying vigenere cipher')
        result = vigenere.solve_vigenere(ciphertext, silent=0)
        fit = (fitness(result) if result else -100)
        if fit>FITNESS_CUTOFF:
            return result
        print('Vigenere failed, fitness=',fit,sep='')
        print('Let\'s try a variant of the vigenere, the Beaufort cipher')
        result = vigenere.solve_beaufort(ciphertext, silent=0)
        fit = (fitness(result) if result else -100)
        if fit>FITNESS_CUTOFF:
            return result
        print('Beaufort failed, fitness=',fit,sep='')
        print(f'At this point it is likely to be some sort of vigenere + substitution or {ka[0]} different substitution alphabets or something')
    print('Let\'s try the prefix sum cipher')
    result = prefix_sum.solve_prefix_sum(ciphertext)
    if result!=None:
        fit=fitness(result)
        if fit>FITNESS_CUTOFF:
            print('Worked!')
            return result
    print('Let\'s try the Hill cipher')
    result = hill.solve_hill(ciphertext)
    if result:
        return result

    print('The cipher solver failed to find a solution. Please solve manually.')
    
    
    

if __name__=='__main__':
    with open("input.txt","r") as f:   
        ciphertext = f.read()
    result = analyse(ciphertext)
    if result==None:
        print('Solver failed, you will have to do it manually')
    else:
        print(result[:200]+'...')
        print("Fitness:",fitness(result))
        with open("result.txt","w") as f:
            f.write(result+'\n')
    print('Time taken:',time()-start_time)



