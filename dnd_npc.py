from dice import *

races = {
    "dwarf" : {
        "speed" : 25,
        "racial traits" : ["Darkvision 60ft", "Resistance vs poison damage", "Advantage on saving throws vs poison"],
        "stats" : {
            "STR" : 2,
            "CON" : 2
        }
    }
}

stat_blocks = {
    "bandit" : {
        "ac" : 12,
        "hp" : max((d8(2) + 2), 10),
        "melee weapon" : [],
        "ranged weapon" : [],
        "stats" : {
            "STR" : 1,
            "DEX" : 2,
            "CON" : 2
        },
        "challenge" : "1/8, 25 XP"
    }
}

class NPC:

    def __init__(self, race='', gender='', stat_block=''):
        self.stats = {
            "STR" : 10,
            "DEX" : 10,
            "CON" : 10,
            "INT" : 10,
            "WIS" : 10,
            "CHA" : 10
        }
        self.ac = 10
        self.hp = 10
        self.speed = 30
        self.perception = 10
        self.weapon = ''
        self.ranged_weapon = ''
        self.challenge = ''
        self.traits = []
        self.spells = []