#!/usr/bin/env python

__author__ = 'Shamar D. Brown'
__version__ = '6.0'

import sys
from poke_functions_v6 import (Pkmn, import_poke_input_file, generate_type_combos, generate_combo_dicts, type_counts,
                                 get_combo_difference, get_coverage, join_coverage, print_coverage)

'''
DESCRIPTION:
    In the game of Pokémon, a Pokémon can be one or two of 18 unique types. This is their type combination.
     - There are 306/324 possible type combinations currently in use.
     - Each Pokémon can attack with up to four moves.
     - Each move can be any type in the attackers move pool.
     - When Pokémon attack using a move of the same type, they get a "Same-type attack bonus" or STAB, where (1.5)*DAMAGE is dealt.
     - Attack types can:
         - Be Super-effective (2.0 or 4.0*DAMAGE)
         - Be Resisted or 'Not very-effective' (0.5 or 0.25*DAMAGE)
         - Be an Immunity or Have 'no effect' (0*DAMAGE)
    
    This project suggests 4 types to help users choose moves 
      that will do the most damage to the most type combinations. 
    These moves are known as "coverage."
'''


########################################################################################################################
#                                              C O N S T A N T S                                                       #
########################################################################################################################

# list of all types of pokemon
all_types = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic',
             'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']

# strengths = {pkmn_type: [types that pkmn_type does "super effective damage"(damage*2 or 4) to]}; offensive dictionary
all_strengths = {'normal': [], 'fire': ['grass', 'ice', 'bug', 'steel'], 'water': ['fire', 'ground', 'rock'],
                 'electric': ['water', 'flying'], 'grass': ['water', 'ground', 'rock'],
                 'ice': ['grass', 'ground', 'flying', 'dragon'], 'fighting': ['normal', 'ice', 'rock', 'dark', 'steel'],
                 'poison': ['grass', 'fairy'], 'ground': ['fire', 'electric', 'poison', 'rock', 'steel'],
                 'flying': ['grass', 'fighting', 'bug'], 'psychic': ['fighting', 'poison'],
                 'bug': ['grass', 'psychic', 'dark'], 'rock': ['fire', 'ice', 'flying', 'bug'],
                 'ghost': ['psychic', 'ghost'], 'dragon': ['dragon'], 'dark': ['psychic', 'ghost'],
                 'steel': ['ice', 'rock', 'fairy'], 'fairy': ['fighting', 'dragon', 'dark']}

# weaknesses = {pkmn_type: [types that do "super effective damage"(damage*2 or 4) to pkmn_type]}; defensive dictionary
all_weaknesses = {'normal': ['fighting'], 'fire': ['water', 'rock', 'ground'], 'water': ['electric', 'grass'],
                  'electric': ['ground'], 'grass': ['fire', 'ice', 'poison', 'flying', 'bug'],
                  'ice': ['fire', 'fighting', 'rock', 'steel'], 'fighting': ['flying', 'psychic', 'fairy'],
                  'poison': ['ground', 'psychic'], 'ground': ['water', 'ice', 'grass'],
                  'flying': ['electric', 'ice', 'rock'], 'psychic': ['bug', 'ghost', 'dark'],
                  'bug': ['fire', 'flying', 'rock'], 'rock': ['water', 'grass', 'fighting', 'ground', 'steel'],
                  'ghost': ['ghost', 'dark'], 'dragon': ['ice', 'dragon', 'fairy'],
                  'dark': ['fighting', 'bug', 'fairy'],
                  'steel': ['fire', 'fighting', 'ground'], 'fairy': ['poison', 'steel']}

# resistances = {pkmn_type: [types that do "resisted damage"(damage*0.5 or 0.25) to pkmn_type]}; defensive dictionary
all_resistances = {'normal': [], 'fire': ['fire', 'grass', 'ice', 'bug', 'steel', 'fairy'],
                   'water': ['fire', 'water', 'ice', 'steel'], 'electric': ['electric', 'flying', 'steel'],
                   'grass': ['water', 'electric', 'grass', 'ground'], 'ice': ['ice'],
                   'fighting': ['bug', 'rock', 'dark'],
                   'poison': ['fighting', 'poison', 'bug', 'fairy'], 'ground': ['poison', 'rock'],
                   'flying': ['fighting', 'bug', 'grass'], 'psychic': ['fighting', 'psychic'],
                   'bug': ['fighting', 'ground', 'grass'], 'rock': ['normal', 'fire', 'poison', 'flying'],
                   'ghost': ['poison', 'bug'], 'dragon': ['fire', 'water', 'electric', 'grass'],
                   'dark': ['ghost', 'dark'],
                   'steel': ['normal', 'grass', 'ice', 'psychic', 'flying', 'bug', 'rock', 'dragon', 'steel', 'fairy'],
                   'fairy': ['fighting', 'bug', 'dark']}

# immunities = {pkmn_type: types with an "immunity"(damage*0) to pkmn_type}; defensive dictionary
all_immunities = {'normal': ['ghost'], 'ground': ['electric'], 'flying': ['ground'], 'ghost': ['normal', 'fighting'],
                  'dark': ['psychic'], 'steel': ['poison'], 'fairy': ['dragon']}

# list of static dictionaries
all_swri = [all_strengths, all_weaknesses, all_resistances, all_immunities]

# Unused type combinations (for canon Pokémon)
unused_combos = [['normal', 'ice'], ['normal', 'bug'], ['normal', 'rock'], ['normal', 'steel'], ['fire', 'fairy'],
                 ['ice', 'poison'], ['ground', 'fairy'], ['bug', 'dragon'], ['rock', 'ghost'], ['ice', 'normal'],
                 ['bug', 'normal'], ['rock', 'normal'], ['steel', 'normal'], ['fairy', 'fire'], ['poison', 'ice'],
                 ['fairy', 'ground'], ['dragon', 'bug'], ['ghost', 'rock']]

# initialize count
all_count = 1


########################################################################################################################
#                                                     S E T U P                                                        #
########################################################################################################################


# INTRO
print('\n** Starting Program!\n** Ensure input file is current.\n\n')

# import the input file
pkmn_team = import_poke_input_file(r'poke_input.txt')
print(f'\nT E A M : {pkmn_team}\n')

# Generate a list of all usable type combos
all_combos = generate_type_combos(all_types, unused_combos)

# Generate Dictionaries using Static Dictionaries {type combo: [static dictionary calc]}
all_combo_swri = generate_combo_dicts(all_types, all_combos, all_swri)

# generate type counts; {'atk_type': {'combo count': int(count),
#                                     ('type_combo',): [(type_combos,) that 'atk_type' does damage to]}}
all_type_counts = type_counts(all_types, all_combo_swri)
all_weak_counts, all_resist_counts, all_immune_counts = all_type_counts

# used for tracking combos not covered by your team's stab types
team_nonstab_damage = all_types.copy()


########################################################################################################################
#                                                     START WORK                                                       #
########################################################################################################################

if __name__ == '__main__':

    for pokemon in pkmn_team:

        # create pkmn; print 'this_pkmn' stats
        this_pkmn = Pkmn(all_types, pokemon, all_swri)
        all_count = this_pkmn.print_pkmn(all_count)


        # [these_combos] = change from list of lists to tuples. to compare to dictionary keys
        these_combos = [tuple(combo) for combo in all_combos]

        # [last_bit_of_combos] = [these_combos] - [(type combos that 'this_pkmn' does not (2*damage) to), ]
        last_bit_of_combos = get_combo_difference(this_pkmn.strength, these_combos, all_weak_counts)

        # generate stab coverage data for this_pkmn; [[stab types_header], [stab effectiveness lists]]
        stab_coverage = get_coverage(this_pkmn.types, all_type_counts)


        # generate options for this_pkmn coverage recommendation
        last_bit_of_combo_swri = generate_combo_dicts(all_types, last_bit_of_combos, all_swri)
        last_bit_of_counts = type_counts(all_types, last_bit_of_combo_swri)
        last_bit_of_coverage = get_coverage([t for t in all_types if t not in this_pkmn.types], last_bit_of_counts)


        # concatenate stab coverage data & coverage recommendations
        new_coverage = join_coverage(stab_coverage, last_bit_of_coverage)

        # print 'this_pkmn' coverage table
        print_coverage(new_coverage)

        # track the types that your pokemon team should cover;
        team_nonstab_damage = [t for t in team_nonstab_damage if t not in this_pkmn.types]

# print uncoverable combos as a dictionary
print(f"\n\n\t** {len(team_nonstab_damage)} types don't do stab damage: {team_nonstab_damage} **\n")

########################################################################################################################
#                                                       END WORK                                                       #
########################################################################################################################
