If = lambda cond, a, b: a if cond else b
Max = lambda a,b: If(a>b, a, b)
Min = lambda a,b: If(a<b, a, b)

Fibonacci = lambda n: If(n<2, n, Fibonacci(n-1)+Fibonacci(n-2))

print('Max(3,5)=', Max(3,5))
print('Min(3,5)=', Min(3,5))
print('Fibonacci(8)=', Fibonacci(8))

