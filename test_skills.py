from time import *
from SpreadClasses import *
import SkillTree

pygame.init()
pygame.display.set_mode((800, 600))

skilltree = SkillTree.empty()
p0 = Player("0", dim_grey, grey, light_grey, 0.03, 20)
p1 = Player("1", maroon, brown, peru, 0.12, 30)
p2 = Player("2", olive, yellow_green, yellow, 0.4, 70)

# c0 = Cell((100, 100), 50, p0, 50)
# c1 = Cell((200, 100), 60, p1, 100)
# c2 = Cell((400, 200), 100, p2, 100)
# c3 = Cell((600, 300), 80, p0, 100)


def create_test_cells(amount: int, p: Player, pop=100):
    result = []
    for i in range(0, amount):
        result += [Cell((i*200, i*100), 1000, p, pop)]
    return result


def create_test_bubbles(amount: int, p: Player, pop = 10000):
    result = []
    c = create_test_cells(1, p)[0]
    for i in range(0, amount):
        time = pygame.time.get_ticks()
        b = Bubble((0, 0), c, time)
        b.population = pop
        result += [b]
    return result


def test_fight():
    # create_test_cells(1, p0)
    attackers = [100, 110, 90, 91, 100, 100, 100]
    defenders = [100, 100, 100, 100, 101, 109, 90]
    result = [(-9, 9), (-19, 0), (1, 18), (0, 17), (-8, 10), (0, 18), (-18, -1)]
    for i in range(0, len(attackers)):
        for (j, attack_modifier) in enumerate([0.1, -0.1]):
            assert fight(attackers[i], defenders[i], attack_modifier) == result[i][j]

def test_fight_bubbles():
    b1 = create_test_bubbles(1, p0, 1000)[0]
    b2 = create_test_bubbles(1, p1, 300)[0]
    new_b = b1.collide_with_bubble(b2)
    assert b1.population == 700
    assert new_b == b1

#from AttackSkill import *
import AttackSkill as AS
def test_base():
    p = Player("W", olive, yellow_green, yellow, 0.4, 70)
    value_list = [(0.2,), (0.3,)]
    for value in value_list:
        perk = AS.Base([value])
        assert perk.values == [value]
        assert value[0] == perk.values[0][0]
        perk.level_up()
        assert perk.attack_modifier(None) == value[0]
        skilltree = SkillTree.SkillTree([AS.AttackSkill([perk])])
        p.skilltree = skilltree
        #assert p.attack_modifier(None) == value[0]


def test_rage():
    p = Player("W", olive, yellow_green, yellow, 0.4, 70)
    value_list = [(0.3, 0.2), (0.2, 0.1)]
    for time, value in value_list:
        perk = AS.Rage([(time, value)])
        perk.level_up()
        skilltree = SkillTree.SkillTree([AS.AttackSkill([perk])])
        p.skilltree = skilltree
        pcells = create_test_cells(1, p, 1)
        a_bubbles = create_test_bubbles(1, p0, 10)
        for cell, bubble in zip(pcells, a_bubbles):
            bubble.collide_with_cell(cell)
        b = create_test_bubbles(1, p)[0]
        assert p.attack_modifier(b) == value
        sleep(time/2)
        assert p.attack_modifier(b) == value
        sleep(time)
        assert p.attack_modifier(b) == 0

def test_berserker():
    p = Player("W", olive, yellow_green, yellow, 0.4, 70)
    value_list = [(0.3, 0.2), (0.2, 0.1)]
    for time, value in value_list:
        p.clear_action_tracker()
        perk = AS.Berserker([(time, value)])
        perk.level_up()
        skilltree = SkillTree.SkillTree([AS.AttackSkill([perk])])
        p.skilltree = skilltree
        pcells = create_test_cells(2, p)
        b1 = pcells[0].attack((0, 0))
        assert p.attack_modifier(b1) == value*0
        sleep(time/3)
        b2 = pcells[0].attack((0, 0))
        assert p.attack_modifier(b1) == value*0
        assert p.attack_modifier(b2) == value*1
        sleep(time/2)
        b3 = pcells[0].attack((0, 0))
        assert p.attack_modifier(b1) == value*0
        assert p.attack_modifier(b2) == value*1
        assert p.attack_modifier(b3) == value*2
        sleep(time/3)
        b4 = pcells[0].attack((0, 0))
        assert p.attack_modifier(b4) == value*2

def test_slavery():
    p = Player("W", olive, yellow_green, yellow, 0.4, 70)
    value_list = [[(10,)], [(20,)]]
    for value in value_list:
        perk = AS.Slavery(value)
        perk.level_up()
        skilltree = SkillTree.SkillTree([AS.AttackSkill([perk])])
        p.skilltree = skilltree
        c = create_test_cells(1, p1)[0]
        old_pop = c.population
        c.switch_player(p)
        assert old_pop+value[0][0] == c.population

import InfectionSkill as IS
def test_infection_base():
    p = Player("W", olive, yellow_green, yellow, 0.4, 70)
    value_list = [(500,), (300,)]
    for value in value_list:
        perk = IS.Base([value])
        perk.level_up()
        skilltree = SkillTree.SkillTree([IS.InfectionSkill([perk])])
        p.skilltree = skilltree
        c = create_test_cells(1, p1, 1000)[0]
        c.population = 1000
        b = create_test_bubbles(1, p, 150)[0]
        time = pygame.time.get_ticks()
        b.collide_with_cell(c)
        old_pop = c.population
        alpha = 50000/c.radius
        c.grow(2*alpha, pygame.time.get_ticks())
        assert old_pop == c.population
        #assert time == 0
        sleep(140/value[0])
        c.grow(c.cycle_interval, pygame.time.get_ticks())
        assert old_pop == c.population
        sleep(10/value[0])
        c.grow(c.cycle_interval, pygame.time.get_ticks())
        assert old_pop != c.population
