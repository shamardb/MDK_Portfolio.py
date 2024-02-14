# SDB_Portfolio


# 1. Poke_Coverage.py

In the game of Pokemon, a pokemon can be one or two of 18 unique types. This is their type combination.
 - There are 306/324 possible type combinations currently in use.
 - Each pokemon can attack with up to four moves.
 - Each move can be any type in the attackers move pool.
 - When pokemon attack using a move of the same type, they get a "Same-type attack bonus" or STAB, where (1.5)*DAMAGE is dealt.
 - Attacks can:
     - Be Super-effective: (2.0)*DAMAGE
     - Be Resisted or 'Not very-effective': (0.5 or 0.25)*DAMAGE
     - Have no effect (Immunity): 0*DAMAGE

This project suggests 4 types to help users choose moves that will do the most damage to the most type combinations not covered by stab types. 
These moves are known as "coverage."
