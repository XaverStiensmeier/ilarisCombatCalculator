#!/usr/bin/env python3
from re import S
import numpy
import math
import pprint

def ilarisHitProb(at,vt):
    """
    at: AT of attacking character
    vt: VT of defending character
    return: probability that attacking character will hit defending character
    """
    # 47.5 is the chance without any bonus
    # 47.5-((y-41)*y)/8 is the added chance per bonus
    # (at>vt) is extra if at>vt because equal wins
    if at-vt>20:
        return 1
    elif vt-at>20:
        return 0
    else:
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

def get_damage_output(discrete_TP_distribution, tp, wse, koloss=0, tpm=0, hit_probability=1):
    """
    discrete_TP_distribution: List of (k,p) tuples where k is a natural number and p the probability to get said k. Zero values are not listed.
    tp: weapon damage + extra damage by strength (KK)
    btp: bonus tp given by maneuvers
    """
    return hit_probability*sum([math.floor((TP+tp+tpm)*probability)/(wse*2**koloss) for TP,probability in discrete_TP_distribution])

def get_being_damage_output(from_waffe, to_waffe, to_werte, from_atm=0, to_vtm=0, tpm=0):
    """
    from_waffe: contains at,vt,tp(n,s,tp)
    to_waffe: contains vt
    to_werte: contains ws, wse and coloss
    from_atm: at modificator
    to_vtm: vt modificator
    tpm: tp modificator
    return: Expected one-turn damage_output from from_being against to_being
    """
    at,vt = from_waffe["AT"] + from_atm, to_waffe["VT"]+to_vtm
    n,s,tp = from_waffe["TP"]["anzahl"], from_waffe["TP"]["W"], from_waffe["TP"]["plus"]+tpm
    wse,koloss = to_werte.get("WSE") or to_werte["WS"], to_werte.get("koloss") or 0
    hit_probability = ilarisHitProb(at,vt)
    discrete_TP_distribution = get_NdS_discrete_TP_distribution(n,s)
    return get_damage_output(discrete_TP_distribution, tp, wse, koloss, tpm, hit_probability)