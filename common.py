from board import *

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
    h = 0
    child = ' '.join(str(e) for e in b.board_as_string_list)

    if child not in visited.keys():
        priority_queue.append((h, b.board_as_string_list))
        visited[child] = [h, h + ph, parent]


def get_path(board, visited):
    if board == 'NULL':
        return
    else:
        get_path(visited[board][2], visited)
        b = Board(board.split(' '))
        b.print_board()
        print('')
