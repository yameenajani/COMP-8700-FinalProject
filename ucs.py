from copy import copy, deepcopy
from sys import getsizeof, maxsize
from board import *
import globals
from common import *
import psutil
import time
import os
from heapq import *

def find_node_with_min_cost(priority_queue):
    min_cost = maxsize
    min_cost_node = None

    for node in priority_queue:
        if node[0] < min_cost:
            min_cost = node[0]
            min_cost_node = node

    return min_cost_node

def ucs(start_board):
    priority_queue = []
    visited = {}

    b = Board(start_board)
    h = 0

    cb_as_list = b.board_as_string_list
    visited[' '.join(str(e) for e in cb_as_list)] = [h, h, 'NULL']

    priority_queue.append((h, cb_as_list))

    curr_max = 0

    curr_time = time.time()

    while len(priority_queue) != 0:

        if (time.time() - curr_time) * 1000 > 30000:
            print('30 sec timeout reached. Terminating.......')
            break
        node = find_node_with_min_cost(priority_queue)
        node = priority_queue.pop(priority_queue.index(node))
        if getsizeof(priority_queue) > curr_max:
            curr_max = getsizeof(priority_queue)

        
        if node[1] == GOAL_STATE_15_AS_ILIST or node[1] == GOAL_STATE_15_AS_SLIST:
            get_path(GOAL_STATE_15, visited)
            print('*** Solution Found Using UCS!                       ***')
            print('*** Solution Path - ***')

            process = psutil.Process(os.getpid())
            memory = process.memory_info().rss
            memory_ucs = memory / 1000000

            globals.memory_ucs = memory_ucs
            visited.clear()
            return True

        curr_board = transform_to_matrix(node[1])

        pos = find_blank_tile(curr_board)

        move_up(node[0], curr_board, deepcopy(curr_board), pos, priority_queue, visited)
        move_down(node[0], curr_board, deepcopy(curr_board), pos, priority_queue, visited)
        move_left(node[0], curr_board, deepcopy(curr_board), pos, priority_queue, visited)
        move_right(node[0], curr_board, deepcopy(curr_board), pos, priority_queue, visited)

    return False