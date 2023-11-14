import sys

def opposite_well_1408385(state, index):
	if index == 6:
		return state[13]
	if index == 13:
		return state[6]
	return state[12-index]

def func_1408385(estado, jogador):
	score = 0
	if jogador == estado.SOUTH:
		# Sementes ganhas
		score += (estado.state[6] - estado.state[13])*(sys.maxsize - 48)
		# Jogadas que levam a jogar outra vez
		if 1 == estado.state[5]:
			score += 6
		if 2 == estado.state[4]:
			score += 5
		if 3 == estado.state[3]:
			score += 4
		if 4 == estado.state[2]:
			score += 3
		if 5 == estado.state[1]:
			score += 2
		if 6 == estado.state[0]:
			score += 1
		# Jogadas em que podemos roubar sementes
		stolen_seeds = [0]
		for i in range(5):
			if estado.state[i] > 0 and i+estado.state[i] < 6 and estado.state[i+estado.state[i]] == 0:
				seeds_in_opposite_well = opposite_well_1408385(estado.state, i+estado.state[i])
				stolen_seeds.append(1 + seeds_in_opposite_well)
		stolen_seeds.sort()
		score += stolen_seeds[-1] + len(stolen_seeds) - 1
	else: #Quão bom é este estado para o NORTE
		# Sementes ganhas
		score += (estado.state[13] - estado.state[6])*(sys.maxsize - 48)
		# Jogadas que levam a jogar outra vez
		if 1 == estado.state[12]:
			score += 6
		if 2 == estado.state[11]:
			score += 5
		if 3 == estado.state[10]:
			score += 4
		if 4 == estado.state[9]:
			score += 3
		if 5 == estado.state[8]:
			score += 2
		if 6 == estado.state[7]:
			score += 1
		#testar multiplicar por 2as jogadasque levam a jogar dnv
		# Jogadas em que podemos roubar sementes
		stolen_seeds = [0]
		for i in range(7, 12):
			if estado.state[i] > 0 and i+estado.state[i] < 6 and estado.state[i+estado.state[i]] == 0:
				seeds_in_opposite_well = opposite_well_1408385(estado.state, i+estado.state[i])
				stolen_seeds.append(1 + seeds_in_opposite_well)
		stolen_seeds.sort()
		score += stolen_seeds[-1] + len(stolen_seeds) - 1
	return score
