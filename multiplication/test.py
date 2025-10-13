
exact = 0
lastRounded = 0
while exact < 43:
    exact += 43 / 18.0
    rounded = round(exact)
    if(exact < 43):
        print((rounded - lastRounded), end=' + ')
    lastRounded = rounded
print()
print(exact)
