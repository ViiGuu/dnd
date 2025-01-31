#!python

#auto-py-to-exe

#TODO: add a combat encounter challenge rating table (dm guide p. 82)
    # calculate easy / medium / hard / deadly encounter XP based on character levels (and multiply based on num of monsters)

#TODO: add a conditions lookup (i.e conditions prone will return a description of prone.)

#TODO: Potentially add a time/date tracker (would need to add something like a save file to permanently save and increase time)

#TODO: add onto the treasure reward (magic items tables etc.)

#TODO: add improvised damage table

#TODO: add randomised shops inventory.

import argparse
import sys
import random

    #NPC FEATURES

npc_appearance = ['Distinctive jewelry, earrings, necklace, circlet, bracelets',
                  'Piercings',
                  'Flamboyant or outlandish clothes',
                  'Formal, clean clothes',
                  'Ragged, dirty clothes',
                  'Pronounced scar',
                  'Missing teeth',
                  'Missing fingers',
                  'Unusual eye colors or heterochromia',
                  'Tattoos',
                  'Birthmark',
                  'Unusual skin color',
                  'Bald',
                  'Braided beard/hair',
                  'Unusual hair color',
                  'Nervous eye twitch',
                  'Distinctive nose',
                  'Crooked or rigid posture',
                  'Exceptionally beautiful',
                  'Exceptionally ugly',
                  'Has a limp',
                  'Visible burns.',
                  'Distinctive walk',
                  'Unusual height (extremely tall or short)',
                  'Lisps',
                  'Deformed or misshapen ears',
                  'Unique dental modifications',
                  'Pronounced muscle definition or unusual body build',
                  'Noticeably fat or lean',
                  'Distinctive hand tattoos or finger markings',
                  ]

npc_mannerism = ['Prone to singing, whistling, or humming quietly',
                 'Speaks in rhyme or some other peculiar way',
                 'Particularly low or high voice',
                 'Slurs words, lisps or stutters',
                 'Enunciates overly clearly',
                 'Speaks loudly',
                 'Whispers',
                 'Uses flowery speech or long words',
                 'Frequently uses the wrong word',
                 'Uses colorful oaths and exclamations',
                 'Makes constant jokes or puns',
                 'Prone to predictions of doom',
                 'Fidgets',
                 'Squints',
                 'Stares into the distance',
                 'Chews something',
                 'Paces',
                 'Taps fingers',
                 'Bites fingernails',
                 'Twirls hair or tugs beard',
                 'Has a nervous tic',
                 'Adjusts clothing compulsively']

npc_traits = ['Argumentative',
              'Arrogant',
              'Blustering',
              'Rude',
              'Curious',
              'Friendly',
              'Honest',
              'Hot tempered',
              'Irritable',
              'Ponderous',
              'Quiet',
              'Suspicious',
              'Paranoid']

npc_races = ['dwarf',
             'human',
             'elf',
             'halfling',
             'gnome']

    #NAMES

dwarf_names_male = [['Tho', 'Thu', 'Gi', 'Du', 'Bro', 'Ki', 'Vi', 'Vin', 'Do', 'Da', 'Mo', 'Gra', 'Mo', 'Arn', 'O', 'Ga', 'Vo'],
                    ['grym', 'grim', 'brim', 'ror', 'tur', 'li', 'lur', 'im', 'in', 'gun', 'gar', 'dis', 'rak', 'rums', 'ums', 
                    'rik', 'gern', 'sik', 'dain', 'dal'],
                    ['ga', 'ka', 'rath', 'ra', 'kha']]

dwarf_names_female = [['Vis', 'Var', 'Hel', 'Ran', 'Maer', 'Am', 'Aes', 'Ael', 'Ar', 'Aud', 'Kath', 'Gur', 'Moir', 'Bir'],
                      ['la', 'lys', 'lynn', 'ynn', 'ra', 'ta', 'dia', 'lia', 'waen', 'via', 'byr', 'tyn', 'ra', 'dis', 'na', 'nis', 'lita', 'ita'],
                      ['al', 'en', 'in', 'ae']]

human_names_male = [['Ald', 'Jor', 'Ler', 'Sig', 'Ever', 'Had', 'Ar', 'Mar', 'Al', 'Ker', 'And', 'Uth', 'Ath', 'Eth',
                    'Bren', 'Cal', 'Dav', 'El', 'Fin', 'Gar', 'Hal', 'Ian', 'Kai', 'Lor', 'Ra'], #AI 
                    ['ric', 'rim', 'nar', 'ner', 'reif', 'rian', 'mund', 'ret', 'ron', 'nam',
                    'ken', 'den', 'van', 'in', 'lon', 'gan', 'ran', 'ian'], #AI
                    ['dra', 'ka', 'ath', 'nir', 'ur', 'na', 'a', 'e', 'i', 'o',
                    'la', 'ge', 'er', 'an', 'en', 'in', 'ien', 'on']] #AI

human_names_female = [['Kat', 'Kit', 'El', 'Jan', 'Ja', 'Lea', 'Ya', 'Yan', 'Sa', 'Ai', 'Ei', 'Sar', 'San', 'Io', 'Al', 'Eld', 'Cael', 'Ae'],
                    ['nie', 'na', 'lyn', 'wyn', 'wen', 'lia', 'die', 'ra'],
                    ['no', 'ro', 'do', 'a']]

elf_names_male = [
    ['Ad', 'Ael', 'Ald', 'Ar', 'Ara', 'Aus', 'Ber', 'Bei', 'Car', 'En', 'Erd', 'Ere', 'Gal', 'Had', 'Hei', 'Hi',
     'Imm', 'Ive', 'Lau', 'Min', 'Pae', 'Per', 'Qua', 'Ria', 'Rol', 'Sov', 'Thal', 'Ther', 'Var'],

    ['ran', 'ar', 'il', 'is', 'o', 'an', 'en', 'ion'],

    ['ram', 'am', 'an', 'el', 'ian', 'ric', 'lis', 'dan', 'ai', 'en', 'ion', 'len', 'liss', 'ior', 'vol', 'ren', 'dar', 'rel']
]

elf_names_female = [
    ['A', 'E', 'Ad', 'Al', 'Anas', 'And', 'Ant', 'Beth', 'Bir', 'Cae', 'Dru', 'En', 'Fel', 'Iel', 'Jel', 'Key', 'Lesh', 
     'Li', 'Mer', 'Mi', 'Na', 'Quel', 'Quil', 'Sar', 'Shan', 'Shaev', 'Sil', 'Thei', 'Thi', 'Vad', 'Val', 'Xan'],
    ['rie', 'thaea', 'ianna', 'inua', 'na', 'nia', 'athe', 'ath', 'asta', 'ia', 'the', 'phia', 'ra', 'la', 'in', 'anna'],
    ['stas', 'laste', 'naste', 'ryn', 'rel', 'lyn', 'lia', 'na', 'lial', 'ne', 'le', 'a', 'e', 'nan', 'lan', 'liel', 'riele', 'va',  've', 'len', 'lui']
]

halfling_names_male = [['Al', 'An', 'Ca', 'Cor', 'El', 'Er', 'Fin', 'Gar', 'Lin', 'Lyl', 'Mer', 'Mil', 'Os', 'Perr', 'Re', 'Rosc', 'Well'],
                    ['ton', 'der', 'de', 'rin', 'don', 'rich', 'nan', 'dal', 'ric', 'born', 'rin', 'by']]
halfling_names_female = [['Andr', 'Br', 'Call', 'Cor', 'Euphem', 'Jill', 'Kithr', 'Lavin', 'Lidd', 'Merl', 'Nedd', 'Pael', 'Port', 'Seraph',
                    'Shaen', 'Tr', 'Van', 'Vern'],
                    ['y', 'ee', 'ie', 'a', 'ia', 'ian', 'i', 'ina', 'ini']]

gnome_names_male = [['Alst', 'Al', 'Bodd', 'Br', 'Burg', 'Dimb', 'Eld', 'Erk', 'Fonk', 'Bonk', 'Fr', 'Gerb', 'Gorb', 'Gimbl', 'Glim',
                    'Jebedd', 'Kell', 'Namf', 'Orr', 'Roond', 'Seeb', 'Sindr', 'Warr', 'Wre', 'Zo'],
                    ['on', 'yn', 'ock', 'occ', 'ell', 'le', 'in', 'oodle', 'o', 'e', 'im', 'i', 'enn']]
gnome_names_female = [['Bimp', 'Breen', 'Caram', 'Carl', 'Don', 'Duvam', 'Elly', 'Lill', 'Loop', 'Boop', 'Bopp', 'Lorill', 'Mard', 'Niss',
                    'Od', 'Orl', 'Royw', 'Sham', 'Tan', 'Wayw', "Zann", 'Zap'],
                    ['nottin', 'a', 'y', 'ie', 'ip', 'in', 'ella', 'il', 'jobell', 'bell', 'wick', 'i', 'mottin', 'illa', 'nab', 'ix', 'wyn',
                    'wocket']]

    #TREASURE

gemstones = {
    10: [
        "Azurite (opaque mottled deep blue)",
        "Banded agate (translucent striped brown, blue, white, or red)",
        "Blue quartz (transparent pale blue)",
        "Eye agate (translucent circles of gray, white, brown, blue, or green)",
        "Hematite (opaque gray-black)",
        "Lapis lazuli (opaque light and dark blue with yellow flecks)",
        "Malachite (opaque striated light and dark green)",
        "Moss agate (translucent pink or yellow-white with mossy gray or green markings)",
        "Obsidian (opaque black)",
        "Rhodochrosite (opaque light pink)",
        "Tiger eye (translucent brown with golden center)",
        "Turquoise (opaque light blue-green)"
    ],
    50: [
        "Bloodstone (opaque dark gray with red flecks)",
        "Carnelian (opaque orange to red-brown)",
        "Chalcedony (opaque white)",
        "Chrysoprase (translucent green)",
        "Citrine (transparent pale yellow-brown)",
        "Jasper (opaque blue, black, or brown)",
        "Moonstone (translucent white with pale blue glow)",
        "Onyx (opaque bands of black and white, or pure black or white)",
        "Quartz (transparent white, smoky gray, or yellow)",
        "Sardonyx (opaque bands of red and white)",
        "Star rose quartz (translucent rosy stone with white star-shaped center)",
        "Zircon (transparent pale blue-green)"
    ],
    100: [
        "Amber (transparent watery gold to rich gold)",
        "Amethyst (transparent deep purple)",
        "Chrysoberyl (transparent yellow-green to pale green)",
        "Coral (opaque crimson)",
        "Garnet (transparent red, brown-green, or violet)",
        "Jade (translucent light green, deep green, or white)",
        "Jet (opaque deep black)",
        "Pearl (opaque lustrous white, yellow, or pink)",
        "Spinel (transparent red, red-brown, or deep green)",
        "Tourmaline (transparent pale green, blue, brown, or red)"
    ],
    500: [
        "Alexandrite (transparent dark green)",
        "Aquamarine (transparent pale blue-green)",
        "Black pearl (opaque pure black)",
        "Blue spinel (transparent deep blue)",
        "Peridot (transparent rich olive green)",
        "Topaz (transparent golden yellow)",
        "Black sapphire (translucent lustrous black with glowing highlights)",
        "Diamond (transparent blue-white, canary, pink, brown, or blue)",
        "Jacinth (transparent fiery orange)",
        "Ruby (transparent clear red to deep crimson)"
    ],
    1000: [
        "Black opal (translucent dark green with black mottling and golden flecks)",
        "Blue sapphire (transparent blue-white to medium blue)",
        "Emerald (transparent deep bright green)",
        "Fire opal (translucent fiery red)",
        "Opal (translucent pale blue with green and golden mottling)",
        "Star ruby (translucent ruby with white star-shaped center)",
        "Star sapphire (translucent blue sapphire with white star-shaped center)",
        "Yellow sapphire (transparent fiery yellow or yellow-green)"
    ]
}

art_objects = {
    25: [
        "Silver ewer",
        "Carved bone statuette",
        "Small gold bracelet",
        "Cloth-of-gold vestments",
        "Black velvet mask stitched with silver thread",
        "Copper chalice with silver filigree",
        "Pair of engraved bone dice",
        "Small mirror set in a painted wooden frame",
        "Embroidered silk handkerchief",
        "Gold locket with a painted portrait inside"
    ],
    250: [
        "Gold ring set with bloodstones",
        "Carved ivory statuette",
        "Large gold bracelet",
        "Silver necklace with a gemstone pendant",
        "Bronze crown",
        "Silk robe with gold embroidery",
        "Large well-made tapestry",
        "Brass mug with jade inlay",
        "Box of turquoise animal figurines",
        "Gold bird cage with electrum filigree"
    ],
    750: [
        "Silver chalice set with moonstones",
        "Silver-plated steel longsword with jet set in hilt",
        "Carved harp of exotic wood with ivory inlay and zircon gems",
        "Small gold idol",
        "Gold dragon comb set with red garnets as eyes",
        "Bottle stopper cork embossed with gold leaf and set with amethysts",
        "Ceremonial electrum dagger with a black pearl in the pommel",
        "Silver and gold brooch",
        "Obsidian statuette with gold fittings and inlay",
        "Painted gold war mask"
    ],
    2500: [
        "Fine gold chain set with a fire opal",
        "Old masterpiece painting",
        "Embroidered silk and velvet mantle set with numerous moonstones",
        "Platinum bracelet set with a sapphire",
        "Embroidered glove set with jewel chips",
        "Jeweled anklet",
        "Gold music box",
        "Gold circlet set with four aquamarines",
        "Eye patch with a mock eye set in blue sapphire and moonstone",
        "A necklace string of small pink pearls"
    ],
    7500: [
        "Jeweled gold crown",
        "Jeweled platinum ring",
        "Small gold statuette set with rubies",
        "Gold cup set with emeralds",
        "Gold jewelry box with platinum filigree",
        "Painted gold child's sarcophagus",
        "Jade game board with solid gold playing pieces",
        "Bejeweled ivory drinking horn with gold filigree"
    ]
}

trinkets = [
    "A mummified goblin hand",
    "A piece of crystal that faintly glows in the moonlight",
    "A gold coin minted in an unknown land",
    "A diary written in a language you don't know",
    "A brass ring that never tarnishes",
    "An old chess piece made from glass",
    "A pair of knucklebone dice, each with a skull symbol on the side that would normally show six pips",
    "A small idol depicting a nightmarish creature that gives you unsettling dreams when you sleep near it",
    "A rope necklace from which dangles four mummified elf fingers",
    "The deed for a parcel of land in a realm unknown to you",
    "A 1-ounce block made from an unknown material",
    "A small cloth doll skewered with needles",
    "A tooth from an unknown beast",
    "A bright green feather",
    "An enormous scale, perhaps from a dragon",
    "An old divination card bearing your likeness",
    "A glass orb filled with moving smoke",
    "A 1-pound egg with a bright red shell",
    "A pipe that blows bubbles",
    "A glass jar containing a weird bit of flesh floating in pickling fluid",
    "A tiny gnome-crafted music box that plays a song you dimly remember from your childhood",
    "A small wooden statuette of a smug halfling",
    "A brass orb etched with strange runes",
    "A multicolored stone disk",
    "A tiny silver icon of a raven",
    "A bag containing forty-seven humanoid teeth, one of which is rotten",
    "A shard of obsidian that always feels warm to the touch",
    "A dragon's bony talon hanging from a plain leather necklace",
    "A pair of old socks",
    "A blank book whose pages refuse to hold ink, chalk, graphite, or any other substance or marking",
    "A silver badge in the shape of a five-pointed star",
    "A knife that belonged to a relative",
    "A glass vial filled with nail clippings",
    "A rectangular metal device with two tiny metal cups on one end that throws sparks when wet",
    "A white, sequined glove sized for a human",
    "A vest with one hundred tiny pockets",
    "A small, weightless stone block",
    "A tiny sketch portrait of a goblin",
    "An empty glass vial that smells of perfume when opened",
    "A gemstone that looks like a lump of coal when examined by anyone but you",
    "A scrap of cloth from an old banner",
    "A rank insignia from a lost legionnaire",
    "A tiny silver bell without a clapper",
    "A mechanical canary inside a gnomish lamp",
    "A tiny chest carved to look like it has numerous feet on the bottom",
    "A dead sprite inside a clear glass bottle",
    "A metal can that has no opening but sounds as if it is filled with liquid, sand, spiders, or broken glass (your choice)",
    "A glass orb filled with water, in which swims a clockwork goldfish",
    "A silver spoon with an M engraved on the handle",
    "A whistle made from gold-colored wood",
    "A dead scarab beetle the size of your hand",
    "Two toy soldiers, one with a missing head",
    "A small box filled with different-sized buttons",
    "A candle that can't be lit",
    "A tiny cage with no door",
    "An old key",
    "An indecipherable treasure map",
    "A hilt from a broken sword",
    "A rabbit's foot",
    "A glass eye",
    "A cameo carved in the likeness of a hideous person",
    "A silver skull the size of a coin",
    "An alabaster mask",
    "A pyramid of sticky black incense that smells very bad",
    "A nightcap that, when worn, gives you pleasant dreams",
    "A single caltrop made from bone",
    "A gold monocle frame without the lens",
    "A 1-inch cube, each side painted a different color",
    "A crystal knob from a door",
    "A small packet filled with pink dust",
    "A fragment of a beautiful song, written as musical notes on two pieces of parchment",
    "A silver teardrop earring made from a real teardrop",
    "The shell of an egg painted with scenes of human misery in disturbing detail",
    "A fan that, when unfolded, shows a sleeping cat",
    "A set of bone pipes",
    "A four-leaf clover pressed inside a book discussing manners and etiquette",
    "A sheet of parchment upon which is drawn a complex mechanical contraption",
    "An ornate scabbard that fits no blade you have found so far",
    "An invitation to a party where a murder happened",
    "A bronze pentacle with an etching of a rat's head in its center",
    "A purple handkerchief embroidered with the name of a powerful archmage",
    "Half of a floorplan for a temple, castle, or some other structure",
    "A bit of folded cloth that, when unfolded, turns into a stylish cap",
    "A receipt of deposit at a bank in a far-flung city",
    "A diary with seven missing pages",
    "An empty silver snuffbox bearing an inscription on the surface that says 'dreams'",
    "An iron holy symbol devoted to an unknown god",
    "A book that tells the story of a legendary hero's rise and fall, with the last chapter missing",
    "A vial of dragon blood",
    "An ancient arrow of elven design",
    "A needle that never bends",
    "An ornate brooch of dwarven design",
    "An empty wine bottle bearing a pretty label that says 'The Wizard of Wines Winery, Red Dragon Crush, 331422-W'",
    "A mosaic tile with a multicolored, glazed surface",
    "A petrified mouse",
    "A black pirate flag adorned with a dragon's skull and crossbones",
    "A tiny mechanical crab or spider that moves about when it's not being observed",
    "A glass jar containing lard with a label that reads 'Griffon Grease'",
    "A wooden box with a ceramic bottom that holds a living worm with a head on each end of its body",
    "A metal urn containing the ashes of a hero"
]

def d4():
    return random.randint(1, 4)

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

def random_money_reward(challenge_rating, treasure, num, individual_or_hoard):
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
       return random_money_reward(challenge_rating, treasure, num - 1)

def gem_art_reward(challenge_rating, treasure):
    die = d100()
    if 0 <= challenge_rating <= 4:
        if 7 <= die <= 16:
            for _ in range(0, d6(2)):
                treasure['10'] += random.choice(gemstones[10])
    return treasure

#page 136
#TODO: get rid of num_of_monsters arg.
def treasure(challenge_rating = 0, num_of_monsters = 1, individual_or_hoard = ''):
    treasure = {'Copper' : 0,
                'Silver' : 0,
                'Electrum' : 0,
                'Gold' : 0,
                'Platinum' : 0}
    
    treasure = random_money_reward(int(challenge_rating), treasure, int(num_of_monsters), individual_or_hoard)

    if individual_or_hoard == 'hoard':
        treasure = gem_art_reward(int(challenge_rating), treasure) #fix

    if d100() <= 10:
        treasure['Trinket'] = random.choice(trinkets)
    print("")
    for coin_type, amount in treasure.items():
        print(f"{coin_type}: {amount}") 
    print("")

def trinket():
    print(random.choice(trinkets))

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
    treasure_parser.add_argument('num_of_monsters', nargs='?', default= 1, help='Parameter for the amount of monsters (with the same challenge rating), defaults to 1')
    treasure_parser.add_argument('individual_or_hoard', nargs='?', default= '', help='Specifying whether to roll from the individual treasure or treasure hoard charts, if not specified it will roll from individual treasure charts')
    
    trinket_parser = subparsers.add_parser('trinket')
    trinket_parser.description = 'Randomly picks a trinket from the trinket chart'

    args = parser.parse_args()
    
    # Call appropriate function based on arguments
    if args.function == 'npc':
        npc(args.race, args.gender, args.stat_block)
    elif args.function == 'treasure':
        treasure(args.challenge, args.num_of_monsters, args.individual_or_hoard)
    elif args.function == 'trinket':
        trinket()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()