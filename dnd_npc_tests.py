import pytest
import random
from dnd_npc import NPC, races, stat_blocks

# Patch the d8 function in the dnd_npc module to return a fixed value.
# With this patch, d8(n) will return 4*n, so calculations like hp become predictable.
def fixed_d8(n=1):
    return 4 * n

@pytest.fixture(autouse=True)
def patch_d8(monkeypatch):
    monkeypatch.setattr('dnd_npc.d8', fixed_d8)

def test_valid_npc_dwarf_bandit():
    # Create an NPC with specific parameters.
    npc = NPC(race="dwarf", gender="male", stat_block="bandit")
    # Verify that the chosen properties are set correctly.
    assert npc.race == "dwarf"
    assert npc.gender == "male"
    assert npc.stat_block == "bandit"

    # Base stats are 10. For a dwarf, add bonus: {"STR": 2, "CON": 2}.
    # For a bandit stat block, bonus: {"STR": 1, "DEX": 2, "CON": 2}.
    # Expected final stats:
    #   STR: 10 + 2 + 1 = 13, DEX: 10 + 0 + 2 = 12, CON: 10 + 2 + 2 = 14,
    #   INT, WIS, CHA remain at 10.
    expected_stats = {
        "STR": 13,
        "DEX": 12,
        "CON": 14,
        "INT": 10,
        "WIS": 10,
        "CHA": 10
    }
    assert npc.stats == expected_stats

    # For bandit stat block: AC should be 12.
    assert npc.ac == 12

    # With our fixed d8, hp is calculated as:
    #   max(fixed_d8(2) + 2, 10) = max(8 + 2, 10) = 10.
    assert npc.hp == 10

    # Check that the race-determined speed is correct (dwarf speed is 25).
    assert npc.speed == 25

    # Perception for bandit is explicitly 10.
    assert npc.perception == 10

    # Challenge rating should match the stat block.
    assert npc.challenge == "1/8 (25 XP)"

    # Verify that a name is generated (and it isn’t the fallback "Unnamed NPC").
    assert isinstance(npc.name, str)
    assert npc.name != "Unnamed NPC"

    # Check that the string representation includes expected keywords.
    s = str(npc)
    assert "NPC:" in s
    assert "dwarf" in s.lower()

def test_invalid_race():
    # Provide an invalid race; expect a ValueError.
    with pytest.raises(ValueError) as excinfo:
        NPC(race="hmuan", gender="male", stat_block="bandit")
    assert "Race 'hmuan' not recognized" in str(excinfo.value)

def test_invalid_gender():
    # Provide an invalid gender; expect a ValueError.
    with pytest.raises(ValueError) as excinfo:
        NPC(race="human", gender="unknown", stat_block="commoner")
    assert "Gender must be 'male' or 'female'." in str(excinfo.value)

def test_invalid_stat_block():
    # Provide an invalid stat block; expect a ValueError.
    with pytest.raises(ValueError) as excinfo:
        NPC(race="human", gender="female", stat_block="wizard")
    assert "Stat block 'wizard' not recognized" in str(excinfo.value)

def test_default_values():
    # If no arguments are provided, NPC should randomly choose valid defaults.
    npc = NPC()
    assert npc.race in races
    assert npc.gender in ["male", "female"]
    assert npc.stat_block in stat_blocks
    # Ensure a generated name exists.
    assert npc.name != "Unnamed NPC"

def test_generate_name():
    # Test the name-generation separately.
    npc = NPC(race="elf", gender="female", stat_block="acolyte")
    name = npc.generate_name()
    assert isinstance(name, str)
    assert name != "Unnamed NPC"

def test_repr_equals_str():
    # __repr__ should equal __str__.
    npc = NPC(race="halfling", gender="female", stat_block="cultist")
    assert repr(npc) == str(npc)

def test_spells_for_acolyte():
    # For an NPC with the acolyte stat block, verify that spells are assigned.
    npc = NPC(race="human", gender="male", stat_block="acolyte")
    assert len(npc.spells) > 0

def test_ranged_weapon_empty_for_acolyte():
    # The acolyte stat block does not include a ranged weapon.
    npc = NPC(race="human", gender="male", stat_block="acolyte")
    assert npc.ranged_weapon == ""

def test_traits_combined():
    # For a human cultist, traits should combine both racial traits and the stat block traits.
    npc = NPC(race="human", gender="female", stat_block="cultist")
    for trait in ["Versatile", "Adaptable", "Dark Devotion: Saving throws vs charmed or frightened"]:
        assert trait in npc.traits

def test_get_mod_calculation():
    # Create a dummy NPC (any valid parameters) so we can call get_mod.
    npc = NPC(race="human", gender="male", stat_block="commoner")
    # Test various stat values.
    assert npc.get_mod(10) == "(+0)"
    assert npc.get_mod(11) == "(+0)"  # floor((11-10)/2) = floor(0.5) = 0
    assert npc.get_mod(12) == "(+1)"  # floor((12-10)/2) = 1
    assert npc.get_mod(8)  == "(-1)"  # floor((8-10)/2)  = -1
    assert npc.get_mod(9)  == "(-1)"  # floor((9-10)/2)  = -1

def test_str_includes_modifiers():
    # Create a dwarf bandit NPC.
    # Calculation details:
    # Base stats: all 10.
    # Dwarf bonus: {STR: +2, CON: +2} and bandit bonus: {STR: +1, DEX: +2, CON: +2}
    # => Final stats: STR: 10+2+1 = 13, DEX: 10+0+2 = 12, CON: 10+2+2 = 14,
    # INT, WIS, CHA remain 10.
    npc = NPC(race="dwarf", gender="male", stat_block="bandit")
    s = str(npc)
    
    # Check that each stat and its computed modifier appear in the string.
    assert "STR: 13 (+1)" in s  # 13 -> modifier = floor((13-10)/2)=1
    assert "DEX: 12 (+1)" in s  # 12 -> modifier = 1
    assert "CON: 14 (+2)" in s  # 14 -> modifier = 2
    assert "INT: 10 (+0)" in s
    assert "WIS: 10 (+0)" in s
    assert "CHA: 10 (+0)" in s

def test_str_format():
    # Create an NPC and verify that the string representation contains key sections.
    npc = NPC(race="elf", gender="female", stat_block="acolyte")
    output = str(npc)
    # Check for presence of NPC name, race, stat block and stats with modifiers.
    assert "NPC:" in output
    assert "Elf" in output
    assert "Acolyte" in output
    # Ensure each stat is printed with its value and modifier.
    for stat in ["STR", "DEX", "CON", "INT", "WIS", "CHA"]:
        assert stat + ":" in output
        # Check that a modifier (e.g. "(+0)" or similar) appears after the stat value.
        assert "(" in output and ")" in output
