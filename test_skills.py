from spread_classes import fight

def test_fight():
    assert int(100-int((1+0.1)*90)) == 1
    attackers = [100, 110, 90, 91, 100, 100, 100]
    defenders = [100, 100, 100, 100, 101, 109, 90]
    result = [(-9, 9), (-19, 0), (1, 18), (0, 17), (-8, 10), (0, 18), (-18, -1)]
    for i in range(0, len(attackers)):
        for (j, attack_modifier) in enumerate([0.1, -0.1]):
            assert fight(attackers[i], defenders[i], attack_modifier) == result[i][j]
