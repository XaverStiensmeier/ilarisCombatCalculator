#!/usr/bin/env python3
import random
import math
import ilarisCharacter
import copy

def decision(probability):
    return random.random()<probability

def ilarisHitProb(at,vt):
    # 47.5 is the chance without any bonus
    # 47.5-((y-41)*y)/8 is the added chance per bonus
    # (at>vt) is extra if at>vt because equal wins
    y = lambda y: 47.5-((y-41)*y)/8
    return y(at-vt+(at>vt))/100 if at>=vt else 1-y(vt-at+(vt>at))/100

def ilarisOptWS(at,vt, tp):
    mx = 0
    wsmx = 0
    for ws in range(0,8):
        c = ilarisHitProb(at-ws,vt)*(tp+ws)
        if(mx<c):
            mx = c
            wsmx=ws
        else:
            break
    return (mx, wsmx)

def isAttackHitDSA5(at=12,vt=8):
    at=at/20
    vt=vt/201
    GES = at*vt
    #print(f"Hit-Probability:{GES}")
    return decision(GES)

def isAttackHitIlaris(eAT=8,eVT=8):
    rAT = eAT+random.randint(1,20)
    rVT = eVT+random.randint(1,20)
    #print(f"Hit-Probability:{ilarisHitProb(eAT,eVT)}")
    return rAT > rVT or (rAT == rVT and eAT>eVT)

def getDamageDSA5(tp, eRS):
    return max(rollDamage(tp) - eRS, 0) # SP

def getDamageIlaris(tp, eWS):
    return int(math.floor((rollDamage(tp)-1)/eWS))

def rollDamage(tp):
    return sum(random.sample(range(1, tp[1]+1), tp[0]))+tp[2]

def fightTillDeath(a,b):
    a = copy.copy(a)
    b = copy.copy(b)
    first,second = (a,b) if a.ini>b.ini else (b,a) if (a.ini<b.ini) else random.choice((a,b),(b,a))
    counter = 0
    while not (a.isDead() or b.isDead()):
        counter+=1
        #print(f"Round {counter}")
        #print(f"{first.name} ({first.wounds}) attacks {second.name} ({second.wounds})")
        #print(first.at, second.vt)
        if(isAttackHitIlaris(first.at,second.vt)):
            damage = getDamageIlaris(first.tp, second.ws)
            #print(damage)
            second.wounds+=damage
            #print(f"Hit! {damage} wound(s)!")
        else:
            #print("Miss!")
            pass
        if(not second.isDead()):
            #print(f"{second.name} ({second.wounds}) attacks {first.name} ({first.wounds})")          
            if(isAttackHitIlaris(second.at,first.vt)):
                damage = getDamageIlaris(second.tp, first.ws)
                first.wounds+=damage
                #print(f"Hit! {damage} wound(s)!")
            else:
                #print("Miss!")
                pass
    return (b if a.isDead() else a, counter)

def doXFights(a,b,x):
    c = 0
    ac = 0
    bc = 0
    for i in range(x):
        winner, rounds = fightTillDeath(a,b)
        c+=rounds
        if(a.name==winner.name):
            ac+=1
        else:
            bc+=1
    print(f"AVG Rounds: {c/x}")
    print(f"{a.name} won {ac/x} of all fights")
    print(f"{b.name} won {bc/x} of all fights")
    return (ac,bc)



testChar1 = ilarisCharacter.IlarisCharacter()
testChar2 = ilarisCharacter.IlarisCharacter(name="Fast Alrik", ini=4)
testChar3 = ilarisCharacter.IlarisCharacter(name="Slow Alrik", at=8, vt=6, ini=2, tp=(4,6,4))
testChar3 = ilarisCharacter.IlarisCharacter(name="Oger", ws=14, at=14, vt=8, ini=2, tp=(4,6,6))
testChar4 = ilarisCharacter.IlarisCharacter(name="Knight Alrik the 1.", ws=8, at=10, vt=15, ini=6, tp=(2,6,9))
testChar5 = ilarisCharacter.IlarisCharacter(name="Knight Alrik the 2.", ws=8, at=11, vt=15, ini=6, tp=(2,6,8))
