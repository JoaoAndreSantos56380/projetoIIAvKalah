import math
import sys
from kalah import *

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


def possible_pass_v2(estado, jogador):
	pits = 6
	owned = 0
	i = pits
	if jogador == estado.SOUTH:
		for pit in range(pits):
			if estado.state[pit] == i:
				owned += 1
			i -= 1
	else:
		for pit in range(7,14):
			if estado.state[pit] == i:
				owned += 1
			i -= 1
	return owned

def possible_pass_again(estado, jogador):
	pits = 6
	owned = 0
	i = pits
	if jogador == estado.SOUTH:
		for pit in range(pits):
			if estado.state[pit] == i-1:
				owned += 1
			i -= 1
	else:
		for pit in range(7,14):
			if estado.state[pit] == i-1:
				owned += 1
			i -= 1
	return owned

def rouba_sementes(estado, jogador):
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

def stolen_seeds_adv(estado, jogador):
	stolen_seeds = []
	if jogador == estado.NORTH:
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

def steal_seeds_2(estado, jogador):
	score = 0
	if estado.is_game_over():
		return estado.result()*10000
	#maixmizar povos meus vazios com pocos adversarios cheios
	score += possible_pass_v2(estado, jogador) #* 3
	score += (estado.state[6] - estado.state[13]) * 3
	stolen_seeds_list = rouba_sementes(estado, jogador)
	stolen_seeds_num = 0
	if(len(stolen_seeds_list) > 0):
		stolen_seeds_num = stolen_seeds_list[-1] + len(stolen_seeds_list)
	score += stolen_seeds_num
	return score if jogador == estado.SOUTH else (-score)








# Heuristics
def owned_seeds(estado, jogador):
	return sum(estado.state[0:7]) if jogador == estado.SOUTH else sum(estado.state[7:])

def won_seeds(estado, jogador):
	return estado.state[6] if jogador == estado.SOUTH else estado.state[13]

def won_seeds_diff(estado, jogador):
	#print(estado)
	score = 0
	if jogador == estado.to_move and jogador == estado.SOUTH:
		score = (estado.state[6] - estado.state[13])*3
	elif jogador == estado.to_move and jogador == estado.NORTH:
		score = (estado.state[13] - estado.state[6])*3
	return score if jogador == estado.SOUTH else (-score)

def won_seeds_diff2(estado, jogador):
	#print(estado)
	""" score = 0
	if jogador == estado.SOUTH: """
	score = (estado.state[6] - estado.state[13])*3
	""" else:
		score = (estado.state[13] - estado.state[6])*3 """
	return score if jogador == estado.SOUTH else (-score)
	#return (estado.state[6] - estado.state[13])*3

def won_seeds_diff3(estado, jogador):
	#print(estado)
	#score = (estado.state[13] - estado.state[6])*3
	score = 0
	if jogador == estado.SOUTH:
		score += (estado.state[6] - estado.state[13])*3
	else:
		score -= (estado.state[13] - estado.state[6])*3

	return score if jogador == estado.SOUTH else (-score)

def won_seeds_diff32(estado, jogador):
	#print(estado)
	#score = (estado.state[13] - estado.state[6])*3
	score = 0
	if jogador == estado.SOUTH:
		score += estado.state[6] - estado.state[13]
	else:
		score -= (estado.state[13] - estado.state[6])
	return score
	""" score = 0
	if jogador == estado.SOUTH:
		score += (estado.state[6] - estado.state[13])*3
	else:
		score -= (estado.state[13] - estado.state[6])*3

	return score if jogador == estado.SOUTH else (-score) """

def roubo_sementes(estado, jogador):
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

def possivel_repete_jogadas(estado, jogador):
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

def possivel_repete_jogadas_adv(estado, jogador):
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

def owned_seeds_fun(estado, jogador):
	if estado.is_game_over():
		return estado.result()*1000
	score = owned_seeds(estado, jogador)
	return score if jogador == estado.SOUTH else (-score)

def possble_passing_fun(estado, jogador):
	if estado.is_game_over():
		return estado.result()*1000
	score = possivel_repete_jogadas(estado, jogador)
	return score if jogador == estado.SOUTH else (-score)

def possble_passing_adv_fun(estado, jogador):
	if estado.is_game_over():
		return estado.result()*1000
	score = possivel_repete_jogadas_adv(estado, jogador)
	return score if jogador == estado.SOUTH else (-score)

def steal_seeds(estado, jogador):
	if estado.is_game_over():
		return estado.result()*1000
	roubos_list = roubo_sementes(estado, jogador)
	if roubos_list > 0:
		score += roubos_list[-1] + len(roubos_list)
	return score if jogador == estado.SOUTH else (-score)

def steal_seeds_adv(estado, jogador):
	if estado.is_game_over():
		return estado.result()*1000
	roubos_adv = stolen_seeds_adv(estado, jogador)
	if roubos_adv > 0:
		score += roubos_adv[-1] + len(roubos_adv)
	return score if jogador == estado.SOUTH else (-score)

def holes_counter(estado, jogador):
	if estado.is_game_over():
		return estado.result()*1000
	score = max_holes(estado, jogador)
	return score if jogador == estado.SOUTH else (-score)

def won_seeds_diff(estado, jogador):
	#print(estado)
	score = 0
	if jogador == estado.to_move and jogador == estado.SOUTH:
		score = (estado.state[6] - estado.state[13])*3
	elif jogador == estado.to_move and jogador == estado.NORTH:
		score = (estado.state[13] - estado.state[6])*3
	return score if jogador == estado.SOUTH else (-score)

def won_seeds_diff2(estado, jogador):
	#print(estado)
	""" score = 0
	if jogador == estado.SOUTH:
		score = (estado.state[6] - estado.state[13])*3
	else:
		score = (estado.state[13] - estado.state[6])*3
	return score if jogador == estado.SOUTH else (-score) """
	return (estado.state[6] - estado.state[13])*3

def won_seeds_diff3(estado, jogador):
	#print(estado)
	#score = (estado.state[13] - estado.state[6])*3
	score = 0
	if jogador == estado.SOUTH:
		score += (estado.state[6] - estado.state[13])*3
	else:
		score -= (estado.state[13] - estado.state[6])*3

	return score if jogador == estado.SOUTH else (-score)



# Lost to owned_seeds_fun
def won_seeds_fun(estado, jogador):
	if estado.is_game_over():
		return estado.result()*1000
	score = won_seeds(estado, jogador)
	return score if jogador == estado.SOUTH else (-score)



def possible_pass_adversary_fun(estado, jogador):
	score = 0
	passings = possivel_repete_jogadas(estado, jogador)
	adv_passings = possivel_repete_jogadas_adv(estado, jogador)
	if adv_passings > passings:
		score += -1
	else:
		score += passings
	return score if jogador == estado.SOUTH else (-score)



def owned_possible_pass_adversary_fun(estado, jogador):
	score = 0
	passings = possivel_repete_jogadas(estado, jogador)
	adv_passings = possivel_repete_jogadas_adv(estado, jogador)
	if adv_passings > passings:
		score += -1
	else:
		score += passings
	return score if jogador == estado.SOUTH else (-score)



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


def my_own_fun_v7(estado, jogador):
	if estado.is_game_over():
		return estado.result()*100
	score = possible_pass_v2(estado, jogador)
	stolen_seeds_list = rouba_sementes(estado, jogador)
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


def steal_seeds_better_v2(estado, jogador):
	if estado.is_game_over():
		return estado.result()*100
	score = possible_pass_v2(estado, jogador)
	score += (estado.state[6] - estado.state[13]) * (sys.maxsize - 48)
	stolen_seeds_list = rouba_sementes(estado, jogador)
	stolen_seeds_num = 0
	if(len(stolen_seeds_list) > 0):
		stolen_seeds_num = stolen_seeds_list[-1] + len(stolen_seeds_list)
	score += stolen_seeds_num
	return score if jogador == estado.SOUTH else (-score)


def steal_seeds_better_v2_2(estado, jogador):
	if estado.is_game_over():
		return estado.result()*100
	score = 0
	if estado.pass_turn:
		if jogador == estado.SOUTH:
			score -= estado.state[13]
		else:
			score -= estado.state[6]
	score += possible_pass_v2(estado, jogador)*2
	score += (estado.state[6] - estado.state[13]) * (sys.maxsize - 48)
	""" if jogador == estado.SOUTH:
		score += (estado.state[6] - estado.state[13])*(sys.maxsize - 48)
	else:
		score -= (estado.state[13] - estado.state[6])*(sys.maxsize - 48) """
	stolen_seeds_list = rouba_sementes(estado, jogador)
	stolen_seeds_num = 0
	if(len(stolen_seeds_list) > 0):
		stolen_seeds_num = stolen_seeds_list[-1] + len(stolen_seeds_list)
	score += stolen_seeds_num
	return score if jogador == estado.SOUTH else (-score)


def steal_seeds_better_v2_2_impar(estado, jogador):
	if estado.is_game_over():
		return estado.result() * sys.maxsize
	score = 0
	#print(estado)
	if estado.pass_turn:
		if jogador == estado.SOUTH:
			score -= estado.state[13]
		else:
			score -= estado.state[6]
	score += (possible_pass_v2(estado, jogador)- possivel_repete_jogadas_adv(estado, jogador))*2
	score += (estado.state[6] - estado.state[13]) * (sys.maxsize-48)

	stolen_seeds_list = rouba_sementes(estado, jogador)
	stolen_seeds_num = 0
	if(len(stolen_seeds_list) > 0):
		stolen_seeds_num = stolen_seeds_list[-1] + len(stolen_seeds_list)
	score += stolen_seeds_num

	stolen_seeds_list = stolen_seeds_adv(estado, jogador)
	if(len(stolen_seeds_list) > 0):
		stolen_seeds_num = stolen_seeds_list[-1] + len(stolen_seeds_list)
	score -= stolen_seeds_num

	return score if jogador == estado.SOUTH else (-score)


def steal_seeds_better_v2_2_impar_kalah_mod(estado, jogador):
	if estado.is_game_over():
		return estado.result() * sys.maxsize
	score = 0
	#print(estado)
	""" if estado.pass_turn:
		score -= 1 """
	score += (possible_pass_v2(estado, jogador) - possivel_repete_jogadas_adv(estado, jogador)) * 32
	#score += (math.pow(estado.state[6],2) - math.pow(estado.state[13],2)) * 24
	if jogador == estado.SOUTH:
		score += (estado.state[6] - estado.state[13]) * (sys.maxsize - 48)
	else:
		score -= (estado.state[13] - estado.state[6]) * (sys.maxsize - 48)
	stolen_seeds_list = rouba_sementes(estado, jogador)
	stolen_seeds_num = 0
	if(len(stolen_seeds_list) > 0):
		stolen_seeds_num = (stolen_seeds_list[-1] + len(stolen_seeds_list)) * 64
	score += stolen_seeds_num

	stolen_seeds_list = stolen_seeds_adv(estado, jogador)
	if(len(stolen_seeds_list) > 0):
		stolen_seeds_num = (stolen_seeds_list[-1] + len(stolen_seeds_list)) * 64
	score -= stolen_seeds_num

	return score if jogador == estado.SOUTH else (-score)



def teste(estado, jogador):
	if estado.is_game_over():
		return estado.result() * sys.maxsize
	#print(estado)
	bonus = 0
	bonus_adv = 0
	score = 0
	if estado.state[6] > 18:
		i = 0
	if jogador == estado.SOUTH:
		score = 0
		if estado.pass_turn:
			score -= estado.state[13]
		#score += (possible_pass_v2(estado, jogador) - possivel_repete_jogadas_adv(estado, jogador))*2#16
		passing = possible_pass_v2(estado, jogador) - possivel_repete_jogadas_adv(estado, jogador)
		if passing > 0:
			bonus += passing
			new_passing = possible_pass_again(estado, jogador)
			if new_passing > 0:
				score += new_passing * estado.state[6] * 2 + 1
			if new_passing > 0:
				bonus += 1
			score += passing  * estado.state[6] + 1

		#score += sum(estado.state[:5]) - sum(estado.state[7:12])
		#score += (math.pow(estado.state[6],2) - math.pow(estado.state[13],2)) * 24
		stolen_seeds_list = rouba_sementes(estado,jogador)
		if (len(stolen_seeds_list) > 0):
			score += (stolen_seeds_list[-1] + len(stolen_seeds_list))* (48-estado.state[6]) #* 8#math.pow(estado.state[6],2)
			bonus += stolen_seeds_list[-1]
		stolen_seeds_list_adv = stolen_seeds_adv(estado, jogador)
		if (len(stolen_seeds_list_adv) > 0):
			score -= (stolen_seeds_list_adv[-1] + len(stolen_seeds_list_adv))*(48-estado.state[13]) #* 8#math.pow(estado.state[13],2)#*4
			bonus_adv += stolen_seeds_list_adv[-1]
		score += (estado.state[6] + bonus - estado.state[13] - bonus_adv) * 200#(sys.maxsize - 48)
	else:
		score = 0
		if estado.pass_turn:
			score += estado.state[6]
		#score -= (possible_pass_v2(estado, jogador) - possivel_repete_jogadas_adv(estado, jogador))*2#16
		bonus = 0
		bonus_adv = 0
		passing = possible_pass_v2(estado, jogador) - possivel_repete_jogadas_adv(estado, jogador)

		if passing > 0:
			bonus += passing
			new_passing = possible_pass_again(estado, jogador)
			if new_passing > 0:
				score -= new_passing * estado.state[13] * 2 + 1
			if new_passing > 0:
				bonus += 1
			score -= passing * estado.state[13] +1#* 6

		#score -= possible_pass_again(estado, jogador) * 5
		#score -= (sum(estado.state[7:12]) - sum(estado.state[:5]))
		#score -= (math.pow(estado.state[13],2) - math.pow(estado.state[6],2)) * 24
		stolen_seeds_list = rouba_sementes(estado,jogador)
		if (len(stolen_seeds_list) > 0):
			score -= (stolen_seeds_list[-1] + len(stolen_seeds_list))*(48-estado.state[13])#*8#math.pow(estado.state[13],2)#*2#*4
			bonus += stolen_seeds_list[-1]
		stolen_seeds_list_adv = stolen_seeds_adv(estado, jogador)
		if (len(stolen_seeds_list_adv) > 0):
			score += (stolen_seeds_list_adv[-1] + len(stolen_seeds_list_adv))*(48-estado.state[6])#*8#math.pow(estado.state[6],2)#*2#*4
			bonus_adv += stolen_seeds_list_adv[-1]
		score -= (estado.state[13] + bonus - estado.state[6] - bonus_adv) * 200#(sys.maxsize - 48)
	return score
	#ver se posso roubar se jogar dnv
	#verficar a contagem das sementes depois de avaliar roubos
	#score += (estado.state[6] - estado.state[13]) * 48
	#print(estado)
	""" if estado.pass_turn:
		score -= 1 """
	score += (possible_pass_v2(estado, jogador) - possivel_repete_jogadas_adv(estado, jogador))*2#16
	#score += (estado.state[6] - estado.state[13]) * 20
	if jogador == estado.SOUTH:
		score += math.pow((estado.state[6] - estado.state[13]),25)# * (sys.maxsize - 48)
	else:
		score -= math.pow((estado.state[13] - estado.state[6]),25)# * (sys.maxsize - 48)
	stolen_seeds_list = rouba_sementes(estado, jogador)
	stolen_seeds_num = 0
	if(len(stolen_seeds_list) > 0):
		stolen_seeds_num = (stolen_seeds_list[-1] + len(stolen_seeds_list))*4#32
	score += stolen_seeds_num

	stolen_seeds_list = stolen_seeds_adv(estado, jogador)
	if(len(stolen_seeds_list) > 0):
		stolen_seeds_num = (stolen_seeds_list[-1] + len(stolen_seeds_list))*4#32
	score -= stolen_seeds_num

	return score if jogador == estado.SOUTH else (-score)












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

class Chapiteau(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, chapiteau)

class StealSeedsBetterV2_2_impar_kalah_mod(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, steal_seeds_better_v2_2_impar_kalah_mod)

class StealSeedsBetterV2_2_impar(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, steal_seeds_better_v2_2_impar)

class StealSeedsBetterV2_2(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, steal_seeds_better_v2_2)

class StealSeedsBetterV2(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, steal_seeds_better_v2)

class StealSeedsBetterV2(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, steal_seeds_better_v2)





class MyOwnv7(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, my_own_fun_v7)
class MyOwnv6(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, my_own_fun_v6)
class MyOwn(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, my_own_fun)
class MyOwnv2(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, my_own_fun_v2)
class MyOwnv5(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, my_own_fun_v5)
class MyOwnv4(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, my_own_fun_v4)
class MyOwnv3(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, my_own_fun_v3)

class StealSeedsBetterV2_2_impar_kalah_mod(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, steal_seeds_better_v2_2_impar_kalah_mod)

class OwnedPossiblePassAdversary(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, owned_possible_pass_adversary_fun)

class PossiblePassAdversary(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, possible_pass_adversary_fun)

class WonSeeds(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, won_seeds_fun)

class WonSeedsDiff(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, won_seeds_diff)

class WonSeedsDiff2(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, won_seeds_diff2)

class WonSeedsDiff3(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, won_seeds_diff3)

class OwnedSeeds(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, owned_seeds_fun)

class StealSeedsBetter(JogadorAlfaBeta):
	def __init__(self, nome, depth):
		super().__init__(nome, depth, steal_seeds_2)
