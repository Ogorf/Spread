a = [(4, 5, 2), (5, 6, 1)]
l1, *l2 = zip(*a)
l = list(zip(*a))
print("{}{}{}".format(*l))
a = [0.1, 0.2, 0.3]
b = list(zip(a))
print(b)
a = [(4, 5)]
l = list(zip(a))
print("{}".format(*l))

a = [(1,), (2,), (3,)]
b = list(zip(*a))
print(b)
#for touple in b:
#    print(touple)
#    print("/".join(list(map(lambda y: str(y), touple))))
c = map(lambda x: "/".join(list(map(lambda y: str(y), x))), b)

d = ["hi", "man"]
print("/".join(d))

a = [(1, 2), (4, 5)]
print(a)
b = list(zip(*a))
print(b)
c = map(lambda x: "/".join(list(map(lambda y: str(y), x))), b)
print("{}{}".format(*c))
