def Range(start, end, step=1):
    return list(range(start, end, step))

def If(exp, a, b):
    if exp(): return a()
    else: return b()

def Each(a, f):
    for x in a:
        f(x)

def Map(a, f):
    r = []
    for x in a:
        r.append(f(x))
    return r

def Filter(a, f):
    r = []
    for x in a:
        if f(x): r.append(x)
    return r

def Reduce(a, f, init):
    r = init
    for x in a:
        r = f(r, x)
    return r

a = range(1,5)
Each(a, lambda x:print(x))
Each(a, lambda x:If(lambda:x%2==0, lambda:print(x), lambda:None))
print(Map(a, lambda x:x*x))
print(Filter(a, lambda x:x%2==1))
print(Reduce(a, lambda x,y:x+y, 0))
