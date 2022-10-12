# https://medium.com/@adambene/fixed-point-combinators-in-javascript-c214c15ff2f6

Z = lambda g: lambda v: g(Z(g))(v)

sum = Z(
    lambda g: # g for self-referencing
        lambda _from:
            lambda _to:
                _to if _from == _to else _from + g(_from + 1)(_to) # step one and recurse
)

print('sum(5)(8)=', sum(5)(8))
