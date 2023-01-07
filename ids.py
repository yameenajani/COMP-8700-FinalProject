import os
import time
import psutil
import globals
from board import *
from copy import deepcopy


def move_board(direction, node, visited):
    cb_as_list = node[0]
    parent_board = node[1]
    pos = node[2]
    curr_board = deepcopy(parent_board)
    passed = False

    if direction == "UP" and pos[0] - 1 >= 0:
        passed = True
        tmp = curr_board[pos[0] - 1][pos[1]]
        curr_board[pos[0] - 1][pos[1]] = curr_board[pos[0]][pos[1]]
        curr_board[pos[0]][pos[1]] = tmp
        cb_as_list = transform_to_string_list(curr_board)

    elif direction == "DOWN" and pos[0] + 1 < EDGE_LENGTH:
        passed = True
        tmp = curr_board[pos[0] + 1][pos[1]]
        curr_board[pos[0] + 1][pos[1]] = curr_board[pos[0]][pos[1]]
        curr_board[pos[0]][pos[1]] = tmp
        cb_as_list = transform_to_string_list(curr_board)

    elif direction == "LEFT" and pos[1] - 1 >= 0:
        passed = True
        tmp = curr_board[pos[0]][pos[1] - 1]
        curr_board[pos[0]][pos[1] - 1] = curr_board[pos[0]][pos[1]]
        curr_board[pos[0]][pos[1]] = tmp
        cb_as_list = transform_to_string_list(curr_board)

    elif direction == "RIGHT" and pos[1] + 1 < EDGE_LENGTH:
        passed = True
        tmp = curr_board[pos[0]][pos[1] + 1]
        curr_board[pos[0]][pos[1] + 1] = curr_board[pos[0]][pos[1]]
        curr_board[pos[0]][pos[1]] = tmp
        cb_as_list = transform_to_string_list(curr_board)

    del curr_board[:]
    del curr_board

    if passed:
        result = check_hm(Board(cb_as_list), ' '.join(str(num) for row in parent_board for num in row), visited)
    else:
        return 'NULL'

    if result:
        return cb_as_list
    else:
        return 'NULL'


def check_hm(b, parent, visited):

    child = ' '.join(str(e) for e in b.board_as_string_list)
    if child not in visited.keys():
        visited[child] = parent
        return True
    return False


def get_path(board, visited):

    if board == 'NULL':
        return
    else:
        get_path(visited[board], visited)
        b = Board(board.split(' '))
        b.print_board()
        print('')


def ids(start_board):
    visited = {}
    curr_time = time.time()
    depth = 0

    while True:

        if (time.time() - curr_time) * 1000 > 30000:
            print('30 sec timeout reached. Terminating.....')
            break

        b = Board(start_board)
        cb_as_list = b.board_as_string_list
        visited[' '.join(str(e) for e in cb_as_list)] = 'NULL'

        if dls(start_board, depth, visited):
            get_path(GOAL_STATE_15, visited)
            print('*** Solution Found using Recursive IDS!                     ***')
            print('*** Solution Path - ***')
            return True

        depth += 1
        visited.clear()

    return False


def dls(current_board, depth, visited):
    b = Board(current_board)

    cb_as_list = b.board_as_string_list

    if cb_as_list == GOAL_STATE_15_AS_ILIST or cb_as_list == GOAL_STATE_15_AS_SLIST:
        return True

    if depth <= 0:
        return False

    curr_board = transform_to_matrix(cb_as_list)

    pos = find_blank_tile(curr_board)

    up_result = move_board("UP", [cb_as_list, curr_board, pos], visited)
    down_result = move_board("DOWN", [cb_as_list, curr_board, pos], visited)
    left_result = move_board("LEFT", [cb_as_list, curr_board, pos], visited)
    right_result = move_board("RIGHT", [cb_as_list, curr_board, pos], visited)

    process = psutil.Process(os.getpid())
    memory = process.memory_info().rss
    memory_ids = memory / 1000000
    globals.memory_ids = memory_ids

    if up_result != "NULL":
        if dls(up_result, depth - 1, visited):
            return True
    if down_result != "NULL":
        if dls(down_result, depth - 1, visited):
            return True
    if left_result != 'NULL':
        if dls(left_result, depth - 1, visited):
            return True
    if right_result != 'NULL':
        if dls(right_result, depth - 1, visited):
            return True

    return False


def nr_ids(start_board):
    curr_time = time.time()
    visited = {}
    overall_depth = 0

    while True:

        if (time.time() - curr_time) * 1000 > 30000:
            print('30 sec timeout reached. Terminating.....')
            break

        visited.clear()

        b = Board(start_board)
        cb_as_list = b.board_as_string_list

        visited[' '.join(str(e) for e in cb_as_list)] = 'NULL'
        lifo_pq = [(cb_as_list, 0)]

        while len(lifo_pq) > 0:

            curr_board = lifo_pq.pop()

            if curr_board[0] == GOAL_STATE_15_AS_ILIST or curr_board[0] == GOAL_STATE_15_AS_SLIST:
                get_path(GOAL_STATE_15, visited)
                print('*** Solution Found using Non-Recursive IDS!                     ***')
                print('*** Solution Path - ***')

                process = psutil.Process(os.getpid())
                memory = process.memory_info().rss
                memory_nr_ids = memory / 1000000
                globals.memory_nr_ids = memory_nr_ids

                return True

            if curr_board[1] < overall_depth:

                board_as_matrix = transform_to_matrix(curr_board[0])
                pos = find_blank_tile(board_as_matrix)

                up_result = move_board("UP", [curr_board[0], board_as_matrix, pos], visited)
                down_result = move_board("DOWN", [curr_board[0], board_as_matrix, pos], visited)
                left_result = move_board("LEFT", [curr_board[0], board_as_matrix, pos], visited)
                right_result = move_board("RIGHT", [curr_board[0], board_as_matrix, pos], visited)

                if right_result != 'NULL':
                    lifo_pq.append((right_result, curr_board[1] + 1))
                if left_result != 'NULL':
                    lifo_pq.append((left_result, curr_board[1] + 1))
                if down_result != "NULL":
                    lifo_pq.append((down_result, curr_board[1] + 1))
                if up_result != "NULL":
                    lifo_pq.append((up_result, curr_board[1] + 1))

        overall_depth = overall_depth + 1

    return False
