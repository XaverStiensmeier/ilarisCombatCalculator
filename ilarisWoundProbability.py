#!/usr/bin/env python3
from re import S
import numpy
import math

def ilarisHitProb(at,vt):
    # 47.5 is the chance without any bonus
    # 47.5-((y-41)*y)/8 is the added chance per bonus
    # (at>vt) is extra if at>vt because equal wins
    y = lambda y: 47.5-((y-41)*y)/8
    return y(at-vt+(at>vt))/100 if at>=vt else 1-y(vt-at+(vt>at))/100

def NdS_equal_k(k,n,s=6):
    """
    int n: number of dice
    int s: sides of dice
    int k: wanted value

    return: Probability to get k when rolling n s-sided dice.
    """
    # see https://en.wikipedia.org/w/index.php?title=Dice&oldid=393538650#Probability
    total_combinations = s**n
    winning_combinations = sum([(-1)**i*math.comb(n,i)*math.comb(k-s*i-1, n-1) for i in range(math.floor((k-n)/s)+1)])
    return winning_combinations/total_combinations

def get_NdS_discrete_TP_distribution(n,s=6):
    """
    int n: number of dice
    int s: sides of dice

    return: List of (k,p) tuples where k is a natural number and p the probability to get said k. Zero values are not listed.
    """
    return [(k, NdS_equal_k(k,n,s)) for k in range(n,n*s+1)]

def get_damage_output(discrete_TP_distribution, tp, ws, koloss=0, btp=0, hit_probability=1):
    """
    discrete_TP_distribution: List of (k,p) tuples where k is a natural number and p the probability to get said k. Zero values are not listed.
    tp: weapon damage + extra damage by strength (KK)
    btp: bonus tp given by maneuvers
    """
    return sum([(TP+tp+btp)*probability/(ws*2**koloss) for TP,probability in discrete_TP_distribution])

def get_character_damage_output(from_character, to_character, btp=0):
    #print(from_character.name)
    n,s,tp = from_character.tp
    at = from_character.at
    vt = to_character.vt
    ws = to_character.wss
    koloss = to_character.koloss
    hit_probability = ilarisHitProb(at,vt)
    #print("hitpro", hit_probability)
    discrete_TP_distribution = get_NdS_discrete_TP_distribution(n,s)
    #print("discrete_tp_distribution")
    #print(discrete_TP_distribution)
    return get_damage_output(discrete_TP_distribution, tp, ws, koloss, btp, hit_probability)