element(X, [X|_]).
element(X, [Y|R]):-element(X, R).

spoji([], X, X).
spoji([G|R], Y, [G|Z]):-
                    spoji(R, Y, Z).


brisi(X, [X|R], R).
brisi(X, [Y|R], [Y|T]):-
                    brisi(X, R, T).

dodaj(X, L, Rez):-brisi(X, Rez, L).

permutacija([], []).
permutacija([G|R], T):-
    permutacija(R, PR),
    dodaj(G, PR, T).

uredjena([]).
uredjena([X]).
uredjena([X|[Y|R]]):-X<Y,
                   uredjena([Y|R]).

sortiraj(L, R):-permutacija(L, R),
                 uredjena(R).
