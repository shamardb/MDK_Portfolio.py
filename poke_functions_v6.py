#!/usr/bin/env python

__author__ = 'Shamar D. Brown'
__version__ = '6.0'

import sys

'''
DESCRIPTION:
    - functions for "poke_coverage" script

FUNCTIONS:
from poke_functions_v6 import (Pkmn, import_poke_input_file, generate_type_combos, generate_pkmn_stats,
                                 generate_combo_dicts, combo_print, type_counts, coverage_calcs, get_combo_difference,
                                 get_coverage, join_coverage, print_coverage)
'''


########################################################################################################################
#                                                      CLASSES                                                         #
########################################################################################################################


# Create the Pkmn object
class Pkmn:

    # initialize pkmn attributes
    def __init__(self, all_types, pkmn_types, all_swri):

        """ :param  all_types:  ['all pkmn types', ]
            :param pkmn_types:  ['self.pkmn's types', ]
            :param   all_swri:  [all_strengths, all_weaknesses, all_resistances, all_immunities]"""

        self.types = pkmn_types
        self.strength, self.weakness, self.resisted, self.immune = (
            generate_pkmn_stats(all_types, self.types, all_swri))
        self.uncovered = sorted([t for t in all_types if t not in self.strength], key=lambda t: all_types.index(t))

    # print 'pkmn' attributes
    def print_pkmn(self, count):

        """ :param count:  used label team members"""

        # setup name
        name = f'{self.types[0]} {self.types[1]}' if self.types[1] else f'{self.types[0]}'
        name = f' P K M N {count} :  {name} '
        dash = '-' * len(name)

        # Print pkmn data
        print(f'\n{dash}\n{name}\t\n{dash}')
        print(f'\tstrengths:\t\t\t{len(self.strength)}\t| {self.strength}')
        print(f'\tuncovered:\t\t\t{len(self.uncovered)}\t| {self.uncovered}')
        print(f'\tweaknesses:\t\t\t{len(self.weakness)}\t| {self.weakness}')
        print(f'\tresistances:\t\t{len(self.resisted)}\t| {self.resisted}')
        print(f'\timmunities:\t\t\t{len(self.immune)}\t| {self.immune}\n')

        return count + 1


########################################################################################################################
#                                                    FUNCTIONS                                                         #
########################################################################################################################

# read lines from txt file into a [list]
def import_poke_input_file(filename):

    """ :param filename:  'path_to_input_file' """

    txt_file_data = []
    try:
        txt_file = open(filename, 'r', encoding='utf-8-sig')
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        sys.exit(0)
    else:
        for line in txt_file:
            if line.startswith('-'):
                break
            else:
                data = line.rstrip('\n')
                data = data.split() if len(data) > 8 else [data.strip(), None]
                txt_file_data.append(data)
        txt_file.close()

    return txt_file_data


# Generate a list of all usable type combos
def generate_type_combos(types, unused_combos):

    """ :param         types:  ['attacking pkmn's types', ]
        :param unused_combos:  [(type combos not used by legitimate Pokémon), ]"""

    # generate list of all possible type combinations
    all_combos = [[type1, type2] if type2 else [type1, ] for type1 in types for type2 in types]

    # Modify tuples with duplicate entries [i.e. ('fairy', 'fairy') to ('fairy', None)]
    unique_combos = [[t[0], None] if t[0] == t[1] else t for t in all_combos]

    # Remove type combos unused on real pkmn
    type_combos = [t for t in unique_combos if t not in unused_combos]
    # [print(f"{count + 1}: {combo}") for count, combo in enumerate(type_combos)]

    return type_combos


# Generate a list of types that are "type_dict" against 'pkmn'; type_dict = strengths, weakness, etc...
def generate_type_list(pkmn_types, type_dict):

    """ :param pkmn_types:  ['attacking pkmn type1', 'type2' or None]
        :param  type_dict:  {'atk_type': ['defending types', ]}"""

    # return ['types based on effectiveness', ]
    t1, t2 = pkmn_types     # extract pkmn types
    return type_dict.get(t1, []) + type_dict.get(t2, []) if t2 is not None else type_dict.get(t1, [])


# Use the static type-interaction dictionaries to generate stats unique to the pokemon's type combination
def generate_pkmn_stats(all_types, pkmn_types, all_swri):

    """ :param  all_types:  ['all types', ]
        :param pkmn_types:  ['attacking pkmn type1', 'type2' or None]
        :param   all_swri:  [{(combo, ): ['strengths', ]}, {(combo, ): ['weakness', ]},
                             {(combo, ): ['resisted', ]}, {(combo, ): ['immune', ]}]"""

    # extract 'swri' dictionaries
    strengths, weaknesses, resistances, immunities = all_swri

    # generate type-interaction lists
    weak = generate_type_list(pkmn_types, weaknesses)
    resist = generate_type_list(pkmn_types, resistances)
    strength = generate_type_list(pkmn_types, strengths)
    immune = generate_type_list(pkmn_types, immunities)

    # sort lists
    strength = sorted(set(strength), key=lambda t: all_types.index(t))
    immune = sorted(immune, key=lambda t: all_types.index(t))

    # filter lists
    weaknessss = [pkmn_type for pkmn_type in weak if pkmn_type not in immune]       # Remove immunities
    weaknesss = [pkmn_type for pkmn_type in weaknessss if pkmn_type not in resist]  # filter resistances
    resisteddd = [pkmn_type for pkmn_type in resist if pkmn_type not in immune]     # Remove immunities
    resistedd = [pkmn_type for pkmn_type in resisteddd if pkmn_type not in weak]    # filter weaknesses

    # sort lists
    weakness = sorted(weaknesss, key=lambda t: all_types.index(t))
    resisted = sorted(resistedd, key=lambda t: all_types.index(t))

    return [strength, weakness, resisted, immune]


# Generate Dictionaries using Static Dictionaries; {type combo: [static dictionary calc]}
def generate_combo_dicts(all_types, type_combos, all_swri):

    """ :param   all_types:  ['all types', ]
        :param type_combos:  [[type combos], ['type_1','type_2'], ]
        :param    all_swri:  [{combo_strengths}, {combo_weakness}, {combo_resisted}, {combo_immune}]"""

    # initialize dictionaries
    combo_strengths, combo_weakness, combo_resisted, combo_immune = {}, {}, {}, {}

    # generate dictionaries  {(type combo): [effectiveness_list]}
    for combo in type_combos:

        # create defending 'pkmn'
        def_pkmn = Pkmn(all_types, combo, all_swri)

        # append defending 'pkmn' effectiveness to combo dict; dict key cannot be list, must be tuple
        combo_strengths[tuple(combo)] = def_pkmn.strength
        combo_weakness[tuple(combo)] = def_pkmn.weakness
        combo_resisted[tuple(combo)] = def_pkmn.resisted
        combo_immune[tuple(combo)] = def_pkmn.immune

    # Sort the dictionaries
    combo_strengths = dict(sorted(combo_strengths.items(), key=lambda item: len(item[1]), reverse=True))
    combo_weakness = dict(sorted(combo_weakness.items(), key=lambda item: len(item[1]), reverse=True))
    combo_resisted = dict(sorted(combo_resisted.items(), key=lambda item: len(item[1]), reverse=True))
    combo_immune = dict(sorted(combo_immune.items(), key=lambda item: len(item[1]), reverse=True))

    return [combo_strengths, combo_weakness, combo_resisted, combo_immune]


# Generate dictionary: weak counts = {type: {length([combos]): [combos]}}
def type_counts(pkmn_types, combo_swri):

    """ :param pkmn_types:  ['attacking pkmn type1', 'type2' or None]
        :param combo_swri:  [{(type_combo): [types effected by type_combo], }, ]"""

    # Extract the dictionaries from [combo_swri]
    combo_strengths, combo_weakness, combo_resisted, combo_immune = combo_swri

    # generate the occurrences in weak_counts
    weak_counts = {t: {'count': len([combo for combo, weak in combo_weakness.items() if t in weak]),
                       'combos': [combo for combo, weak in combo_weakness.items() if t in weak]} for t in pkmn_types}

    # generate the occurrences in resist_counts
    resist_counts = {t: {'count': len([combo for combo, resist in combo_resisted.items() if t in resist]),
                         'combos': [combo for combo, resist in combo_resisted.items() if t in resist]}
                     for t in pkmn_types}

    # generate the occurrences in immune_counts
    immune_counts = {t: {'count': len([combo for combo, immune in combo_immune.items() if t in immune]),
                         'combos': [combo for combo, immune in combo_immune.items() if t in immune]}
                     for t in pkmn_types}

    # Sort the occurrences dictionary by count in descending order
    sorted_weak_counts = dict(sorted(weak_counts.items(), key=lambda item: item[1]['count'], reverse=True))
    sorted_resist_counts = dict(sorted(resist_counts.items(), key=lambda item: item[1]['count'], reverse=True))
    sorted_immune_counts = dict(sorted(immune_counts.items(), key=lambda item: item[1]['count'], reverse=True))

    return [sorted_weak_counts, sorted_resist_counts, sorted_immune_counts]


# Get list of [(type_combos,) that 'pkmn' does not (2 * damage) to]
def get_combo_difference(atk_types, type_combos, weak_counts):

    """ :param   atk_types:  ['attacking pkmn's types', ]
        :param type_combos:  [[type combos], ['type_1','type_2'], ]
        :param weak_counts:  {'atk_type': {'count': int(), 'combos': [[type combos], ]}"""

    # make list [remove_these_combos]; used to remove stab covered combos from [these_combos]
    remove_these_combos = []

    # [atk_types] = list of types 'this_pkmn' does (2*damage) to
    for strength in atk_types:

        # {'atk_type': {'count': count, ('type_combo',): [(type_combos,) that 'atk_type' does (2*damage) to]}}
        for atk_type, v in weak_counts.items():

            # if 'this_pkmn' type == atk_type:
            if strength == atk_type:

                # iterate [(type_combos,) that 'this_pkmn' does (2*damage) to]
                for combo in v['combos']:

                    # append [(type_combos,) that 'this_pkmn' does (2*damage) to] to [remove_these_combos]
                    remove_these_combos.append(combo)

    # remove duplicate [(type_combos,) that 'this_pkmn' does (2*damage) to] from [remove_these_combos]
    remove_these_combos = list(dict.fromkeys(remove_these_combos))

    # last_bit_of_combos = [(type_combos,) that 'this_pkmn' does not (2*damage) to]
    return set(type_combos) - set(remove_these_combos)


# generate data for coverage chart
def get_coverage(pkmn_types, type_counts):

    """ :param  pkmn_types:  ['attacking pkmn's types', ]
        :param type_counts:  {'pkmn_type': {'count': int(), 'combos': [[type combos], ]}"""

    # extract type counts dictionaries [{weak_counts}, {resist_counts}, {immune_counts}]
    weak_counts, resist_counts, immune_counts = type_counts

    # empty lists needed for print_coverage()
    types_header, effectiveness_lst = [], []

    # Sorting the types based on the amount of weaknesses (then resistances, then immunities, if tie)
    pkmn_types.sort(key=lambda count: immune_counts[count].get("count") if count in immune_counts else 0, reverse=True)
    pkmn_types.sort(key=lambda count: resist_counts[count].get("count") if count in resist_counts else 0, reverse=True)
    pkmn_types.sort(key=lambda count: weak_counts[count].get("count") if count in weak_counts else 0, reverse=True)

    # get the top 4 coverage options
    for t in pkmn_types[:4]:

        # 'this_pkmn.type = str(t)' for coverage table header
        if t is not None:
            types_header.append(str(t))

            # get data for type effectiveness
            weak = f'{(weak_counts[t].get("count") if t in weak_counts else None)} weak to'
            resist = f'{(resist_counts[t].get("count") if t in resist_counts else None)} resists'
            immune = f'{(immune_counts[t].get("count") if t in immune_counts else None)} immune'

            # append type effectiveness data to [a_lst]
            a_lst = [weak, resist, immune]

            # append type effectiveness data = [effectiveness_lst] for use in print_coverage()
            effectiveness_lst.append(a_lst)

    # return lists [[coverage table header], [" " data]]
    return [types_header, effectiveness_lst]


# join coverage
def join_coverage(stab_coverage, coverage_options):

    """ :param    stab_coverage:  [[types for stab coverage header], [[stab effectiveness data], ]]
        :param coverage_options:  [[types for coverage options header], [[options effectiveness data], ]]"""

    # declare coverage data
    stab_header, stab_effectiveness_lst = stab_coverage
    options_header, options_effectiveness_lst = coverage_options

    # concatenate header and effectiveness lists
    new_header = stab_header + options_header
    new_effectiveness = stab_effectiveness_lst + options_effectiveness_lst

    # Return the new coverage
    return [new_header, new_effectiveness]


# print coverage options in tabular format
def print_coverage(coverage):

    """ :param coverage:  [[coverage table header], [[effectiveness data], ]]"""

    # extract lists from coverage
    types_header, effectiveness_lst = coverage

    # print the table header
    titles = ['STAB Damage ', 'Coverage Options ']
    title_row = ' |'.join(f'{column:<30}' if len(types_header) > 5 else f'{column:<15}' for column in titles)
    header_row = '|'.join(f'{column:<15}' for column in types_header)
    print(f'\tC O V E R A G E :\t\t|  {title_row}')
    print(f'\t\t\t\t\t\t\t|  {header_row}')
    print('\t\t\t\t\t\t\t| ', '-' * len(header_row))

    # transpose the effectiveness_lst
    transposed_effectiveness_lst = zip(*effectiveness_lst)

    # Print the table data
    for row in transposed_effectiveness_lst:
        row_str = '|'.join(f'{str(cell):<15}' for cell in row)
        print('\t\t\t\t\t\t\t| ', row_str)
    print('\t\t\t\t\t\t\t| ', '-' * len(header_row), '\n\n')


if __name__ == '__main__':
    print(f'\n\n\t\t** printed from "poke_functions" **\n\n\n')