# https://medium.com/@adambene/fixed-point-combinators-in-javascript-c214c15ff2f6

Z = lambda g: lambda v: g(Z(g))(v) # Z(g)(v) = g(Z(g))(v)
# 也就是 Z(g) = g(Z(g))

sum = Z( # sum(v) = Z(g)(v) = g(Z(g))(v) = g(sum)(v)
         #     v 代 _from                         v 代 _from+1 ....
    lambda g: # g for self-referencing
        lambda _from:
            lambda _to:
                _to if _from == _to else _from + sum(_from + 1)(_to) # step one and recurse
)

print('sum(5)(8)=', sum(5)(8))
