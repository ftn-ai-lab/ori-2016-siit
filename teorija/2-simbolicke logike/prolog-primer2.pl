roditelj(X, Y):-otac(X, Y).
roditelj(X, Y):-majka(X, Y).

predak(X, Y):-roditelj(X, Y).
predak(X, Y):-roditelj(X, Z), predak(Z, Y).