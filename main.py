from __future__ import print_function
from ids import ids, nr_ids
from random import shuffle, sample
from board import *
from bfs import bfs
from dfs import dfs
from a_star import a_star
from ucs import ucs
import globals
import psutil
import time
import gc
import os

def check_input(user_input):
    if user_input == 'r' or user_input == 'R':
        return True

    check_against = GOAL_STATE_15_AS_SLIST
    user_input = user_input.split(" ")

    if len(user_input) != 16:
        return False
    for num in check_against:
        if num not in user_input:
            return False
    return True


def randomize_board ():
    users_board = GOAL_STATE_15_AS_SLIST
    shuffled_board = sample(users_board, len(users_board))
    return shuffled_board


def print_board(users_board):
    board = ""
    count = 0
    for num in users_board:
        if count % EDGE_LENGTH == 0 and count != 0:
            board += '\n'
        if len(num) == 1:
            if num == '0':
                board += '   '
            else:
                board += num + '  '
        else:
            board += num + ' '
        count += 1
    print(board)


def main():
    print('*** COMP 8700 - INTRO TO AI ***')
    print('*** FINAL PROJECT - SLIDING PUZZLE PROBLEM ***')
    print('*** BY: Yameen Ajani (110096721) ***')
    print('***     Mohammed Farhan Baluch (110093799) ***')
    print()
    print('*** NOTE ***')
    print('You will be asked to enter a start board. You can either enter a board of your choice or you can enter "r" to randomize the start board. However, if you choose to randomize the start board, you may end up with a board that will run you out of memory or is not possible to solve. The current timeout is set to 30 seconds.')
    print()
    print('A dummy input is provided below. You can copy paste this and hit enter to test the program.')
    print('USE THIS: 1 2 3 4 5 6 7 8 13 9 12 15 0 11 10 14\n')
    user_input = input("Please enter here: ")
    users_board = -999
    is_valid = check_input(user_input)
    if is_valid:
        if user_input == 'r' or user_input == 'R':
            users_board = randomize_board()
        else:
            users_board = user_input.split(' ')
        print('Input is valid. Your board is: ')
        print_board(users_board)
    else:
        print('Input is invalid. Please restart the program and try again.')
        exit(0)

    print('------------')
    print('Please choose an algorithm to run:')
    print('1. BFS')
    print('2. DFS')
    print('3. UCS')
    print('4. Recursive IDS')
    print('5. Non-Recursive IDS')
    print('6. A* with Manhattan Heuristic')
    print('7. A* with Displaced Tiles Heuristic')
    print('8. Run all algorithms')
    print('------------')
    algo_option = input("Please enter here: ")
    if algo_option == '1':
        bfs_start_time = time.time()
        bfs(users_board)
        bfs_time = time.time() - bfs_start_time
        gc.collect()

        print('\n------------')
        print('Result of Time Elapsed:')
        print('------------')
        print('BFS Time Elapsed: ', bfs_time * 1000, 'ms')
        print('------------')
        print('Results on Memory Usage:')
        print('------------')
        print('Memory used in BFS search: ', globals.memory_bfs, ' MB')

    elif algo_option == '2':
        dfs_start_time = time.time()
        dfs(users_board)
        dfs_time = time.time() - dfs_start_time
        gc.collect()

        print('\n------------')
        print('Result of Time Elapsed:')
        print('------------')
        print('DFS Time Elapsed: ', dfs_time * 1000, 'ms')
        print('------------')
        print('Results on Memory Usage:')
        print('------------')
        print('Memory used in DFS search: ', globals.memory_dfs, ' MB')

    elif algo_option == '3':
        ucs_start_time = time.time()
        ucs(users_board)
        ucs_time = time.time() - ucs_start_time
        gc.collect()

        print('\n------------')
        print('Result of Time Elapsed:')
        print('------------')
        print('UCS Time Elapsed: ', ucs_time * 1000, 'ms')
        print('------------')
        print('Results on Memory Usage:')
        print('------------')
        print('Memory used in UCS search: ', globals.memory_ucs, ' MB')

    elif algo_option == '4':
        ids_start_time = time.time()
        ids(users_board)
        ids_time = time.time() - ids_start_time
        gc.collect()

        print('\n------------')
        print('Result of Time Elapsed:')
        print('------------')
        print('Recursive IDS Time Elapsed: ', ids_time * 1000, 'ms')
        print('------------')
        print('Results on Memory Usage:')
        print('------------')
        print('Memory used in Recursive IDS search: ', globals.memory_ids, ' MB')

    elif algo_option == '5':
        nr_ids_start_time = time.time()
        nr_ids(users_board)
        nr_ids_time = time.time() - nr_ids_start_time
        gc.collect()

        print('\n------------')
        print('Result of Time Elapsed:')
        print('------------')
        print('Non-Recursive IDS Time Elapsed: ', nr_ids_time * 1000, 'ms')
        print('------------')
        print('Results on Memory Usage:')
        print('------------')
        print('Memory used in Non-Recursive IDS search: ', globals.memory_nr_ids, ' MB')

    elif algo_option == '6':
        manhattan_astar_start_time = time.time()
        a_star(users_board, 'M')
        manhattan_astar_time = time.time() - manhattan_astar_start_time
        gc.collect()

        print('\n------------')
        print('Result of Time Elapsed:')
        print('------------')
        print('A* with Manhattan Heuristic Time Elapsed: ', manhattan_astar_time * 1000, 'ms')
        print('------------')
        print('Results on Memory Usage:')
        print('------------')
        print("Size of hashmap in A* search with Manhattan Distance Heuristic: ", globals.memory_manhattan_astar, ' MB')

    elif algo_option == '7':
        displaced_astar_start_time = time.time()
        a_star(users_board, 'D')
        displaced_astar_time = time.time() - displaced_astar_start_time
        gc.collect()

        print('\n------------')
        print('Result of Time Elapsed:')
        print('------------')
        print('A* with Displaced Tiles Heuristic Time Elapsed: ', displaced_astar_time * 1000, 'ms')
        print('------------')
        print('Results on Memory Usage:')
        print('------------')
        print("Size of hashmap in A* search with Displaced Tiles Heuristic: ", globals.memory_displaced_astar, ' MB')

    elif algo_option == '8':
        process = psutil.Process(os.getpid())
        memory = process.memory_info().rss
        memory_main = memory / 1000000

        globals.memory_main = memory_main

        # bfs time
        bfs_start_time = time.time()
        bfs(users_board)
        bfs_time = time.time() - bfs_start_time
        gc.collect()

        # dfs time
        dfs_start_time = time.time()
        dfs(users_board)
        dfs_time = time.time() - dfs_start_time
        gc.collect()

        # ucs time
        ucs_start_time = time.time()
        ucs(users_board)
        ucs_time = time.time() - ucs_start_time
        gc.collect()

        # ids time
        ids_start_time = time.time()
        ids(users_board)
        ids_time = time.time() - ids_start_time
        gc.collect()

        nr_ids_start_time = time.time()
        nr_ids(users_board)
        nr_ids_time = time.time() - nr_ids_start_time
        gc.collect()

        # Manhattan Heuristic used with A*
        manhattan_astar_start_time = time.time()
        a_star(users_board, 'M')
        manhattan_astar_time = time.time() - manhattan_astar_start_time
        gc.collect()

        # Displaced Tiles Heuristic used with A*
        displaced_astar_start_time = time.time()
        a_star(users_board, 'D')
        displaced_astar_time = time.time() - displaced_astar_start_time
        gc.collect()

        # 1 2 3 4 5 6 7 8 13 9 12 15 0 11 10 14
        # 1 2 3 4 5 6 7 8 0 9 10 15 13 14 12 11

        print('\n------------')
        print('Result of Time Elapsed:')
        print('------------')
        print('BFS Time Elapsed: ', bfs_time * 1000, 'ms')
        print('DFS Time Elapsed: ', dfs_time * 1000, 'ms')
        print('UCS Time Elapsed: ', ucs_time * 1000, 'ms')
        print('IDS Time Elapsed: ', ids_time * 1000, 'ms')
        print('NR_ids Time Elapsed: ', nr_ids_time * 1000, 'ms')
        print('Manhattan A* Time Elapsed: ', manhattan_astar_time * 1000, 'ms')
        print('Displaced A* Time Elapsed: ', displaced_astar_time * 1000, 'ms')
        print('------------')
        print('Results on Memory Usage:')
        print('------------')
        print("Memory used in main, just before any search:                      | ", globals.memory_main, ' MB')
        print("Memory used just before returning in bfs search:                  | ", globals.memory_bfs, ' MB')
        print("Memory used just before returning in dfs search:                  | ", globals.memory_dfs, ' MB')
        print("Memory used just before returning in ucs search:                  | ", globals.memory_ucs, ' MB')
        print("Memory used just before returning in recursive ids search:      | ", globals.memory_ids, ' MB')
        print("Memory used just before returning in Non-recursive ids search:  | ", globals.memory_nr_ids, ' MB')
        print("Size of hashmap in A* search with Manhattan Distance Heuristic:   | ", globals.memory_manhattan_astar, ' Bytes')
        print("Size of hashmap in A* search with Displaced Tiles Heuristic:      | ", globals.memory_displaced_astar, ' Bytes')

    else:
        print('Invalid option, please try again.')
        exit(0)

if __name__ == "__main__":
    main()
