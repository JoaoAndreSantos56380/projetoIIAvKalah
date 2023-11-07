# Coisas

KalahState ✅
	Attributos
		KalahState(fairkalah_state_index, other = (proximo_a_jogar, listaSementes))
			fairkalah_state_index: -1 se for o tabuleiro por omissão, 0 aleatório justo, ou índice [1, 254]
		to_move: que é o próximo (0 SUL, 1 NORTE)
		pass_turn: se passa a vez ou não (True/False)
		state: lista com número de sementes nos poços e kalahs, pela ordem anti-horária a começar pelo fundo à esquerda. Por exemplo: [4, 4, 5, 4, 3, 4, 0, 4, 4, 4, 4, 4, 4, 0]
	Métodos
		get_legal_moves
		is_game_over
		result: determina o resultado de um jogo finalizado (-1 NORTE, 0 empate, +1 SUL)
		real_move: gera um novo estado dada uma acção

Acções: lista de índices das sementes que queremos distribuir (ou -1 se passarmos)

Kalah ✅
	actions
	result
	terminal_test
	utility: -1 SUL, 0 empate, +1 NORTE
	display

Jogador
	Attributos
		nome
		fun ✅
	Métodos
		display

Jogador Aleatório
Jogador Alfabeta Minimax
Jogador El Caos Inteligente
Chapiteau

Função que realiza um jogo entre 2 jogadores

Função que realiza N pares de jogos (N/2 a SUL e N/2 a NORTE)

Função para realizar um torneio entre vários jogadores
