#!/usr/bin/env python3
import ilarisWoundProbability as iWP
from roman_arabic_numerals import conv
import yaml
import pprint
import traceback

trace = False

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

def indict(thedict, thestring):
    """
    https://stackoverflow.com/questions/55173864/how-to-find-whether-a-string-either-a-key-or-a-value-in-a-dict-or-in-a-dict-of-d
    """
    if thestring in thedict:
        return True
    for val in thedict.values():
        if isinstance(val, dict) and indict(val, thestring):
            return True
        elif isinstance(val, str) and thestring in val:
            return True
    return False


def get_additional_attacks(vorteile_list):
    if vorteile_list:
        additional_attacks = 0
        doppelangriff = False
        for vorteil in vorteile_list:
                if vorteil["name"].startswith("Zusätzliche Attacke"):
                    additional_attacks+=conv.rom_arab(vorteil["name"][20:])
                elif vorteil in ["Doppelangriff"]:
                    doppelangriff = True
        return additional_attacks, doppelangriff
    else:
        return 0,False

def get_fight_data(being_dict):
    kampf_dict = being_dict["kampf"]
    vorteil_list = kampf_dict.get("vorteile")
    additional_attacks, doppelangriff =  get_additional_attacks(vorteil_list)
    attack_counter = additional_attacks+1
    atm = -4*doppelangriff
    return attack_counter,doppelangriff, atm, kampf_dict["waffen"], kampf_dict["werte"]

def get_melee_expected_damage(from_doppelangriff, from_waffe, to_waffe, to_werte, from_atm, from_attack_counter, to_vtm=0, tpm=0):
    weapon_info = from_waffe.get("info")
    additional_attacks = 0
    doppelangriff = False
    if weapon_info: # will become a list CHANGE HERE
        additional_attacks, doppelangriff = get_additional_attacks([{"name":elem} for elem in weapon_info.split(",")])
        doppelangriff = doppelangriff or from_doppelangriff
    final_attack_counter = (from_attack_counter + additional_attacks)*2**doppelangriff
    return  sum([iWP.get_being_damage_output(from_waffe, to_waffe, to_werte, from_atm, to_vtm-3*i, tpm)
        for i in range((final_attack_counter))]), final_attack_counter

def get_melee_prowess(from_being_dict, to_being_dict, maximum=True):
    """
    from_being: being that is to be tested.
    to_being: being that is to be tested against.
    return: Estimation how well from_being performs melee wise against to_being (quotient of expected wounds)
    """
    from_attack_counter, from_doppelangriff, from_atm, from_waffen, from_werte = get_fight_data(from_being_dict)
    to_attack_counter, to_doppelangriff, to_atm, to_waffen, to_werte = get_fight_data(to_being_dict)
    melee_prowess_list = []
    for from_waffe in from_waffen:
        for to_waffe in to_waffen:
            try:
                # If doppelangriff on weapon or advantage double the attack_counter
                for from_ws in range(9):
                    from_waffe_damage, from_final_attack_counter = get_melee_expected_damage(from_doppelangriff, from_waffe, to_waffe, to_werte, from_atm-from_ws, from_attack_counter, tpm=from_ws)
                    to_waffe_damage, to_final_attack_counter = get_melee_expected_damage(to_doppelangriff, to_waffe, from_waffe, from_werte, to_atm, to_attack_counter)
                    melee_prowess = from_waffe_damage/to_waffe_damage
                    if melee_prowess<0:
                        raise ValueError("Negative")
                    else:
                        melee_prowess_list.append((melee_prowess, f"{from_being_dict['name']} From:{from_waffe.get('name')} To:{to_waffe.get('name')} in {from_final_attack_counter} attacks with wuchtschlag {from_ws}"))
            except (TypeError, KeyError, ValueError) as e:
                print(from_being_dict["name"], from_waffe["name"], e)
                if trace:
                    print(traceback.format_exc())
    if maximum:
        return max(melee_prowess_list)
    else:
        melee_prowess_list.sort()
        return melee_prowess_list

def do_all(creature_dict, to_creature=alrik, maximum=True):
    all_list = []
    for creature in creature_dict:
        if True or indict(creature_dict[creature], "-1"):
            try:
                melee_prowess = get_melee_prowess(creature_dict[creature], to_creature, maximum)
                if melee_prowess:
                    all_list.append(melee_prowess)
            except (TypeError, KeyError, ValueError) as e:
                print(creature,e)
    all_list.sort()
    return all_list

def do_single(creature, to_creature=alrik, maximum=True):
    try:
        return get_melee_prowess(creature_dict[creature], creature_dict[to_creature], maximum)
    except (TypeError, KeyError, ValueError) as e:
        print(traceback.format_exc())
        return f"{creature}: {str(e)}"

with open("kreaturen.yml", "r") as stream:
    try:
        creature_dict = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(traceback.format_exc())

pprint.pprint(do_all(creature_dict, creature_dict["soeldner"], maximum=False))
#print(do_single("aaswolf"))