#!/usr/bin/env python3
import random
import math
import ilarisCharacter as iC
import copy
import ilarisWoundProbability as iWP

oger = iC.IlarisCharacter(name="Oger", ws=12, wss=14, koloss=0, tp=(4,6,6), at=14, vt=14, actions=1)

def get_melee_prowess(from_character, to_character=iC.IlarisCharacter()):
    """
    from_character: Character that is to be tested.
    to_character: Character that is to be tested against.
    return: Estimation how well from_character performs melee wise against to_character (quotient of expected wounds)
    """
    return iWP.get_character_damage_output(from_character, to_character)/(iWP.get_character_damage_output(to_character, from_character)+1)

print(get_melee_prowess(oger))