from random import randint, random
from math import e, pi
from utilities import *
def solve_substitution(text, iterations=10000, print_inc = 0):
    '''decrypts a substitution cipher using greedy algorithm'''
    text2=text.upper()
    text2 = ''.join(i for i in text2 if i in ALPHABET)
    table = {i:i for i in ALPHABET} #start from just normal mapping
    T = 5
    fitness0 = fitness(text)
    for i in range(iterations):
        if print_inc and not i%print_inc:
            print(i,fitness0)
        j,k = randint(0,25),randint(0,25)
        if j==k:
            continue
        else:
            text3 = text2.replace(ALPHABET[j],"*")
            text3 = text3.replace(ALPHABET[k],ALPHABET[j])
            text3 = text3.replace("*",ALPHABET[k])
            fitness1 = fitness(text3)
            if fitness1>fitness0:
                table[j] = k
                table[k] = j
                fitness0 = fitness1
                text2 = text3
        T-=(1/iterations-0.01)
    return text2
def solve_substitution_2(text, iterations=30000, print_inc = 0):
    text2=text.upper()
    text2 = ''.join(i for i in text2 if i in ALPHABET)
    table = {i:i for i in ALPHABET} #start from just normal mapping
    T = 0.03
    orig_T = T
    fitness0 = fitness(text)
    for i in range(1, iterations+1):
        if print_inc and not i%print_inc:
            print(i,fitness0)
        j,k = randint(0,25),randint(0,25)
        if j==k:
            continue
        else:
            text3 = text2.replace(ALPHABET[j],"*")
            text3 = text3.replace(ALPHABET[k],ALPHABET[j])
            text3 = text3.replace("*",ALPHABET[k])
            fitness1 = fitness(text3)
            if fitness1>fitness0:
                table[j] = k
                table[k] = j
                fitness0 = fitness1
                text2 = text3
            elif fitness1<=fitness0 and random()<e**((fitness1-fitness0)/T):
                table[j] = k
                table[k] = j
                fitness0 = fitness1
                text2 = text3
        T-=(orig_T/iterations)
    return text2