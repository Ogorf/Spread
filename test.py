import math

def angle(p):
    angle = math.acos(p[0]/math.sqrt(p[0]**2+p[1]**2))*180/math.pi
    if p[1] < 0:
        return 360-angle
    else:
        return angle

for p in [(1, 1), (0, 1), (-1, 0), (-1, -1), (0, -1)]:
    print(p, angle(p))
