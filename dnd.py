#!python

#auto-py-to-exe

#TODO: add a combat encounter challenge rating table (dm guide p. 82)
    # calculate easy / medium / hard / deadly encounter XP based on character levels (and multiply based on num of monsters)

#TODO: add a conditions lookup (i.e conditions prone will return a description of prone.)

#TODO: Potentially add a time/date tracker (would need to add something like a save file to permanently save and increase time)

import argparse
import sys
import random
from dnd_collections import *

def d4(num_rolls=1):
    if num_rolls == 1:
        return random.randint(1, 4)
    else:
        return sum(random.randint(1, 4) for _ in range(num_rolls))

def d6(num_rolls=1):
    if num_rolls == 1:
        return random.randint(1, 6)
    else:
        return sum(random.randint(1, 6) for _ in range(num_rolls))

def d8(num_rolls=1):
    if num_rolls == 1:
        return random.randint(1, 8)
    else:
        return sum(random.randint(1, 8) for _ in range(num_rolls))

def d10():
    return random.randint(1, 10)
def d12():
    return random.randint(1, 12)

def d20():
    return random.randint(1, 20)

def d100():
    return random.randint(1, 100)

def random_money_reward(challenge_rating, treasure, individual_or_hoard, num):
    roll = d100()
    if 0 <= challenge_rating <= 4:
        if individual_or_hoard == 'hoard':
            treasure['Copper'] += d6(6) * 100
            treasure['Silver'] += d6(3) * 100
            treasure['Gold'] += d6(2) * 10
        else:
            if 1 <= roll <= 30:
                treasure['Copper'] += d6(5)
            elif 31 <= roll <= 60:
                treasure['Silver'] += d6(4)
            elif 61 <= roll <= 70:
                treasure['Electrum'] += d6(3)
            elif 71 <= roll <= 95:
                treasure['Gold'] += d6(3)
            else:
                treasure['Platinum'] += d6()
    elif 5 <= challenge_rating <= 10:
        if individual_or_hoard == 'hoard':
            pass
        else:
            if 1 <= roll <= 30:
                treasure['Copper'] += d6(4) * 100
                treasure['Electrum'] += d6() * 10
            elif 31 <= roll <= 60:
                treasure['Silver'] += d6(6) * 10
                treasure['Gold'] += d6(2) * 10
            elif 61 <= roll <= 70:
                treasure['Electrum'] += d6(3) * 10
                treasure['Gold'] += d6(2) * 10
            elif 71 <= roll <= 95:
                treasure['Gold'] += d6(4) * 10
            else:
                treasure['Gold'] += d6(2) * 10
                treasure['Platinum'] += d6(3) * 10
    if num == 1:
        return treasure
    else:
       return random_money_reward(challenge_rating, treasure, individual_or_hoard, num - 1)

def gem_art_reward(challenge_rating, gems_art):

    die = d100()
    
    if 0 <= challenge_rating <= 4:
        if 7 <= die <= 16:
            if '10' not in gems_art:
                gems_art['10'] = []
            for _ in range(0, d6(2)):
                gems_art['10'].append(random.choice(gemstones[10]))

        elif 17 <= die <= 26:
            if '25' not in gems_art:
                gems_art['25'] = []
            for _ in range(0, d4(2)):
                gems_art['25'].append(random.choice(art_objects[25]))

        elif 27 <= die <= 36:
            if '50' not in gems_art:
                gems_art['50'] = []
            for _ in range(0, d6(2)):
                gems_art['50'].append(random.choice(gemstones[50]))

        elif 37 <= die <= 44:
            if '10' not in gems_art:
                gems_art['10'] = []
            if 'Items' not in gems_art:
                gems_art['Items'] = []
            for _ in range(0, d6(2)):
                gems_art['10'].append(random.choice(gemstones[10]))
            for _ in range(0, d6()):
                gems_art['Items'].append(random.choice(list(magic_items_a.values()))) #magic items are dicts

        elif 45 <= die <= 52:
            if '25' not in gems_art:
                gems_art['25'] = []
            if 'Items' not in gems_art:
                gems_art['Items'] = []
            for _ in range(d4(2)):
                gems_art['25'].append(random.choice(art_objects[25]))
            for _ in range(d6()):
                gems_art['Items'].append(random.choice(list(magic_items_a.values())))

        elif 53 <= die <= 60:
            if '50' not in gems_art:
                gems_art['50'] = []
            if 'Items' not in gems_art:
                gems_art['Items'] = []    
            for _ in range(d6(2)):
                gems_art['50'].append(random.choice(gemstones[50]))
            for _ in range(d6()):
                gems_art['Items'].append(random.choice(list(magic_items_a.values())))

        elif 61 <= die <= 65:
            if '10' not in gems_art:
                gems_art['10'] = []
            if 'Items' not in gems_art:
                gems_art['Items'] = []
            for _ in range(d6(2)):
                gems_art['10'].append(random.choice(gemstones[10]))
            for _ in range(d4()):
                gems_art['Items'].append(random.choice(list(magic_items_b.values())))

        elif 66 <= die <= 70:
            if '25' not in gems_art:
                gems_art['25'] = []
            if 'Items' not in gems_art:
                gems_art['Items'] = []
            for _ in range(d4(2)):
                gems_art['25'].append(random.choice(art_objects[25]))
            for _ in range(d4()):
                gems_art['Items'].append(random.choice(list(magic_items_b.values())))

        elif 71 <= die <= 75:
            if '50' not in gems_art:
                gems_art['50'] = []
            if 'Items' not in gems_art:
                gems_art['Items'] = []
            for _ in range(d6(2)):
                gems_art['50'].append(random.choice(gemstones[50]))
            for _ in range(d4()):
                gems_art['Items'].append(random.choice(list(magic_items_b.values())))

        elif 76 <= die <= 78:
            if '10' not in gems_art:
                gems_art['10'] = []
            if 'Items' not in gems_art:
                gems_art['Items'] = []
            for _ in range(d6(2)):
                gems_art['10'].append(random.choice(gemstones[10]))
            for _ in range(d4()):
                gems_art['Items'].append(random.choice(list(magic_items_c.values())))

        elif 79 <= die <= 80:
            if '25' not in gems_art:
                gems_art['25'] = []
            if 'Items' not in gems_art:
                gems_art['Items'] = []
            for _ in range(d4(2)):
                gems_art['25'].append(random.choice(art_objects[25]))
            for _ in range(d4()):
                gems_art['Items'].append(random.choice(list(magic_items_c.values())))

        elif 81 <= die <= 85:
            if '50' not in gems_art:
                gems_art['50'] = []
            if 'Items' not in gems_art:
                gems_art['Items'] = []
            for _ in range(d6(2)):
                gems_art['50'].append(random.choice(gemstones[50]))
            for _ in range(d4()):
                gems_art['Items'].append(random.choice(list(magic_items_c.values())))

        elif 86 <= die <= 92:
            if '25' not in gems_art:
                gems_art['25'] = []
            if 'Items' not in gems_art:
                gems_art['Items'] = []
            for _ in range(d4(2)):
                gems_art['25'].append(random.choice(art_objects[25]))
            for _ in range(d4()):
                gems_art['Items'].append(random.choice(list(magic_items_f.values())))

        elif 93 <= die <= 97:
            if '50' not in gems_art:
                gems_art['50'] = []
            if 'Items' not in gems_art:
                gems_art['Items'] = []
            for _ in range(d6(2)):
                gems_art['50'].append(random.choice(gemstones[50]))
            for _ in range(d4()):
                gems_art['Items'].append(random.choice(list(magic_items_f.values())))

        elif 98 <= die <= 99:
            if '25' not in gems_art:
                gems_art['25'] = []
            if 'Items' not in gems_art:
                gems_art['Items'] = []
            for _ in range(d4(2)):
                gems_art['25'].append(random.choice(art_objects[25]))
            gems_art['Items'].append(random.choice(list(magic_items_g.values())))

        elif die == 100:
            if '50' not in gems_art:
                gems_art['50'] = []
            if 'Items' not in gems_art:
                gems_art['Items'] = []
            for _ in range(d6(2)):
                gems_art['50'].append(random.choice(gemstones[50]))
            gems_art['Items'].append(random.choice(list(magic_items_g.values())))

    return gems_art

#page 136
def treasure(challenge_rating = 0, individual_or_hoard = '', num_of_monsters = 1):
    treasure = {'Copper' : 0,
                'Silver' : 0,
                'Electrum' : 0,
                'Gold' : 0,
                'Platinum' : 0}
    gems_art = {}
    
    treasure = random_money_reward(int(challenge_rating), treasure, individual_or_hoard, int(num_of_monsters))

    if individual_or_hoard == 'hoard':
        gems_art = gem_art_reward(int(challenge_rating), gems_art) #fix

    if d100() <= 10:
        treasure['Trinket'] = random.choice(trinkets)
    print("")
    for coin_type, amount in treasure.items():
            print(f"{coin_type}: {amount}")
    for value, items in gems_art.items():
        if value.isdigit():
            print(f"Value: {value}")
        else:
            print(value)
        for item in items:
            print(f" - {item}")
    print("")

def trinket():
    print(random.choice(trinkets))

def random_magic_item(table, num):
    for _ in range(0, int(num)):
        random_number = d100()
        magic_item = next((item for range, item in magic_items(table).items() if int(range.split("-")[0]) <= random_number <= int(range.split("-")[1])), "No matching magic item")
        print(f"Magic item: {magic_item}")

def convert_dnd_currency(currency, amount_str):
    """
    Generated shamelessly with Claude AI
    """
    amount = int(amount_str)
    rates = {"copper": 1, "silver": 10, "electrum": 50, "gold": 100, "platinum": 1000}
    if currency not in rates:
        print(f"Invalid currency type: {currency}")
        return
        
    total_copper = amount * rates[currency]
    print(f"{amount} {currency} is equivalent to:")
    remaining = total_copper
    
    for curr in ["platinum", "gold", "electrum", "silver", "copper"]:
        qty, remaining = divmod(remaining, rates[curr])
        if qty > 0:
            print(f"{qty} {curr} pieces")

def rand_name(names):
    if len(names) > 2:
        if random.randint(0, 1) == 1:
             return random.choice(names[0]) + random.choice(names[2]) + random.choice(names[1])
    return random.choice(names[0]) + random.choice(names[1])

def npc(race = '', gender = '', stat_block = ''):

    stat_block = stat_block.lower()

    if race not in npc_races:
        print("race not recognized")
        return

    if gender not in ["male", "female"]:
        print("gender not recognized")
        return

    name = ""
    ac = 10
    hp = 10
    speed = 30
    weapon = ''
    ranged_weapon = ''
    challenge = ''
    perception = 10
    stats = 'STR: 10 (+0), DEX: 10 (+0), CON: 10 (+0), INT: 10 (+0), WIS: 10 (+0), CHA: 10 (+0)'

    if gender == '':
        gender = random.choice(['male', 'female'])

    if race == '':
        race = random.choice(npc_races)

    if race == 'dwarf':
        if gender == 'female':
            name = rand_name(dwarf_names_female)
        else:
            name = rand_name(dwarf_names_male)
        speed -= 5

    if race == 'human':
        if gender == 'female':
            name = rand_name(human_names_female)
        else:
            name = rand_name(human_names_male)

    if race == 'elf':
        if gender == 'female':
            name = rand_name(elf_names_female)
        else:
            name = rand_name(elf_names_male)

    if race == 'halfling':
        if gender == 'female':
            name = rand_name(halfling_names_female)
        else:
            name = rand_name(halfling_names_male)
        speed -= 5

    if race == 'gnome':
        if gender == 'female':
            name = rand_name(gnome_names_female)
        else:
            name = rand_name(gnome_names_male)
        speed -= 5

    if stat_block == 'bandit':
        ac = 12
        hp = max((d8(2) + 2), 10)
        melee_weapons = ['Scimitar (+3 to hit, 5ft range, 1d6 + 1 slashing damage)',
                        'Shortsword (+3 to hit, 5ft range, 1d6 + 1 slashing damage)',
                        'Handaxe (+3 to hit, 5ft range, 1d6 + 1 slashing damage, thrown (range 20/60)']
        weapon = random.choice(melee_weapons)
        ranged_weapon = 'Light crossbow (+3 to hit, 80/320ft range, 1d8 + 1 piercing damage)'
        challenge = '1/8 (25 XP)'
        stats = 'STR: 11 (+0), DEX: 12 (+1), CON: 12 (+1), INT: 10 (+0), WIS: 10 (+0), CHA: 10 (+0)'

    if stat_block == 'commoner':
        hp = max(d8(), 4)
        melee_weapons = ['Club (+2 to hit, 5ft range, 1d4) bludgeoning damage',
                        'Dagger (+2 to hit, 5ft range, 1d4) piercing damage, thrown (range 20/60)',
                        'Light hammer (+2 to hit, 5ft range, 1d4) bludgeoning damage, thrown (range 20/60)']
        weapon = random.choice(melee_weapons)
        challenge = '0 (10 XP)'

    if stat_block == 'acolyte':
        hp = max((d8(2)), 9)
        weapon = 'Club (+2 to hit, 5ft range, 1d4) bludgeoning damage'
        stats = 'STR: 10 (+0), DEX: 10 (+0), CON: 10 (+0), INT: 10 (+0), WIS: 14 (+2), CHA: 11 (+0)\n\nSpellcasting: Wisdom. Spell Save DC: 12. +4 to hit.\nCantrips: light, sacred flame, thaumaturgy.\n1st level (3 slots): bless, cure wounds, sanctuary'
        challenge = '1/4 (50 XP)'
        perception = 12

    if stat_block == 'cultist':
        hp = max((d8(2)), 9)
        weapon = 'Scimitar (+3 to hit, 5ft range, 1d6 + 1 slashing damage)'
        ac = 12
        stats = 'STR: 11 (+0), DEX: 12 (+1), CON: 10 (+0), INT: 10 (+0), WIS: 11 (+0), CHA: 10 (+0)\n\n Dark Devotion: Saving throws vs charmed or frightened'
        challenge = '1/8 (25 XP)'

    if stat_block == 'guard':
        ac = 16
        hp = max(11, (d8(2) + 2))
        stats = 'STR: 13 (+1), DEX: 12 (+1), CON: 12 (+1), INT: 10 (+0), WIS: 11 (+0), CHA: 10 (+0)'
        perception = 12
        challenge = '1/8 (25 XP)'
        weapon = 'Spear: (+3 to hit, 5ft range, thrown (range 20/60 ft). 1d6 + 1 piercing damage or 1d8 + 1 if 2h)'

    print(f"\nNPC is a {gender} {race} called {name}")
    print(f"Character has appearance: {random.choice(npc_appearance)}")
    print(f"Character has mannerism: {random.choice(npc_mannerism)}")
    print(f"Character has trait: {random.choice(npc_traits)}\n")
    print(f'AC: {ac}')
    print(f'HP: {hp}\n')
    if weapon != '':
        print(f"Melee weapon:\n{weapon}")
    if ranged_weapon != '':
        print(f"Ranged weapon:\n{ranged_weapon}\n")
    print(f"Challenge rating {challenge}")
    print(f"Passive perception {perception}")
    print(f"{stats}\n")

def encounter(num_encounters = 2):
    social_encounters = [
        "Traveling merchant with unusual wares",
        "Lost pilgrim seeking directions",
        "Wounded adventurer needing aid",
        "Local hunters warning of dangers ahead",
        "Wandering entertainer seeking audience",
        "Refugees fleeing from recent trouble",
        "Two groups about to start fighting over something"
    ]

    environmental_features = [
        "Ancient ruins partially hidden by vegetation",
        "Natural bridge across dangerous terrain",
        "Hidden cave entrance",
        "Fresh water spring with strange properties",
        "Abandoned campsite with signs of hasty departure",
        "Unusual rock formation with local legends"
    ]

    weather_events = [
        "Sudden heavy fog reducing visibility",
        "Unseasonable temperature change",
        "Brief but intense rainfall",
        "Strong winds carrying strange scents",
        "Eerie calm with unnatural silence",
        "Thunder without rain"
    ]

    tracks_and_signs = [
        "Fresh monster tracks leading somewhere",
        "Broken equipment from recent travelers",
        "Strange markings carved into trees",
        "Signs of recent battle",
        "Abandoned supplies worth investigating",
        "Ritual circle made of stones or items"
    ]

    minor_events = [
        "Tree falls blocking the path ahead",
        "Small landslide reveals something interesting",
        "Distant sounds of celebration or combat",
        "Local wildlife behaving strangely",
        "Strange lights in the distance",
        "Ground showing signs of recent disturbance"
    ]

    resource_opportunities = [
        "Patch of rare herbs or mushrooms",
        "Game animals in unusual abundance",
        "Valuable minerals visible in rock face",
        "Fruit trees with ripe produce",
        "Abandoned equipment worth salvaging",
        "Clean water source with fish"
    ]

    dangerous_encounters = [
        "Ambushed by a group of enemies",
        "Monster lair discovered with creatures inside",
        "Territorial beast defending its territory",
        "Bandits demanding toll or tribute",
        "Cursed area causing immediate effects",
        "Aggressive creature stalking the party"
    ]

    all_encounters = {
        "Social": social_encounters,
        "Environmental": environmental_features,
        "Weather": weather_events,
        "Tracks": tracks_and_signs,
        "Minor Events": minor_events,
        "Resources": resource_opportunities,
        "Dangerous": dangerous_encounters
    }

    categories = random.sample(list(all_encounters.keys()), num_encounters)
    
    print("\nRandom encounter:")
    for category in categories:
        print(random.choice(all_encounters[category]))
    print("")

def main():
    parser = argparse.ArgumentParser(description='Create random characters or scenarios with command line arguments')
    subparsers = parser.add_subparsers(dest='function', help='Commands to run')

    npc_parser = subparsers.add_parser('npc')
    npc_parser.description = 'Randomly generates an npc with a random name and characteristics'
    npc_parser.add_argument('race', nargs='?', default='', help='Parameter for random character name')
    npc_parser.add_argument('gender', nargs='?', default='', help='Parameter for random character gender, male if not specified')
    npc_parser.add_argument('stat_block', nargs='?', default='', help='Parameter for random character stat block')

    treasure_parser = subparsers.add_parser('treasure')
    treasure_parser.description = 'Randomly generates treasure from the individual/hoard treasure tables based on challenge rating. Has a 10% chance of generating a trinket'
    treasure_parser.add_argument('challenge', nargs='?', default= 0, help='Parameter for monster\'s challenge rating')
    treasure_parser.add_argument('individual_or_hoard', nargs='?', default= '', help="Specifying whether to roll from the individual treasure or treasure hoard charts. Can be 'individual' or 'hoard'. If not specified it will roll from individual treasure charts")
    treasure_parser.add_argument('num_of_monsters', nargs='?', default= 1, help='Parameter for the amount of monsters (with the same challenge rating), defaults to 1')

    trinket_parser = subparsers.add_parser('trinket')
    trinket_parser.description = 'Randomly picks a trinket from the trinket chart'

    magic_item_parser = subparsers.add_parser('magic_item')
    magic_item_parser.description = 'Generates items from the magic item tables.'
    magic_item_parser.add_argument('table', nargs='?', default="a", help="Specify which table, defaults to A if no argument is given")
    magic_item_parser.add_argument('num', nargs="?", default="1", help="Specify how many items to generate, defaults to 1 if no argument is given")

    currency_parser = subparsers.add_parser('currency')
    currency_parser.description = 'Shows conversion between currencies'
    currency_parser.add_argument('coinage', nargs='?', default="", help="Specify coinage type, for example 'copper' ")
    currency_parser.add_argument('amount', nargs="?", default=0, help="Specify coinage amount")

    encounter_parser = subparsers.add_parser('encounter')
    encounter_parser.description = 'Generates a random encounter'

    args = parser.parse_args()
    
    # Call appropriate function based on arguments
    if args.function == 'npc':
        npc(args.race, args.gender, args.stat_block)
    elif args.function == 'treasure':
        treasure(args.challenge, args.individual_or_hoard, args.num_of_monsters)
    elif args.function == 'trinket':
        trinket()
    elif args.function == 'magic_item':
        random_magic_item(args.table, args.num)
    elif args.function == 'currency':
        convert_dnd_currency(args.coinage, args.amount)
    elif args.function == 'encounter':
        encounter()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()