#!/usr/bin/env python3
import ilarisWoundProbability as iWP
from roman_arabic_numerals import conv
import yaml

alrik = {
 'kampf': {
  'waffen': [{'AT': 12,
    'RW': 1,
    'TP': {'W': 6, 'anzahl': 3, 'plus': 5},
    'VT': 12,
    'name': 'Angriff'}],
  'werte': {'WSE': 6}},
 'name': 'Alrik',
 'talente': [{'name': 'Zähigkeit', 'wert': 24}]}

def get_fight_data(being_dict):
    kampf_dict = being_dict["kampf"]
    vorteile_list = kampf_dict.get("vorteile")
    attack_counter = 1
    atm = 0
    if vorteile_list:
        for vorteil in vorteile_list:
            if vorteil["name"].startswith("Zusätzliche Attacke"):
                attack_counter+=conv.rom_arab(vorteil["name"][20:])
            elif vorteil in ["Doppelangriff"]:
                attack_counter = attack_counter*2
                atm = -4
    return attack_counter, atm, kampf_dict["waffen"], kampf_dict["werte"]

def get_melee_prowess(from_being_dict, to_being_dict):
    """
    from_being: being that is to be tested.
    to_being: being that is to be tested against.
    return: Estimation how well from_being performs melee wise against to_being (quotient of expected wounds)
    """
    from_attack_counter, from_atm, from_waffen, from_werte = get_fight_data(from_being_dict)
    to_attack_counter, to_atm, to_waffen, to_werte = get_fight_data(to_being_dict)
    melee_prowess_list = []
    for from_waffe in from_waffen:
        for to_waffe in to_waffen:
            from_waffe_damage = sum([iWP.get_being_damage_output(from_waffe, to_waffe, to_werte, from_atm, -3*i)
                for i in range((from_attack_counter))])
            to_waffe_damage = sum([iWP.get_being_damage_output(to_waffe, from_waffe, from_werte, to_atm, -3*i) 
                for i in range((to_attack_counter))])
            melee_prowess = from_waffe_damage/to_waffe_damage
            if melee_prowess<0:
                raise ValueError("Negative")
            else:
                melee_prowess_list.append((melee_prowess, f"From:{from_waffe.get('name')} To:{to_waffe.get('name')}"))
    #print(max(melee_prowess_list))
    return max(melee_prowess_list), from_being_dict["name"]

with open("kreaturen.yml", "r") as stream:
    try:
        creature_dict = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

all_list = []
for creature in creature_dict:
    try:
        all_list.append(get_melee_prowess(creature_dict[creature], alrik))
    except (TypeError, KeyError, ValueError) as e:
        print(creature,e)
all_list.sort()
print(all_list)
