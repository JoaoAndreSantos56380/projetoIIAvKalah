from kalah import *

scores={'Vitoria': 3, 'Empate': 1}

def torneio(n, jogadores, jogo_id=0):
		jogo=Kalah(jogo_id)  # jogo gerado ao calha entre os "justos"
		tabela={}
		for i in range(len(jogadores)-1):
			jog1=jogadores[i]
			for j in range(i+1,len(jogadores)):
				jog2=jogadores[j]
				_,_,_,tabelaX = jogaNpares(jogo,n,jog1,jog2)
				incorpora(tabela,tabelaX)
		return tabela

def incorpora(tabela,tx):
	for jog in tx:
		if jog not in tabela:
			tabela[jog]=tx[jog]
		else:
			tabela[jog]+=tx[jog]

def jogaNpares(jogo,n,jog1,jog2):
	tabelaPrim={jog1.nome:0, jog2.nome:0, 'Empate':0}
	tabelaSeg={jog1.nome:0, jog2.nome:0, 'Empate':0}
	tabela={}
	for _ in range(n):
		_,_,vencedor=joga11(jogo,jog1,jog2)
		tabelaPrim[vencedor]+=1
		_,_,vencedor=joga11(jogo,jog2,jog1)
		tabelaSeg[vencedor]+=1
	for x in tabelaPrim:
		tabela[x]=tabelaPrim[x]+tabelaSeg[x]
	return tabelaPrim,tabelaSeg,tabela,traduzPontos(tabela)

def traduzPontos(tabela):
	tabelaScore={}
	empates=tabela['Empate']
	for x in tabela:
		if x != 'Empate':
			tabelaScore[x]=scores['Vitoria']*tabela[x]+empates
	return tabelaScore

def joga11(game, jog1, jog2, verbose=False):
		### jog1 e jog2 são jogadores com funções que dado um estado do jogo devolvem a jogada que escolheram
		### devolve o par de jogadores, a lista de jogadas e o resultado
		estado=game.initial
		proxjog = jog1
		lista_jogadas=[]
		lance = 0
		while not game.terminal_test(estado):
			if verbose:
				print('----------   LANCE:',lance)
				game.display(estado)
			jogada = proxjog.fun(game, estado)
			if verbose:
				print('JOGADA=',jogada)
			estado=game.result(estado,jogada)
			lista_jogadas.append(jogada)
			proxjog = jog2 if proxjog == jog1 else jog1
			lance+=1
		#p jogou e ganhou
		util=game.utility(estado,0)
		if util == 1:
			resultado=jog1.nome
		elif util== -1:
			resultado = jog2.nome
		else:
			resultado='Empate'
		return ((jog1.nome,jog2.nome),lista_jogadas,resultado)
