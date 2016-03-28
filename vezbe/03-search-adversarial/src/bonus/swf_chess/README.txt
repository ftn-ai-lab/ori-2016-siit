Posto je en passant malo teze simulirati, potrebno je podesiti tablu na sljedeci nacin:
	

	Ukoliko se simulira da sljedeci potez ima bijeli igrac:
		1.Potrebno je zamijeniti default tablu na "../../chess/boards/board_en_passant_white.brd"(U pretposljednjem redu)
		2.U narednoj liniji treba simulirati da je prethodni potez crnog igraca bio pijun koji se nalazi na poziciji row=3 col=4
			dodavanje narednih linija(odmah ispod linije za podesavaje table)
			
			board.last_row = 3
			board.last_col = 3
			
		3. Kada se pokrene igra klikom na bijelog pijuna dobice se mogucnost da se klikne i na desno dijagonalno polje sto ce simulirati 
			en passant pomijeranjem bijelog pijuna na to polje i uklanjanjem crnog pijuna koji se nalazio desno od njega.

	Ukoliko se simulira da sljedeci potez ima crni igrac:
		1.Potrebno je podesiti dubinu algoritma na 1, da se ne bi desilo da zbog nekog boljeg poteza tokom predvidjanja
			pijun ode na drugu stranu. 
		2.Zatim je potrebno izmijeniti tablu da bude "../../chess/boards/board_en_passant_black.brd".
		3.Kada se pokrene igra, mogu se pomjeriti bijeli pijuni sa pozicije (row=6, col=0) ili (row=6, col=2) dva polja unaprijed i crni 
			igrac ce odigrati en passant.