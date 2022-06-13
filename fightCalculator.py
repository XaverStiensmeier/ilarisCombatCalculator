#!/usr/bin/env python3
import random
import math
import ilarisCharacter as iC
import copy
import ilarisWoundProbability as iWP

oger = iC.IlarisCharacter(name="Oger", ws=12, wss=14, koloss=0, tp=(4,6,6), at=14, vt=14, actions=1)

def get_melee_prowess(from_character, to_character=iC.IlarisCharacter()):
    print(f"{iWP.get_character_damage_output(from_character, to_character)}/{(iWP.get_character_damage_output(to_character, from_character)+1)}")
    return iWP.get_character_damage_output(from_character, to_character)/(iWP.get_character_damage_output(to_character, from_character)+1)

print(get_melee_prowess(oger))