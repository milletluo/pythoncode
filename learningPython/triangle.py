def Triangle():
    L=[1]
    while True:
        yield(L)
        L.append(0)
        L=[L[i-1]+L[i] for i in range(len(L))]

n=0
for t in Triangle():
    print(t)
    n=n+1
    if n==10:
        break
