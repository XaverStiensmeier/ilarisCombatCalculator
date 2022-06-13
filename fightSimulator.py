#!/usr/bin/env python3
import random
import math
import ilarisCharacter
import copy

def isAttackHitIlaris(eAT=8,eVT=8):
    rAT = eAT+random.randint(1,20)
    rVT = eVT+random.randint(1,20)
    #print(f"Hit-Probability:{ilarisHitProb(eAT,eVT)}")
    return rAT > rVT or (rAT == rVT and eAT>eVT)

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
