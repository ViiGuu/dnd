#!python

#auto-py-to-exe

#PROBABLY REDUNDANT because of the online generator (which might also be more user-friendly than a CLI)
#TODO: add a combat encounter challenge rating table (dm guide p. 82)
    # calculate easy / medium / hard / deadly encounter XP based on character levels (and multiply based on num of monsters)

#TODO: add a conditions lookup (i.e conditions prone will return a description of prone.)

import argparse
import sys
import random
from dnd_collections import *
from harptos_calendar import HarptosCalendar
from dice import *

calendar = HarptosCalendar.load_from_file()

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

def hoard_gem_art_cr_0_4(die, gems_art):
    """
    I know, this code is pure spaghetti
    """
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

def gem_art_reward(challenge_rating, gems_art):
    """
    Depending on challenge rating, returns an amount of gems and art items.
    """
    die = d100()
    
    if 0 <= challenge_rating <= 4:
        return hoard_gem_art_cr_0_4(die, gems_art)

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
            prefix = random.choice(names[0])
            middle = random.choice(names[2])
            suffix = random.choice(names[1])
            while prefix.lower() == middle.lower() or middle.lower() == suffix.lower(): 
                middle = random.choice(names[2])
            while prefix.lower() == suffix.lower() or middle.lower() == suffix.lower():
                suffix = random.choice(names[1])
            return prefix + middle + suffix
        
    prefix = random.choice(names[0])
    suffix = random.choice(names[1])
    while prefix.lower() == suffix.lower():
        suffix = random.choice(names[1])
    return prefix + suffix

def npc(race = '', gender = '', stat_block = ''):

    stat_block = stat_block.lower()

    if race not in npc_races:
        if race == '':
            race = random.choice(npc_races)
            print(f"Random race {race}")
        else:
            print("Race not recognised")
            return
        

    if gender not in ["male", "female"]:
        if gender == '':
            gender = random.choice(["male", "female"])
            print(f"Random gender: {gender}")
        else:
            print("Gender not recognised")
            return

    if stat_block not in npc_stat_blocks:
        if stat_block == '':
            stat_block = random.choice(npc_stat_blocks)
            print(f"Random stat block: {stat_block}")
        else:
            print("Stat block not recognised")
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
    traits = []
    spells = []

    if race == 'dwarf':
        if gender == 'female':
            name = rand_name(dwarf_names_female)
        else:
            name = rand_name(dwarf_names_male)
        speed -= 5
        traits.append("Darkvision 60ft")
        traits.append("Resistance vs poison damage")
        traits.append("Advantage on saving throws vs poison")

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
        traits.append("Advantage on saving throws vs charmed")
        traits.append("Immunity vs magical sleep")

    if race == 'halfling':
        if gender == 'female':
            name = rand_name(halfling_names_female)
        else:
            name = rand_name(halfling_names_male)
        speed -= 5
        traits.append("Advantage on saving throws vs frightened")
        traits.append("Can reroll natural 1 (must use new results)")

    if race == 'gnome':
        if gender == 'female':
            name = rand_name(gnome_names_female)
        else:
            name = rand_name(gnome_names_male)
        speed -= 5
        traits.append("Advantage on Intelligence, Wisdom, and Charisma saving throws against magic")

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
        stats = 'STR: 10 (+0), DEX: 10 (+0), CON: 10 (+0), INT: 10 (+0), WIS: 14 (+2), CHA: 11 (+0)'
        spells.append("Spellcasting: Wisdom. Spell Save DC: 12. +4 to hit.")
        spells.append("Cantrips: light, sacred flame, thaumaturgy.")
        spells.append("1st level (3 slots): bless, cure wounds, sanctuary")
        challenge = '1/4 (50 XP)'
        perception = 12

    if stat_block == 'cultist':
        hp = max((d8(2)), 9)
        weapon = 'Scimitar (+3 to hit, 5ft range, 1d6 + 1 slashing damage)'
        ac = 12
        stats = 'STR: 11 (+0), DEX: 12 (+1), CON: 10 (+0), INT: 10 (+0), WIS: 11 (+0), CHA: 10 (+0)'
        traits.append("Dark Devotion: Saving throws vs charmed or frightened")
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
    for trait in traits:
        print(trait)
    print("")
    for spell in spells:
        print(spell)

def encounter(num_encounters = 2):
    social_encounters = [
        "Traveling merchant with unusual wares",
        "Lost pilgrim seeking directions",
        "Wounded adventurer needing aid",
        "Local hunters warning of dangers ahead",
        "Wandering entertainer seeking audience",
        "Characters fleeing from recent trouble",
        "Two groups about to start fighting over something",
        "Mysterious wanderer with a cryptic message",
        "A pair of characters locked in a tense conversation",
        "A group of characters debating a peculiar rumor",
        "A solitary traveler offering ominous warnings",
        "An exile searching for redemption",
        "A dirty man wearing just his pants, sleeping on the ground"
    ]

    environmental_features = [
        "Ancient ruins partially hidden by vegetation",
        "Natural bridge across dangerous terrain",
        "Hidden cave entrance",
        "Fresh water spring with strange properties",
        "Abandoned campsite with signs of hasty departure",
        "Unusual rock formation",
        "Mysterious stone circle on a barren plain",
        "Weathered monolith carved with enigmatic symbols",
        "A subtle scar in the landscape hinting at ancient upheaval",
        "A series of naturally aligned pillars forming a path",
        "Oddly arranged boulders that seem out of place"
    ]

    weather_events = [
        "Sudden heavy fog reducing visibility",
        "Unseasonable temperature change",
        "Brief but intense rainfall",
        "Strong winds carrying strange scents",
        "Eerie calm with unnatural silence",
        "Thunder without rain",
        "Gusts of wind carrying faint, otherworldly whispers",
        "A rapid shift from bright sunlight to dark clouds without warning"
    ]

    tracks_and_signs = [
        "Fresh monster tracks leading somewhere",
        "Broken equipment from recent travelers",
        "Strange markings carved into trees",
        "Signs of recent battle",
        "Abandoned supplies worth investigating",
        "Ritual circle made of stones or items",
        "Faint, unidentifiable footprints leading off the beaten path",
        "A scattering of personal belongings abandoned in haste",
        "Subtle disturbances in the terrain suggesting large footsteps",
        "Cryptic symbols etched into stone, worn by time",
        "Marks that could be natural or deliberately made"
    ]

    minor_events = [
        "Tree falls blocking the path ahead",
        "Small landslide reveals something interesting",
        "Distant sounds of celebration or combat",
        "Local wildlife behaving strangely",
        "Strange lights in the distance",
        "Ground showing signs of recent disturbance",
        "A low, rumbling tremor passes through the ground",
        "A solitary, unaccounted-for object appears along the path",
        "A momentary lapse in the usual ambient sounds, leaving eerie silence"
    ]

    resource_opportunities = [
        "Patch of rare herbs or mushrooms",
        "Game animals in unusual abundance",
        "Valuable minerals visible in rock face",
        "Fruit trees with ripe produce",
        "Abandoned equipment worth salvaging",
        "Clean water source with fish",
        "A cluster of rare, vibrant minerals embedded in rock",
        "An unexpected formation of crystal-like deposits",
        "A patch of soil that appears unusually rich and fertile",
        "Signs of a long-forgotten cache of supplies or artifacts"
    ]

    dangerous_encounters = [
        "Ambushed by a group of enemies",
        "Monster lair discovered with creatures inside",
        "Territorial beast defending its territory",
        "Bandits demanding toll or tribute",
        "Cursed area causing immediate effects",
        "Aggressive creature stalking the party",
        "A sudden trap or environmental hazard forces quick action",
        "A swarm of aggressive, tiny beasts emerges unexpectedly",
        "A lone, menacing figure lurks in the shadows, watching silently"
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

def cal_set(year, month, day, hour):
    calendar = HarptosCalendar(year, month, day, hour)
    calendar.update_state()
    calendar.save_to_file()
    print(f"Calendar set to {calendar}")

def cal_progress_time(time_type, amount):
    match time_type:
        case 'hours':
            cal_progress_hours(amount)
        case 'days':
            cal_progress_days(amount)
        case 'months':
            cal_progress_months(amount)
        case 'years':
            cal_progress_years(amount)
        case _:
            print("Unknown argument for progressing time")


def cal_progress_hours(hours):
    calendar.progress_hours(hours)
    calendar.save_to_file()

def cal_progress_days(days):
    calendar.progress_days(days)
    calendar.save_to_file()

def cal_progress_months(months):
    calendar.progress_months(months)
    calendar.save_to_file()

def cal_progress_years(years):
    calendar.progress_years(years)
    calendar.save_to_file()

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

        #time parsers
    time_parser = subparsers.add_parser('time')
    time_parser.description = 'Used to set and progress time in your campaign, using the Harptos calendar. Uses automatic saving.'
    time_subparsers = time_parser.add_subparsers(dest="time_subcommand", required=False)

    set_time_parser = time_subparsers.add_parser('set')
    set_time_parser.add_argument('year', type=int, nargs='?', default=0)
    set_time_parser.add_argument('month', type=int, nargs='?', default=0)
    set_time_parser.add_argument('day', type=int, nargs='?', default=0)
    set_time_parser.add_argument('hour', type=int, nargs='?', default=0)

    add_time_parser = time_subparsers.add_parser('add')
    add_time_parser.add_argument('time_type', nargs='?', default=0)
    add_time_parser.add_argument('amount', type=int, nargs='?', default=0)
    

    args = parser.parse_args()
    
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
    elif args.function == 'time':
        if args.time_subcommand == 'set':
             cal_set(args.year, args.month, args.day, args.hour)
        elif args.time_subcommand == 'add':
            cal_progress_time(args.time_type, args.amount)
        else:
            print(calendar)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()