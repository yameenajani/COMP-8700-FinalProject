from copy import deepcopy
from sys import getsizeof
from board import *
import globals
import psutil
import time
import os
from heapq import *


def move_up(p_heuristic, parent_board, curr_board, pos, priority_queue, visited):
    if pos[0] - 1 >= 0:

        tmp = curr_board[pos[0] - 1][pos[1]]
        curr_board[pos[0] - 1][pos[1]] = curr_board[pos[0]][pos[1]]
        curr_board[pos[0]][pos[1]] = tmp
        cb_as_list = transform_to_string_list(curr_board)

        check_hm(Board(cb_as_list),
                 ' '.join(str(num) for row in parent_board for num in row),
                 p_heuristic, priority_queue, visited)


def move_down(p_heuristic, parent_board, curr_board, pos, priority_queue, visited):
    if pos[0] + 1 < EDGE_LENGTH:
        tmp = curr_board[pos[0] + 1][pos[1]]
        curr_board[pos[0] + 1][pos[1]] = curr_board[pos[0]][pos[1]]
        curr_board[pos[0]][pos[1]] = tmp
        cb_as_list = transform_to_string_list(curr_board)

        check_hm(Board(cb_as_list),
                 ' '.join(str(num) for row in parent_board for num in row),
                 p_heuristic, priority_queue, visited)


def move_left(p_heuristic, parent_board, curr_board, pos, priority_queue, visited):
    if pos[1] - 1 >= 0:

        tmp = curr_board[pos[0]][pos[1] - 1]
        curr_board[pos[0]][pos[1] - 1] = curr_board[pos[0]][pos[1]]
        curr_board[pos[0]][pos[1]] = tmp
        cb_as_list = transform_to_string_list(curr_board)

        check_hm(Board(cb_as_list),
                 ' '.join(str(num) for row in parent_board for num in row),
                 p_heuristic, priority_queue, visited)


def move_right(p_heuristic, parent_board, curr_board, pos, priority_queue, visited):
    if pos[1] + 1 < EDGE_LENGTH:

        tmp = curr_board[pos[0]][pos[1] + 1]
        curr_board[pos[0]][pos[1] + 1] = curr_board[pos[0]][pos[1]]
        curr_board[pos[0]][pos[1]] = tmp
        cb_as_list = transform_to_string_list(curr_board)

        check_hm(Board(cb_as_list),
                 ' '.join(str(num) for row in parent_board for num in row),
                 p_heuristic, priority_queue, visited)


def check_hm(b, parent, ph, priority_queue, visited):

    if HEURISTIC == 'M':
        h = b.manhattan_heuristic()
    else:
        h = b.displaced_tiles_heuristic()
    child = ' '.join(str(e) for e in b.board_as_string_list)

    if child not in visited.keys():
        heappush(priority_queue, (h, b.board_as_string_list))
        visited[child] = [h, h + ph, parent]
    elif child in visited:
        if h + visited[parent][1] < visited[child][1]:
            visited[child][1] = h + visited[parent][1]
            heappush(priority_queue, (h, b.board_as_string_list))


def get_path(board, visited):

    if board == 'NULL':
        return
    else:
        get_path(visited[board][2], visited)
        b = Board(board.split(' '))
        b.print_board()
        print('')
        if HEURISTIC == 'M':
            heur = str(b.manhattan_heuristic())
        else:
            heur = str(b.displaced_tiles_heuristic())
        print('Heuristic Value: ' + heur + '\n')


def a_star(start_board, heuristic):
    priority_queue = []
    visited = {}
    global HEURISTIC

    HEURISTIC = heuristic
    b = Board(start_board)

    if HEURISTIC == 'M':
        h = b.manhattan_heuristic()
    else:
        h = b.displaced_tiles_heuristic()

    cb_as_list = b.board_as_string_list
    visited[' '.join(str(e) for e in cb_as_list)] = [h, h, 'NULL']

    heappush(priority_queue, (h, cb_as_list))
    curr_max = 0

    curr_time = time.time()

    while len(priority_queue) != 0:

        if (time.time() - curr_time) * 1000 > 30000:
            print('30 sec timeout reached. Terminating.......')
            break
        node = heappop(priority_queue)

        if getsizeof(priority_queue) > curr_max:
            curr_max = getsizeof(priority_queue)

        if node[1] == GOAL_STATE_15_AS_ILIST or node[1] == GOAL_STATE_15_AS_SLIST:
            get_path(GOAL_STATE_15, visited)

            if HEURISTIC == 'M':
                heur = 'Manhattan Heuristic'
            else:
                heur = 'Displaced Tiles Heuristic'

            print('*** Solution Found Using ', heur, ' A*!     ***')
            print('*** Solution Path - ***')

            print('*** Heuristic Values are printed for each state.    ***'
                  '\n*** Heuristic used: ', heur, '              ***')
            if HEURISTIC == 'M':
                globals.memory_manhattan_astar = getsizeof(visited)
            else:
                globals.memory_displaced_astar = getsizeof(visited)
            visited.clear()
            return True

        curr_board = transform_to_matrix(node[1])

        pos = find_blank_tile(curr_board)

        move_up(node[0], curr_board, deepcopy(curr_board), pos, priority_queue, visited)
        move_down(node[0], curr_board, deepcopy(curr_board), pos, priority_queue, visited)
        move_left(node[0], curr_board, deepcopy(curr_board), pos, priority_queue, visited)
        move_right(node[0], curr_board, deepcopy(curr_board), pos, priority_queue, visited)

    print('There was no solution.')

    return False
