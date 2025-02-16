import random

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