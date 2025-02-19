from dice import *
import math
from dnd_collections import (
    dwarf_names_male, dwarf_names_female,
    human_names_male, human_names_female,
    elf_names_male, elf_names_female,
    halfling_names_male, halfling_names_female,
    gnome_names_male, gnome_names_female
)

races = {
    "dwarf": {
        "speed": 25,
        "racial traits": ["Darkvision 60ft", "Resistance vs poison damage", "Advantage on saving throws vs poison"],
        "stats": {"STR": 2, "CON": 2},
        "perception": 10
    },
    "human": {
        "speed": 30,
        "racial traits": ["Versatile", "Adaptable"],
        "stats": {"STR": 1, "DEX": 1, "CON": 1, "INT": 1, "WIS": 1, "CHA": 1},
        "perception": 10
    },
    "elf": {
        "speed": 30,
        "racial traits": ["Darkvision 60ft", "Keen senses"],
        "stats": {"DEX": 2},
        "perception": 12
    },
    "halfling": {
        "speed": 25,
        "racial traits": ["Lucky", "Brave"],
        "stats": {"DEX": 2},
        "perception": 10
    },
    "gnome": {
        "speed": 25,
        "racial traits": ["Gnome Cunning"],
        "stats": {"INT": 2},
        "perception": 10
    }
}

stat_blocks = {
    "bandit": {
        "ac": 12,
        "hp": lambda: max(d8(2) + 2, 10),
        "melee weapon": [
            "Scimitar (+3 to hit, 5ft range, 1d6 + 1 slashing damage)",
            "Shortsword (+3 to hit, 5ft range, 1d6 + 1 slashing damage)",
            "Handaxe (+3 to hit, 5ft range, 1d6 + 1 slashing damage, thrown (20/60))"
        ],
        "ranged weapon": [
            "Light crossbow (+3 to hit, 80/320ft range, 1d8 + 1 piercing damage)"
        ],
        "stats": {"STR": 1, "DEX": 2, "CON": 2},
        "challenge": "1/8 (25 XP)",
        "perception": 10
    },
    "commoner": {
        "ac": 10,
        "hp": lambda: max(d8(), 4),
        "melee weapon": [
            "Club (+2 to hit, 5ft range, 1d4 bludgeoning damage)",
            "Dagger (+2 to hit, 5ft range, 1d4 piercing damage, thrown (20/60))"
        ],
        "ranged weapon": [],
        "stats": {},
        "challenge": "0 (10 XP)",
        "perception": 10
    },
    "acolyte": {
        "ac": 10,
        "hp": lambda: max(d8(2), 9),
        "melee weapon": [
            "Club (+2 to hit, 5ft range, 1d4 bludgeoning damage)"
        ],
        "ranged weapon": [],
        "stats": {"WIS": 4, "CHA": 1},
        "challenge": "1/4 (50 XP)",
        "perception": 12,
        "spells": [
            "Spellcasting: Wisdom. Spell Save DC: 12. +4 to hit.",
            "Cantrips: light, sacred flame, thaumaturgy.",
            "1st level (3 slots): bless, cure wounds, sanctuary"
        ]
    },
    "cultist": {
        "ac": 12,
        "hp": lambda: max(d8(2), 9),
        "melee weapon": [
            "Scimitar (+3 to hit, 5ft range, 1d6 + 1 slashing damage)"
        ],
        "ranged weapon": [],
        "stats": {"DEX": 2},
        "challenge": "1/8 (25 XP)",
        "perception": 10,
        "traits": ["Dark Devotion: Saving throws vs charmed or frightened"]
    },
    "guard": {
        "ac": 16,
        "hp": lambda: max(d8(2) + 2, 11),
        "melee weapon": [
            "Spear (+3 to hit, 5ft range, thrown (20/60 ft), 1d6 + 1 piercing damage or 1d8 + 1 if two-handed)"
        ],
        "ranged weapon": [],
        "stats": {"STR": 3, "DEX": 2, "CON": 2},
        "challenge": "1/8 (25 XP)",
        "perception": 12
    }
}

class NPC:
    def __init__(self, race='', gender='', stat_block=''):
        """
        Initialize an NPC with a specified or randomly chosen race, gender, and stat block.

        Parameters:
            race (str, optional): The NPC's race. If empty, a random race is selected from available options.
            gender (str, optional): The NPC's gender ("male" or "female"). Randomly chosen if not provided.
            stat_block (str, optional): Identifier for the NPC's stat block. Randomly selected if empty.

        Raises:
            ValueError: If an invalid race, gender, or stat block is provided.

        The NPC is created with base stats of 10, modified by bonuses from the chosen race and stat block.
        Additional attributes such as AC, HP, speed, perception, weapons, traits, spells, and a generated name
        are also set.
        """
        if not race:
            self.race = random.choice(list(races.keys()))
        else:
            if race.lower() not in races:
                raise ValueError(f"Race '{race}' not recognized. Valid races: {list(races.keys())}")
            self.race = race.lower()

        if not gender:
            self.gender = random.choice(["male", "female"])
        else:
            if gender.lower() not in ["male", "female"]:
                raise ValueError("Gender must be 'male' or 'female'.")
            self.gender = gender.lower()

        if not stat_block:
            self.stat_block = random.choice(list(stat_blocks.keys()))
        else:
            if stat_block.lower() not in stat_blocks:
                raise ValueError(f"Stat block '{stat_block}' not recognized. Valid stat blocks: {list(stat_blocks.keys())}")
            self.stat_block = stat_block.lower()

        self.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        
        race_bonus = races[self.race].get("stats", {})
        for stat, bonus in race_bonus.items():
            self.stats[stat] += bonus

        stat_block_bonus = stat_blocks[self.stat_block].get("stats", {})
        for stat, bonus in stat_block_bonus.items():
            self.stats[stat] += bonus

        self.ac = stat_blocks[self.stat_block]["ac"]
        hp_value = stat_blocks[self.stat_block]["hp"]
        self.hp = hp_value() if callable(hp_value) else hp_value
        self.speed = races[self.race]["speed"]

        if "perception" in stat_blocks[self.stat_block]:
            self.perception = stat_blocks[self.stat_block]["perception"]
        elif "perception" in races[self.race]:
            self.perception = races[self.race]["perception"]
        else:
            self.perception = 10

        melee_weapons = stat_blocks[self.stat_block].get("melee weapon", [])
        self.weapon = random.choice(melee_weapons) if melee_weapons else ""
        
        ranged_weapons = stat_blocks[self.stat_block].get("ranged weapon", [])
        self.ranged_weapon = random.choice(ranged_weapons) if ranged_weapons else ""
        self.challenge = stat_blocks[self.stat_block]["challenge"]

        self.traits = []
        self.traits.extend(races[self.race].get("racial traits", []))
        self.traits.extend(stat_blocks[self.stat_block].get("traits", []))

        self.spells = stat_blocks[self.stat_block].get("spells", [])

        self.name = self.generate_name()

    def rand_name(self, names):
        """
        Generate a random name from a list of name parts.

        Args:
            names (list): List of lists of name parts. If the list has more than two elements, 
                the function will randomly decide whether to use a two- or three-part name.

        Returns:
            str: A randomly generated name.
        """
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

    def generate_name(self):
        """
        Generate a name for the NPC based on its race and gender.

        Parameters
        ----------
        None

        Returns
        -------
        str
            The name of the NPC.
        """
        if self.race == "dwarf":
            return self.rand_name(dwarf_names_male) if self.gender == "male" else self.rand_name(dwarf_names_female)
        elif self.race == "human":
            return self.rand_name(human_names_male) if self.gender == "male" else self.rand_name(human_names_female)
        elif self.race == "elf":
            return self.rand_name(elf_names_male) if self.gender == "male" else self.rand_name(elf_names_female)
        elif self.race == "halfling":
            return self.rand_name(halfling_names_male) if self.gender == "male" else self.rand_name(halfling_names_female)
        elif self.race == "gnome":
            return self.rand_name(gnome_names_male) if self.gender == "male" else self.rand_name(gnome_names_female)
        return "Unnamed NPC"
    
    def get_mod(self, stat):
        """
        Calculates the ability score modifier for a given stat.

        Args:
            stat (int): The ability score for which the modifier is calculated.

        Returns:
            str: The formatted modifier as a string, enclosed in parentheses.
        """

        modifier = math.floor((stat - 10) / 2)
        sign = '+' if modifier>=0 else ''
        return f"({sign}{modifier})"
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        """
        Returns a string representation of the NPC's stats and details.
        """

        details = f"\nNPC: {self.name}\n"
        details += f"Race: {self.race.title()}, Gender: {self.gender.title()}, Stat Block: {self.stat_block.title()}\n"
        details += "Stats: " + ", ".join(f"{stat}: {value} {self.get_mod(value)}" for stat, value in self.stats.items()) + "\n"
        details += f"AC: {self.ac}, HP: {self.hp}, Speed: {self.speed}, Perception: {self.perception}\n"
        details += f"Weapon: {self.weapon}\n"
        details += f"Ranged Weapon: {self.ranged_weapon}\n"
        details += f"Challenge: {self.challenge}\n"
        if self.traits:
            details += "Traits: " + ", ".join(self.traits) + "\n"
        if self.spells:
            details += "Spells: " + " ".join(self.spells) + "\n"
        return details
