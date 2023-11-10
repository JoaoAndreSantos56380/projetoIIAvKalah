from multiprocessing import Process, cpu_count, freeze_support
import multiprocessing
import time
from tqdm import tqdm
from players import *
from tournament import torneio

def tournament_function(start, end, progress_queue, result_queue):
	num_games = 20
	depth = 2
	players = [
		Chapiteau("Chapiteau", depth), # 578 pontos em 100 games
		#WonSeeds("WonSeeds", depth),
		#OwnedWonSeeds("OwnedWonSeeds", depth),
		#PossiblePass("PossiblePass", depth),
		#OwnedPossiblePass("OwnedPossiblePass", depth),
		#OwnedSeeds("OwnedSeeds", depth), # OwnedSeeds
		#PossiblePassAdversary("PossiblePassAdversary", depth),
		#OwnedPossiblePassAdversary("OwnedPossiblePassAdversary", depth),
		#StealSeedsBetter("steal_seeds_better", depth),
		#MyOwn("MyOwn", depth),
		#MyOwnv2("MyOwnv2", depth),
		#MyOwnv3("MyOwnv3", depth),
		#MyOwnv4("MyOwnv4", depth),
		#MyOwnv5("MyOwnv5", depth),
		#MyOwnv6("MyOwnv6", depth),
		#MyOwnv7("MyOwnv7", depth),
		#StealSeedsBetterV2("steal_seeds_better2", depth),
		#StealSeedsBetterV2_2("steal_seeds_better2_2", depth),
		#StealSeedsBetterV2_2_impar("steal_seeds_better2_2_impar", depth),
		StealSeedsBetterHoles("esburacado", depth),
		StealSeedsBetterV2_2_impar("steal_seeds_better2_2_impar2", depth),
	]
	tournament = dict()
	for index in range(start, end):
		current_tournament = torneio(num_games, players, index)
		tournament = {key: ((tournament.get(key) if key in tournament else 0) + value) for (key, value) in current_tournament.items()}
		progress_queue.put(1)  # Update the progress queue

	result_queue.put(tournament)  # Put tournament result into the result queue

def launch_processes():
	processes = []
	progress_queue = multiprocessing.Queue()  # Queue to hold progress updates
	result_queue = multiprocessing.Queue()  # Queue to hold individual results

	num_cores = cpu_count()
	num_processes = max(1, int(num_cores))
	num_boards = len(fairkalah_states)

	boards_per_process = num_boards // num_processes

	for i in range(num_processes):
		start = i * boards_per_process
		end = start + boards_per_process if i < num_processes - 1 else num_boards  # Include any remaining boards for the last process
		p = Process(target=tournament_function, args=(start, end, progress_queue, result_queue))
		p.start()
		processes.append(p)

	# Progress tracking for each process
	with tqdm(total=num_boards) as pbar:
		while any(p.is_alive() for p in processes):
				while not progress_queue.empty():
					pbar.update(progress_queue.get())

	for p in processes:
		p.join()

	# Aggregate results from each process
	final_results = {}
	while not result_queue.empty():
		tournament_result = result_queue.get()
		for key, value in tournament_result.items():
				final_results[key] = final_results.get(key, 0) + value

	# Determine the global winner
	temp_results = final_results.copy()
	first_place_name = max(final_results, key = final_results.get)
	first_place = (first_place_name, final_results.get(first_place_name))
	temp_results.pop(first_place_name)
	second_place_name = max(temp_results, key= temp_results.get)
	second_place = (second_place_name, temp_results.get(second_place_name))
	final_results = dict(sorted(final_results.items(), key=lambda item: item[1], reverse = True))
	print(final_results, "(diff:", first_place[1] - second_place[1], ") ", end="")

if __name__ == '__main__':
	freeze_support()
	start_time = time.perf_counter()
	launch_processes()
	end_time = time.perf_counter()
	elapsed_time = end_time - start_time
	print("Ran in", elapsed_time)
