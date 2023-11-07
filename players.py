import sys
from kalah import *

### Player Utils ###

def opposite_well(state, index):
	if index == 6:
		return state[13]
	if index == 13:
		return state[6]
	return state[12-index]

def opposite_well_index(state, index):
	if index == 6:
		return 13
	if index == 13:
		return 6
	return 12-index

### Player Classes ###

class Jogador():
	def __init__(self, nome, fun):
		self.nome = nome
		self.fun = fun
	def display(self):
		print(self.nome+" ")

class JogadorAlfaBeta(Jogador):
	def __init__(self, nome, depth, fun_eval):
		self.nome = nome
		self.fun = lambda game, state: alphabeta_cutoff_search_new(state,game,depth,eval_fn=fun_eval)


### Players ###

def possible_pass_better(estado, jogador):
	pits = 6
	thefts = 0
	i = pits
	if jogador == estado.SOUTH:
		for pit in range(pits):
			if estado.state[pit] == i:
				thefts += 1
			i -= 1
	else :
		for pit in range(7,14):
			if estado.state[pit] == i:
				thefts += 1
			i -= 1
	return thefts

def stolen_seeds_better(estado, jogador):
	stolen_seeds = []
	if jogador == estado.SOUTH:
		start_well = 0
		end_well = (len(estado.state)//2)-2
	else:
		start_well = 7
		end_well = len(estado.state)-2
	for i in range(start_well, end_well):
		if estado.state[i] > 0 and i+estado.state[i] <= end_well and estado.state[i+estado.state[i]] == 0:
			seeds_in_opposite_well = opposite_well(estado.state, i+estado.state[i])
			if seeds_in_opposite_well > 0:
				stolen_seeds.append(1 + seeds_in_opposite_well)
	stolen_seeds.sort()
	return stolen_seeds

def stolen_seeds_dando_a_volta(estado, jogador):
	#entre 13 e 18
	#ver se alterar pass vale a pena
	stolen_seeds = []
	if jogador == estado.SOUTH:
		start_well = 0
		end_well = (len(estado.state)//2)-2
	else:
		start_well = 7
		end_well = len(estado.state)-2
	for i in range(start_well, end_well):
		if estado.state[i] > 0 and ((i + estado.state[i] <= end_well and estado.state[i+estado.state[i]] == 0) or ( (i + estado.state[i])%13 - 1 <= end_well and estado.state[(i+estado.state[i])%13 - 1] == 0 ) and estado.state[i]>7):
			seeds_in_opposite_well = opposite_well(estado.state, i+estado.state[i])
			if seeds_in_opposite_well > 0:
				stolen_seeds.append(1 + seeds_in_opposite_well)
	stolen_seeds.sort()
	return stolen_seeds

def steal_seeds_better(estado, jogador):
	score = 0
	if estado.pass_turn:
		if jogador == estado.SOUTH:
			score -= estado.state[13]
		else:
			score -= estado.state[6]
	#if jogador == estado.to_move:
	if estado.is_game_over():
		return estado.result()*10000
	#maixmizar povos meus vazios com pocos adversarios cheios
	#score -= len(max_holes(estado, jogador))
	#print(estado)
	score += (possible_pass_better(estado, jogador) - possible_pass_adversary(estado,jogador)) * 2
	score += (estado.state[6] - estado.state[13]) * (sys.maxsize - 48)
	stolen_seeds_list = stolen_seeds_better(estado, jogador)
	#stolen_seeds_list = stolen_seeds_dando_a_volta(estado, jogador)
	stolen_seeds_num = 0
	if(len(stolen_seeds_list) > 0):
		stolen_seeds_num = stolen_seeds_list[-1] + len(stolen_seeds_list)
	score += stolen_seeds_num
	return score if jogador == estado.SOUTH else (-score)
	#else:
	#	return 0

class StealSeedsBetter(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, steal_seeds_better)





# Heuristics
def winner(estado):
	if estado.is_game_over():
		return estado.result()*1000
	return 0

def owned_seeds(estado, jogador):
	return sum(estado.state[0:7]) if jogador == estado.SOUTH else sum(estado.state[7:])

def won_seeds(estado, jogador):
	return estado.state[6] if jogador == estado.SOUTH else estado.state[13]

def won_seeds_diff(estado):
	return (estado.state[6] - estado.state[13])*3

def stolen_seeds(estado, jogador):
	#posso roubar sementes ao dar uma volta ao "tabuleiro". verificar se isso acontece
	stolen_seeds = []
	if jogador == estado.SOUTH:
		start_well = 0
		end_well = (len(estado.state)//2)-2
	else:
		start_well = 7
		end_well = len(estado.state)-2
	for i in range(start_well, end_well):
		if estado.state[i] > 0 and i+estado.state[i] <= end_well and estado.state[i+estado.state[i]] == 0:
			seeds_in_opposite_well = opposite_well(estado.state, i+estado.state[i])
			if seeds_in_opposite_well > 0:
				stolen_seeds.append(1 + seeds_in_opposite_well)
	stolen_seeds.sort()
	return stolen_seeds

def possible_pass(estado, jogador):
	pits = 6
	thefts = 0
	i = pits
	if jogador == estado.SOUTH:
		for pit in range(pits):
			if estado.state[pit] == i:
				thefts += 1
			i -= 1
	else :
		for pit in range(7,14):
			if estado.state[pit] == i:
				thefts += 1
			i -= 1
	return thefts

def possible_pass_adversary(estado, jogador):
	#contabilizar passings do adversario
	adv_passings = 0
	pits = 6
	i = pits
	if jogador == estado.SOUTH:
		i = pits
		for pit in range(7,13):
			if estado.state[pit] == i:
				adv_passings += 1
			i -= 1
	else:
		i = pits
		for pit in range(pits):
			if estado.state[pit] == i:
				adv_passings += 1
			i -= -1
	return adv_passings

def max_holes(estado, jogador):
	#contabilizar buracos do adv -> feito aparntemente
	adv_holes = 0
	holes = 0
	holes_list = []
	state = estado.state
	if jogador == estado.SOUTH:
		for i in range(0,6):
			if state[i] == 0 and opposite_well(state, i) > 0:
				holes_list.append(state[opposite_well_index(state, i)])
				holes += 1
			if state[opposite_well_index(state,i)] == 0 and state[i] > 0:
				adv_holes += 1
	else:
		for i in range(7,13):
			if state[i] == 0 and opposite_well(state, i) > 0:
				holes_list.append(state[opposite_well_index(state, i)])
				holes +=1
			if state[opposite_well_index(state,i)] == 0 and state[i] > 0:
				adv_holes += 1
	holes_list.sort()
	if adv_holes > holes:
		return []
	return holes_list


# Jogadores
class JogadorAleat(Jogador):
	def __init__(self, nome):
		self.nome = nome
		self.fun = lambda game, state: random.choice(game.actions(state))

def chapiteau(estado, jogador):
	if estado.is_game_over():
		return estado.result()*100
	#print(estado)
	score = 0
	sum_s = sum(estado.state[:7])
	sum_n = sum(estado.state[7:])
	if jogador == estado.SOUTH:
		score = sum_s - sum_n
	else:
		score = sum_n - sum_s
	#score = abs(sum_s - sum_n)
	if jogador == estado.SOUTH:
		return score
	else:
		return (-score)
class Chapiteau(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, chapiteau)

def max_seeds(estado, jogador):
	if estado.is_game_over():
		return estado.result()*1000
	score = 0
	if jogador == estado.SOUTH:
		score += sum(estado.state[0:7])
	else:
		score += sum(estado.state[7:])
	if jogador == estado.SOUTH:
		return score
	else:
		return (-score)
class MaxSeeds(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, max_seeds)

def min_seeds(estado, jogador):
	if estado.is_game_over():
		return estado.result()*1000
	score = 0
	if jogador == estado.SOUTH:
		score += sum(estado.state[0:7])
	else:
		score += sum(estado.state[7:])
	if jogador == estado.SOUTH:
		return score
	else:
		return (-score)
class MinSeeds(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, min_seeds)

# Winner
def owned_seeds_fun(estado, jogador):
	win = winner(estado)
	if win != 0:
		return win
	score = owned_seeds(estado, jogador)
	return score if jogador == estado.SOUTH else (-score)
class OwnedSeeds(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, owned_seeds_fun)

# Lost to owned_seeds_fun
def won_seeds_fun(estado, jogador):
	win = winner(estado)
	if win != 0:
		return win
	score = won_seeds(estado, jogador)
	return score if jogador == estado.SOUTH else (-score)
class WonSeeds(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, won_seeds_fun)

# Lost to owned_seeds_fun
def owned_won_seeds_fun(estado, jogador):
	win = winner(estado)
	if win != 0:
		return win
	score = owned_seeds(estado, jogador)
	score += won_seeds(estado, jogador)
	return score if jogador == estado.SOUTH else (-score)
class OwnedWonSeeds(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, owned_won_seeds_fun)

# Lost to owned_seeds_fun
def possible_pass_fun(estado, jogador):
	win = winner(estado)
	if win != 0:
		return win
	score = possible_pass(estado, jogador)
	return score if jogador == estado.SOUTH else (-score)
class PossiblePass(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, possible_pass_fun)

# Lost to owned_seeds_fun
def owned_possible_pass(estado, jogador):
	win = winner(estado)
	if win != 0:
		return win
	score = owned_seeds(estado, jogador)
	score += possible_pass(estado, jogador)
	return score if jogador == estado.SOUTH else (-score)
class OwnedPossiblePass(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, owned_possible_pass)

def possible_pass_adversary_fun(estado, jogador):
	win = winner(estado)
	if win != 0:
		return win
	score = 0
	passings = possible_pass(estado, jogador)
	adv_passings = possible_pass_adversary(estado, jogador)
	if adv_passings > passings:
		score += -1
	else:
		score += passings
	return score if jogador == estado.SOUTH else (-score)
class PossiblePassAdversary(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, possible_pass_adversary_fun)

def owned_possible_pass_adversary_fun(estado, jogador):
	win = winner(estado)
	if win != 0:
		return win
	score = 0
	passings = possible_pass(estado, jogador)
	adv_passings = possible_pass_adversary(estado, jogador)
	if adv_passings > passings:
		score += -1
	else:
		score += passings
	return score if jogador == estado.SOUTH else (-score)
class OwnedPossiblePassAdversary(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, owned_possible_pass_adversary_fun)

def my_own_fun(estado, jogador):
	score = 0

	# Seed Count Evaluation
	player_seeds = sum(estado.state[:7]) if jogador == estado.SOUTH else sum(estado.state[7:])
	opponent_seeds = sum(estado.state[7:]) if jogador == estado.SOUTH else sum(estado.state[:7])

	# Prioritize capturing opportunities - Find moves that capture seeds
	for i in range(6):
		if estado.state[i] == 0:
			continue  # Skip empty pits
		if (estado.state[i] + i) % 13 < 6 and estado.state[(estado.state[i] + i) % 13] == 0:
			score += 3  # Reward capturing opportunities

	# Encourage strategic moves that lead to capturing seeds
	score += (player_seeds - opponent_seeds)

	return score
class MyOwn(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, my_own_fun)

def my_own_fun_v2(estado, jogador):
	score = 0

	# Seed Count Evaluation
	player_seeds = sum(estado.state[:7]) if jogador == estado.SOUTH else sum(estado.state[7:])
	opponent_seeds = sum(estado.state[7:]) if jogador == estado.SOUTH else sum(estado.state[:7])

	# Prioritize capturing opportunities - Find moves that capture seeds
	for i in range(6):
		if estado.state[i] == 0:
			continue  # Skip empty pits
		if (estado.state[i] + i) % 13 < 6 and estado.state[(estado.state[i] + i) % 13] == 0:
			score += 3  # Reward capturing opportunities

	# Encourage strategic moves that lead to capturing seeds
	score += (player_seeds - opponent_seeds)

	# Avoid dangerous moves - Analyze the consequences of moves
	for i in range(6):
		if estado.state[i] == 0:
			continue  # Skip empty pits

		# Simulate the move
		next_state = estado.state[:]
		seeds_to_sow = next_state[i]
		next_state[i] = 0

		index = i
		while seeds_to_sow > 0:
			index = (index + 1) % 14  # Move along the pits
			if (index != 6 and jogador == estado.SOUTH) or (index != 13 and jogador == estado.NORTH):
					next_state[index] += 1
					seeds_to_sow -= 1

		# Assess dangerous moves that can leave the opponent with a capturing opportunity
		if (next_state[index] == 1 and index != 6 and jogador == estado.SOUTH) or (next_state[index] == 1 and index != 13 and jogador == estado.NORTH):
			score -= 5  # Penalize dangerous moves

	return score
class MyOwnv2(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, my_own_fun_v2)

def my_own_fun_v3(estado, jogador):
	score = 0

	# Seed Count Evaluation
	player_seeds = sum(estado.state[:7]) if jogador == estado.SOUTH else sum(estado.state[7:])
	opponent_seeds = sum(estado.state[7:]) if jogador == estado.SOUTH else sum(estado.state[:7])

	# Prioritize capturing opportunities - Find moves that capture seeds
	for i in range(6):
		if estado.state[i] == 0:
			continue  # Skip empty pits
		if (estado.state[i] + i) % 13 < 6 and estado.state[(estado.state[i] + i) % 13] == 0:
			score += 3  # Reward capturing opportunities

	# Encourage strategic moves that lead to capturing seeds
	score += (player_seeds - opponent_seeds)

	# Avoid dangerous moves - Analyze the consequences of moves
	for i in range(6):
		if estado.state[i] == 0:
			continue  # Skip empty pits

		# Simulate the move
		next_state = estado.state[:]
		seeds_to_sow = next_state[i]
		next_state[i] = 0

		index = i
		while seeds_to_sow > 0:
			index = (index + 1) % 14  # Move along the pits
			if (index != 6 and jogador == estado.SOUTH) or (index != 13 and jogador == estado.NORTH):
					next_state[index] += 1
					seeds_to_sow -= 1

		# Assess dangerous moves that can leave the opponent with a capturing opportunity
		if (next_state[index] == 1 and index != 6 and jogador == estado.SOUTH) or (next_state[index] == 1 and index != 13 and jogador == estado.NORTH):
			score -= 5  # Penalize dangerous moves

	# Adjust the heuristic based on positional advantages
	if jogador == estado.SOUTH:
		for i in range(6):
			score += estado.state[i]  # Reward seeds in own pits
	else:
		for i in range(7, 13):
			score += estado.state[i]  # Reward seeds in own pits

	return score
class MyOwnv3(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, my_own_fun_v3)

def my_own_fun_v4(estado, jogador):
	# Favorable moves from the current state
	score = 0

	# Seed counts of the current player and the opponent
	player_seeds = sum(estado.state[:7]) if jogador == estado.SOUTH else sum(estado.state[7:])
	opponent_seeds = sum(estado.state[7:]) if jogador == estado.SOUTH else sum(estado.state[:7])

	# Encourage capturing opportunities
	for i in range(6):
		if estado.state[i] == 0:
			continue
		if (estado.state[i] + i) % 13 < 6 and estado.state[(estado.state[i] + i) % 13] == 0:
			score += 3  # Reward capturing opportunities

	# Assess the strategic position of seeds and prioritize moving them closer to the opponent's side
	for i in range(6):
		if estado.state[i] > 0:
			score += (6 - i) if jogador == estado.SOUTH else (13 - i)

	# Evaluate the number of captured seeds, favoring the player with a lower count of captured seeds
	if jogador == estado.SOUTH:
		score += (estado.state[6] - estado.state[13]) * 3
	else:
		score += (estado.state[13] - estado.state[6]) * 3

	# Adjust the heuristic based on the difference between the player and opponent seed counts
	score += (player_seeds - opponent_seeds)

	# Provide a final evaluation based on the game result
	if estado.is_game_over():
		return estado.result() * 1000

	return score if jogador == estado.SOUTH else -score
class MyOwnv4(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, my_own_fun_v4)

def my_own_fun_v5(estado, jogador):
	# Evaluation based on the game result
	if estado.is_game_over():
		return estado.result() * 100

	score = 0

	# Seed counts of the current player and the opponent
	player_seeds = sum(estado.state[:7]) if jogador == estado.SOUTH else sum(estado.state[7:])
	opponent_seeds = sum(estado.state[7:]) if jogador == estado.SOUTH else sum(estado.state[:7])

	# Encourage capturing opportunities
	for i in range(6):
		if estado.state[i] == 0:
			continue
		if (estado.state[i] + i) % 13 < 6 and estado.state[(estado.state[i] + i) % 13] == 0:
			score += 3  # Reward capturing opportunities

	# Evaluate the number of captured seeds, favoring the player with a lower count of captured seeds
	if jogador == estado.SOUTH:
		score += (estado.state[6] - estado.state[13]) * 3
	else:
		score += (estado.state[13] - estado.state[6]) * 3

	# Encourage strategic moves to empty player's pits
	for i in range(6):
		if estado.state[i] == 0:
			score += 1

	# Adjust the heuristic based on the difference between the player and opponent seed counts
	score += (player_seeds - opponent_seeds)

	# Promote a defensive stance by penalizing the opponent for pits near the player's Kalah
	if jogador == estado.SOUTH:
		score += sum([1 for i in range(6) if estado.state[i] == 1 and estado.state[12 - i] != 0])
	else:
		score += sum([1 for i in range(7, 13) if estado.state[i] == 1 and estado.state[12 - i] != 0])

	return score if jogador == estado.SOUTH else -score
class MyOwnv5(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, my_own_fun_v5)

def my_own_fun_v6(estado, jogador):
	# Account for game result and seed difference
	if estado.is_game_over():
		return estado.result() * 100

	# Evaluation based on the game result
	score = 0

	# Evaluate capturing opportunities
	for i in range(6):
		if estado.state[i] == 0:
			continue
		if (estado.state[i] + i) % 13 < 6 and estado.state[(estado.state[i] + i) % 13] == 0:
			score += 3  # Encourage capturing opportunities

	# Adjust score based on the number of captured seeds, favoring the player with fewer captures
	""" if jogador == estado.SOUTH:
		score += (estado.state[6] - estado.state[13]) * 3
	else:
		score += (estado.state[13] - estado.state[6]) * 3 """
	score += (estado.state[6] - estado.state[13]) * 3

	# Encourage strategic moves to empty player's pits
	if jogador == estado.SOUTH:
		for i in range(6):
			if estado.state[i] == 0:
				score += 1
	else:
		for i in range(7,14):
			if estado.state[i] == 0:
				score += 1

	# Penalize for opponent's pits near the player's Kalah, avoiding captures
	if jogador == estado.SOUTH:
		score += sum([1 for i in range(6) if estado.state[i] == 1 and estado.state[12 - i] != 0])
	else:
		score += sum([1 for i in range(7, 13) if estado.state[i] == 1 and estado.state[12 - i] != 0])

	player_seeds = sum(estado.state[:7]) if jogador == estado.SOUTH else sum(estado.state[7:])
	opponent_seeds = sum(estado.state[7:]) if jogador == estado.SOUTH else sum(estado.state[:7])
	score += (player_seeds - opponent_seeds)

	return score if jogador == estado.SOUTH else -score
class MyOwnv6(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, my_own_fun_v6)

def my_own_fun_v7(estado, jogador):
	if estado.is_game_over():
		return estado.result()*100
	score = possible_pass_better(estado, jogador)
	stolen_seeds_list = stolen_seeds_better(estado, jogador)
	stolen_seeds_num = 0
	if(len(stolen_seeds_list) > 0):
		stolen_seeds_num = stolen_seeds_list[-1] + len(stolen_seeds_list)
	score += stolen_seeds_num

	# Evaluate capturing opportunities
	if jogador == estado.SOUTH:
		for i in range(6):
			if estado.state[i] == 0:
				continue
			if (estado.state[i] + i) % 13 < 6 and estado.state[(estado.state[i] + i) % 13] == 0:
				score += 3  # Encourage capturing opportunities
	else:
		for i in range(7,14):
			if estado.state[i] == 0:
				continue
			if (estado.state[i] + i) % 13 < 6 and estado.state[(estado.state[i] + i) % 13] == 0:
				score += 3  # Encourage capturing opportunities
	# Adjust score based on the number of captured seeds, favoring the player with fewer captures
	score += (estado.state[6] - estado.state[13]) * 3

	# Encourage strategic moves to empty player's pits
	if jogador == estado.SOUTH:
		for i in range(6):
			if estado.state[i] == 0:
				score += 1

	# Penalize for opponent's pits near the player's Kalah, avoiding captures
	if jogador == estado.SOUTH:
		score += sum([1 for i in range(6) if estado.state[i] == 1 and estado.state[12 - i] != 0])
	else:
		score += sum([1 for i in range(7, 13) if estado.state[i] == 1 and estado.state[12 - i] != 0])

	return score if jogador == estado.SOUTH else (-score)
class MyOwnv7(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, my_own_fun_v7)


# Para testar
def steal_seeds_better_holes(estado, jogador):
	win = winner(estado)
	if win != 0:
		return win
	#tentar adicionar jogadas consecutivas
	state = estado.state
	score = 0
	#maixmizar povos meus vazios com pocos adversarios cheios
	passings = possible_pass(estado, jogador)
	adv_passings = possible_pass_adversary(estado, jogador)
	if adv_passings > passings:
		score += -1
	else:
		score += passings
	holes = max_holes(estado, jogador)
	""" if len(holes) > 0:
		score += holes[-1] + len(holes)
	else:
		score -= 1 """
	if jogador == estado.SOUTH:
		score += (state[6] - state[13]) * 3
	else:
		score += (state[13] - state[6]) * 3
	#score += (estado.state[6] - estado.state[13]) * 3
	stolen_seeds_list = stolen_seeds(estado, jogador)
	stolen_seeds_num = 0
	if(len(stolen_seeds_list) > 0):
		stolen_seeds_num = stolen_seeds_list[-1] + len(stolen_seeds_list)
	score += stolen_seeds_num
	return score if jogador == estado.SOUTH else (-score)
class StealSeedsBetterHoles(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, steal_seeds_better_holes)

def func_1408385(estado, jogador):
	kalah_index = 6 if jogador == estado.SOUTH else 13
	kalah_adv_index = 6 if jogador == estado.NORTH else 13
	# Verificar se há poços cujo número de sementes é igual à distância até um poço vazio
	stolen_seeds = []
	start_well = 0 if jogador == estado.SOUTH else 7
	end_well = (len(estado.state)//2)-2 if jogador == estado.SOUTH else  len(estado.state)-2
	#print(estado)
	for i in range(start_well, end_well):
		if estado.state[i] > 0 and i+estado.state[i] <= end_well+1 and estado.state[i+estado.state[i]] == 0:
			stolen_seeds.append(1+opposite_well(estado.state, i))
	stolen_seeds.sort()
	score = estado.state[kalah_index] - estado.state[kalah_adv_index] + (stolen_seeds[-1] if len(stolen_seeds) > 0 else 0)
	#print("Score:",score)
	return score

def decprof(estado,jogador):
    ret = 0
    if jogador == estado.SOUTH:
        for i in range(7):
            ret += estado.state[i]
            ret -= estado.state[7+i]
    else:
        for i in range(7):
            ret -= estado.state[i]
            ret += estado.state[7+i]
    if estado.is_game_over():
        aux = estado.result()
        return aux * 100 if jogador == estado.SOUTH else aux  * -100
    return ret
