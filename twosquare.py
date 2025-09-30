from utilities import *
from random import *
#solvers are very hit or miss
#horizontal version
alph2='ABCDEFGHIKLMNOPQRSTUVWXYZ'
def solve_twosquare_version_1(ciphertext):
    def get_bigram(bg,square1,square2):
        x,y=square1.index(bg[0]),square2.index(bg[1])
        return square1[x//5*5+y%5]+square2[y//5*5+x%5]
    square1=list(alph2[:])
    square2=list(alph2[:])
    shuffle(square1)
    shuffle(square2)
    def decrypt_foursquare(square1, square2):
        return ''.join(get_bigram(i,square1,square2) for i in n_grams_blocks(ciphertext,2))
    def set_bigram(bg1,bg2):
        global square1
        global square2
        w,x,y,z=alph2.index(bg1[0]),alph2.index(bg1[1]),alph2.index(bg2[0]),alph2.index(bg2[1])
        pos1=y//5*5+z%5
        pos2=z//5*5+y%5
        #print(pos1,pos2)
        o1,o2=square1.index(bg1[0]),square2.index(bg1[1])
        square1[pos1],square1[o1]=bg1[0],square1[pos1]
        square2[pos2],square2[o2]=bg1[1],square2[pos2]
        #print(pos1,pos2,o1,o2)
    KF = 0.05
    def kitness(square):
        t1 = sum(KF for i in range(len(square)-1) if square[i]<square[i+1])
        t2 = sum(KF for i in range(len(square)-1) if alph2.index(square[i])==(alph2.index(square[i+1])-1)%26)
        return t1*0.5+t2
    #crib = 'AMYTHSEEMSTOHAVEARISENCONCERNINGTURINGSPAPEROFNAMELYTHATHETHEREGAVEATREAT'
    #cribs={}
    #for i in range(0,len(crib)-1,2):
    #    set_bigram(ciphertext[i:i+2],crib[i:i+2])
    print(square1,square2)
    stuck = 0
    pt=decrypt_foursquare(square1,square2)
    for iteration in range(1000000):
        fi=fitness(pt)+kitness(square1)+kitness(square2)
        if fi>6.5+KF*26 and iteration%1000==0:
            print(iteration,"CODE_998244353",fi,pt)
        assert(len(set(square1))==25)
        assert(len(set(square2))==25)
        a,b=randint(0,24),randint(0,24)
        if a==b:
            continue
        if iteration%2==0:
            square1[a],square1[b]=square1[b],square1[a]
        elif iteration%2==1:
            square2[a],square2[b]=square2[b],square2[a]
        newp=decrypt_foursquare(square1,square2)
        newf=fitness(newp)+kitness(square1)+kitness(square2)
        stuck += 1
        if not iteration%100:
            print("INCREMENT",iteration,fi)
        if newf>fi:
            print("IMPROVEMENT",fi,newf)
            stuck = 0
            pt=newp
        else:
            if iteration%2==0:
                square1[a],square1[b]=square1[b],square1[a]
            elif iteration%2==1:
                square2[a],square2[b]=square2[b],square2[a]
        if stuck>1400:
            print('Random Restart',iteration)
            shuffle(square1)
            shuffle(square2)
            pt = decrypt_foursquare(square1,square2)
            stuck=0