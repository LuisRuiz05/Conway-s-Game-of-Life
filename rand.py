import random

# This program generates random cell inputs.
for p in range(650):
    y = random.randint(0,63)
    x = random.randint(0,63)
    print(str(y)+" "+str(x))