#!/usr/bin/env python

__author__ = 'Shamar D. Brown'
__version__ = '5.1'

'''
README:

In the game of Pokemon, a pokemon can be one or two of 18 unique types. This is known as their type combination.
 - There are 306/324 type combinations currently in use.
 - Each pokemon can attack with up to four moves.
 - Each move can be any type in the attackers move pool.
 - When pokemon attack using a move of the same type, they get a "Same-type attack bonus" or STAB

This project suggests 4 types to help users choose moves that will do the most damage to the most type combinations. 
These moves are known as "coverage."
'''


########################################################################################################################
#                                                      CLASSES                                                         #
########################################################################################################################


# Create the Pkmn class
class Pkmn:

    # initialize pkmn attributes
    def __init__(self, all_types, pkmn_types, all_swri):
        self.types = pkmn_types
        self.strength, self.weakness, self.resisted, self.immune = (
            generate_pkmn_stats(all_types, self.types, all_swri))
        self.uncovered = sorted([t for t in all_types if t not in self.strength], key=lambda t: all_types.index(t))

    # ENELFUTURO: calulate 'pkmn' stat distribution
    def calc_stats(self, base_stats, level, nature, ev_spread):
        '''
        :param base_stats: list = [hp, atk, def, sp_a, sp_d, spd]
        :param level: will stay @ 50
        :param nature: make nature dictionaries
        :param ev_spred: list with ev spread; fails if total or maxes wrong (or corrects)
        :return real_stats = calc_stats([90, 120, 75, 75, 75, 90], 50, timid, [0, 252, 4, 0, 0, 252])

        self.hp, self.atk, self.def, self.sp_a, self.sp_d, self.spd = stats
        '''

    # print 'pkmn' attributes
    def print_pkmn(self, count):
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
                # print(data)
                txt_file_data.append(data)
        # print(txt_file_data)
        txt_file.close()
    return txt_file_data


# Generate a list of all usable type combos
def generate_type_combos(types, unused_combos):
    # generate list of all possible type combinations
    all_combos = [[type1, type2] if type2 else [type1, ] for type1 in types for type2 in types]

    # Modify tuples with duplicate entries [i.e. ('fairy', 'fairy') to ('fairy', None)]
    unique_combos = [[t[0], None] if t[0] == t[1] else t for t in all_combos]

    # Remove type combos unused on real pkmn
    type_combos = [t for t in unique_combos if t not in unused_combos]
    # [print(f"{count + 1}: {combo}") for count, combo in enumerate(type_combos)]

    return type_combos


# Generate a list of types that are "type_dict" against 'pkmn'
def generate_type_list(type1, type2, type_effectiveness_dict):
    if type2 is not None:
        type_effectiveness_list = type_effectiveness_dict.get(type1, []) + type_effectiveness_dict.get(type2, [])
    else:
        type_effectiveness_list = type_effectiveness_dict.get(type1, [])
    return type_effectiveness_list


# Use the static type-interaction dictionaries to generate stats unique to the pokemon's type combination
def generate_pkmn_stats(all_types, pkmn_types, all_swri):
    # Extract dictionaries
    strengths, weaknesses, resistances, immunities = all_swri

    # initialized damage lists
    weak = generate_type_list(pkmn_types[0], pkmn_types[1], weaknesses)
    resist = generate_type_list(pkmn_types[0], pkmn_types[1], resistances)
    strength = generate_type_list(pkmn_types[0], pkmn_types[1], strengths)
    immune = generate_type_list(pkmn_types[0], pkmn_types[1], immunities)

    # sort lists
    strength = sorted(set(strength), key=lambda t: all_types.index(t))
    immune = sorted(immune, key=lambda t: all_types.index(t))

    # weakness
    weaknessss = [pkmn_type for pkmn_type in weak if pkmn_type not in immune]  # Remove immunities
    weaknesss = [pkmn_type for pkmn_type in weaknessss if pkmn_type not in resist]

    # resisted
    resisteddd = [pkmn_type for pkmn_type in resist if pkmn_type not in immune]  # Remove immunities
    resistedd = [pkmn_type for pkmn_type in resisteddd if pkmn_type not in weak]

    # sort lists
    weakness = sorted(weaknesss, key=lambda t: all_types.index(t))
    resisted = sorted(resistedd, key=lambda t: all_types.index(t))

    return [strength, weakness, resisted, immune]


# Generate Dictionaries using Static Dictionaries; {type combo: [static dictionary calc]}
def generate_combo_dicts(all_types, type_combos, all_swri):
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

    # [print(k, v) for k, v in combo_weakness.items()]
    return [combo_strengths, combo_weakness, combo_resisted, combo_immune]


# Generate Dictionaries using Static Dictionaries {pkmn_types: [static dictionary calc]}
def combo_print(combo_swri):
    # Extract the dictionaries from [combo_swri]
    combo_strengths, combo_weakness, combo_resisted, combo_immune = combo_swri

    # print(f'\ntype_combos: [all usable type combinations]\n {len(type_combos)} | {type_combos}\n')
    print(f'\ncombo_strengths: dict(pkmn_types: [combos(damaged*2.0)]\n {len(combo_strengths)} | {combo_strengths}\n')
    print(f'\ncombo_weakness: dict(combos: [pkmn_types(damaged*2.0)]\n {len(combo_weakness)} | {combo_weakness}\n')
    print(f'\ncombo_resisted: dict(pkmn_types: [combos(damaged*0.5)]\n {len(combo_resisted)} | {combo_resisted}\n')
    print(f'\ncombo_immune: dict(pkmn_types: [combos(damaged*0)]\n {len(combo_immune)} | {combo_immune}\n')


# Generate dictionary: weak counts = {type: {length([combos]): [combos]}}
def type_counts(types, combo_swri):
    # Extract the dictionaries from [combo_swri]
    combo_strengths, combo_weakness, combo_resisted, combo_immune = combo_swri

    # generate the occurrences in weak_counts
    weak_counts = {t: {'count': len([combo for combo, weak in combo_weakness.items() if t in weak]),
                       'combos': [combo for combo, weak in combo_weakness.items() if t in weak]} for t in types}

    # generate the occurrences in resist_counts
    resist_counts = {t: {'count': len([combo for combo, resist in combo_resisted.items() if t in resist]),
                         'combos': [combo for combo, resist in combo_resisted.items() if t in resist]} for t in types}

    # generate the occurrences in immune_counts
    immune_counts = {t: {'count': len([combo for combo, immune in combo_immune.items() if t in immune]),
                         'combos': [combo for combo, immune in combo_immune.items() if t in immune]} for t in types}

    # Sort the occurrences dictionary by count in descending order
    sorted_weak_counts = dict(sorted(weak_counts.items(), key=lambda item: item[1]['count'], reverse=True))
    sorted_resist_counts = dict(sorted(resist_counts.items(), key=lambda item: item[1]['count'], reverse=True))
    sorted_immune_counts = dict(sorted(immune_counts.items(), key=lambda item: item[1]['count'], reverse=True))

    return [sorted_weak_counts, sorted_resist_counts, sorted_immune_counts]


# Get list of [(type_combos,) that 'pkmn' does not (2 * damage) to]
def get_combo_difference(atk_types, type_combos, weak_counts):
    """ :param atk_types: Pkmn()
        :param weak_counts: [{weak_counts}, {resist_counts}, {immune_counts}]"""

    # make list [remove_these_combos]; used to remove stab covered combos from [these_combos]
    remove_these_combos = []

    # [this_pkmn.strength] = list of types 'this_pkmn' does (2*damage) to
    for strength in atk_types:

        # {'atk_type': {'count': count, ('type_combo',): [(type_combos,) that 'atk_type' does (2*damage) to]}}
        for atk_type, v in weak_counts.items():

            # if 'this_pkmn' type == atk_type:
            if strength == atk_type:

                '''print(f'pkmn type: {s} == dict_type: {k}')\nprint(v['count'], v['combos'])'''

                # iterate [(type_combos,) that 'this_pkmn' does (2*damage) to]
                for combo in v['combos']:
                    '''print(combo)'''

                    # append [(type_combos,) that 'this_pkmn' does (2*damage) to] to [remove_these_combos]
                    remove_these_combos.append(combo)

    # remove duplicate [(type_combos,) that 'this_pkmn' does (2*damage) to] from [remove_these_combos]
    remove_these_combos = list(dict.fromkeys(remove_these_combos))
    '''print(len(remove_these_combos), len(set(remove_these_combos)), remove_these_combos)
    print(len(these_combos), len(set(these_combos)), these_combos)'''

    # last_bit_of_combos = [(type_combos,) that 'this_pkmn' does not (2*damage) to]
    return set(type_combos) - set(remove_these_combos)


# generate data for coverage chart
def get_coverage(pkmn_types, type_counts):
    # declare type counts; [{weak_counts}, {resist_counts}, {immune_counts}]
    weak_counts, resist_counts, immune_counts = type_counts

    # these lists are needed for print_coverage()
    types_header, effectiveness_lst = [], []

    # Sorting the types based on the number of weaknesses (then resistances, then immunities, if tie)
    pkmn_types.sort(key=lambda t: immune_counts[t].get("count") if t in immune_counts else 0, reverse=True)
    pkmn_types.sort(key=lambda t: resist_counts[t].get("count") if t in resist_counts else 0, reverse=True)
    pkmn_types.sort(key=lambda t: weak_counts[t].get("count") if t in weak_counts else 0, reverse=True)

    # get the top 4 coverage options
    for t in pkmn_types[:4]:
        # 'this_pkmn.type = str(t)' for coverage table header
        types_header.append(str(t))

        # get data for type effectiveness
        weak = f'{(weak_counts[t].get("count") if t in weak_counts else None)} weak to'
        resist = f'{(resist_counts[t].get("count") if t in resist_counts else None)} resists'
        immune = f'{(immune_counts[t].get("count") if t in immune_counts else None)} immune'

        # append type effectiveness data to [a_lst]
        a_lst = [weak, resist, immune]

        '''print(t, a_lst)'''

        # append type effectiveness data = [effectiveness_lst] for use in print_coverage()
        effectiveness_lst.append(a_lst)

    # return lists [[coverage table header], [" " data]]
    return [types_header, effectiveness_lst]


# join coverage
def join_coverage(stab_coverage, coverage_options):
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
    types_header, effectiveness_lst = coverage

    # Print the table header
    titles = ['STAB Damage', 'Coverage Options']
    title_row = ' |'.join(f'{column:<30}' for column in titles)
    header_row = '|'.join(f'{column:<15}' for column in types_header)
    print(f'\tC O V E R A G E :\t\t|  {title_row}')
    print(f'\t\t\t\t\t\t\t|  {header_row}')
    print('\t\t\t\t\t\t\t| ', '-' * len(header_row))

    # Transpose the data
    transposed_data = zip(*effectiveness_lst)

    # Print the table data
    for row in transposed_data:
        row_str = '|'.join(f'{str(cell):<15}' for cell in row)
        print('\t\t\t\t\t\t\t| ', row_str)
    print('\t\t\t\t\t\t\t| ', '-' * len(header_row), '\n\n')


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
print('\n** Starting Program!\n** Ensure input file is current.\n')
better_intro = '''
** In the game of Pokemon, a pokemon can be one or two of 18 unique types. This is known as their type combination.
    - There are 306/324 type combinations currently in use.
    - Each pokemon can attack with up to four moves.
    - Each move can be any type in the attackers move pool.
    - When pokemon attack using a move of the same type, they get a "Same-type attack bonus" or STAB

This project suggests 4 types to help users choose moves that will do the most damage to the most type combinations. 
These moves are known as "coverage."'''
print(f'{better_intro}\n\n')


# import the input file
pkmn_team = import_poke_input_file(r'poke_input.txt')


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
        # setup current pkmn
        this_pkmn = Pkmn(all_types, pokemon, all_swri)

        # print 'this_pkmn' stats
        all_count = this_pkmn.print_pkmn(all_count)

        # make list [these_combos]; change from list to tuples to compare to dictionary keys
        these_combos = [tuple(combo) for combo in all_combos]

        # result = [(type_combos,) that 'this_pkmn' does not (2*damage) to]
        last_bit_of_combos = get_combo_difference(this_pkmn.strength, these_combos, all_weak_counts)

        # generate stab coverage data for this_pkmn; [[stab types_header],[stab_coverage data]]
        stab_coverage = get_coverage(this_pkmn.types, all_type_counts)

        # get type counts for coverage recommendation
        last_bit_of_combo_swri = generate_combo_dicts(all_types, last_bit_of_combos, all_swri)
        last_bit_of_counts = type_counts(all_types, last_bit_of_combo_swri)

        # generate coverage options for this_pkmn
        last_bit_of_coverage = get_coverage([t for t in all_types if t not in this_pkmn.types], last_bit_of_counts)

        # concatenate coverage data
        new_coverage = join_coverage(stab_coverage, last_bit_of_coverage)

        # print 'this_pkmn' coverage table
        print_coverage(new_coverage)

        # track the non stab types for your pokemon team
        team_nonstab_damage = [t for t in team_nonstab_damage if t not in this_pkmn.types]

# print uncoverable combos as a dictionary
print(f"\n\n\t** Your team doesn't do stab damage to {len(team_nonstab_damage)} types || {team_nonstab_damage} **\n")

########################################################################################################################
#                                                       END WORK                                                       #
########################################################################################################################
