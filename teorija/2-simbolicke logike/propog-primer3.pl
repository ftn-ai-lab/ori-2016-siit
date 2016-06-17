izvod(x, 1).
izvod(x^N, N*x^N1):-integer(N), N>1, N1 is N-1.
izvod(N, 0):-integer(N).
:-op(200, yfx, ^). 

izvod(U^N, N*U^N1*Du):-integer(N), not(N=0), N1 is N-1, izvod(U, Du). 
izvod(U+V, Du+Dv):-izvod(U, Du), izvod(V, Dv).
izvod(U*V, Du*V+U*Dv):-izvod(U, Du), izvod(V, Dv).


integral(U, V):-izvod(V, U).