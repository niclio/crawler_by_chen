def Print(a):
    return lambda:print(a)

def Lt(a,b):
    return lambda:a<b

def If(exp,a,b):
    if exp(): return a
    else: return b

def Pass():
    return lambda:None

def _Do(a, i):
    # print('a=', a, 'do:i=', i)
    If(Lt(i,len(a)), lambda:[a[i](), _Do(a, i+1)], Pass)()
    return Pass

def Do(a):
    return _Do(a, 0)

def Push(a, x):
    return lambda:a.append(x)

def _Range(start, end, step, a):
    print(f'_Range({start},{end})')
    If(Lt(start, end), lambda:[Push(a,start)(), _Range(start+step, end, step, a)], Pass)()
    return Pass

def Range(start, end, step=1):
    a = []
    print('a=', a, 'step=', step)
    _Range(start, end, step, a)
    print('range:a=',a)
    return lambda:a

'''
def _Each(a, f, i):
    If(Lt(i, len(a)), [a[i]()
    _Each(a, f, i+1)
    return Pass

def Each(a, f):
    return _Each(a, f, 0)
    

def Map(a, f):
    r = []
    for x in a:
        r.append(f(x))
    return r

def filter(a, f):
    r = []
    for x in a:
        if f(x): r.append(x)
    return r

def reduce(a, f, init):
    r = init
    for x in a:
        r = f(r, x)
    return r
'''

if __name__=="__main__":
    Do([Print("step1"), Print("step2")])
    a, b = 1, 2
    Do([If(Lt(a,b), Print("a<b"), Print("a>=b"))])
    # Print("hello")()
    # Print("world")()
    # Do([Print("job1"), Print("job2")])
    # Range(1, 2)
    Do([Range(1, 5)])
    '''
    print(map([1,2,3,4,5], lambda x:x*x))
    print(filter([1,2,3,4,5], lambda x:x%2==1))
    print(reduce([1,2,3,4,5], lambda x,y:x+y, 0))
    '''

