from collections import defaultdict

shapes_by_piece = {'A': ('O', '+'), \
                   'B': ('Q', '+'), \
                   'C': ('Q', 'O'), \
                   'D': ('+', '+'), \
                   'E': ('Q', 'Q'), \
                   'F': ('O', 'O'), \
                   'G': ('Q', 'Q', 'O'), \
                   'H': ('Q', '+', 'O'), \
                   'I': ('+', 'O', 'Q'), \
                   'J': ('Q', '+', '+'), \
                   'K': ('Q', 'O', 'O'), \
                   'L': ('O', 'O', 'Q'), \
                   'M': ('O', '+', 'Q'), \
                   'N': ('O', 'Q', '+')}

board = [['Q', '+', 'O', 'O'], \
         ['O', 'Q', 'Q', '+'], \
         ['+', '+', 'O', '+'], \
         ['+', 'Q', 'O', 'Q'], \
         ['+', 'Q', '+', '+'], \
         ['O', 'Q', 'O', 'O'], \
         ['O', 'O', 'Q', 'Q']]

N_ROWS = len(board)
N_COLS = len(board[0])


matches_by_piece = defaultdict(list)

def is_a_match(shape, row_idx, col_idx):
    return row_idx < N_ROWS and row_idx >= 0 and \
           col_idx < N_COLS and col_idx >= 0 and \
           board[row_idx][col_idx] == shape

def gather_matches_for_piece_and_position(piece, row_idx, col_idx):
    shapes = shapes_by_piece[piece]
    if board[row_idx][col_idx] != shapes[0]:
        return
    matches = matches_by_piece[piece]

    # RIGHT
    if is_a_match(shapes[1], row_idx, col_idx+1):
        fit = True
        used_positions = [(row_idx, col_idx), (row_idx, col_idx+1)]
        if len(shapes) == 3:
            if is_a_match(shapes[2], row_idx+1, col_idx+1):
                used_positions.append((row_idx+1, col_idx+1))
            else:
                fit = False
        if fit:
            matches.append(list(used_positions))

    # DOWN        
    if is_a_match(shapes[1], row_idx+1, col_idx):
        fit = True
        used_positions = [(row_idx, col_idx), (row_idx+1, col_idx)]
        if len(shapes) == 3:
            if is_a_match(shapes[2], row_idx+1, col_idx-1):
                used_positions.append((row_idx+1, col_idx-1))
            else:
                fit = False
        if fit:
            matches.append(list(used_positions))

    # LEFT
    if is_a_match(shapes[1], row_idx, col_idx-1):
        fit = True
        used_positions = [(row_idx, col_idx), (row_idx, col_idx-1)]
        if len(shapes) == 3:
            if is_a_match(shapes[2], row_idx-1, col_idx-1):
                used_positions.append((row_idx-1, col_idx-1))
            else:
                fit = False
        if fit:
            matches.append(list(used_positions))

    # UP
    if is_a_match(shapes[1], row_idx-1, col_idx):
        fit = True
        used_positions = [(row_idx, col_idx), (row_idx-1, col_idx)]
        if len(shapes) == 3:
            if is_a_match(shapes[2], row_idx-1, col_idx+1):
                used_positions.append((row_idx-1, col_idx+1))
            else:
                fit = False
        if fit:
            matches.append(list(used_positions))

def prepare():
    for piece in shapes_by_piece:
        match_list = []
        for row_idx in range(N_ROWS):
            for col_idx in range(N_COLS):
                gather_matches_for_piece_and_position(piece, row_idx, col_idx)

def are_positions_available(intended_positions, used_positions):
    for intended_position in intended_positions:
        if intended_position in used_positions:
            return False
    return True

def backtrack(missing_pieces, used_positions):
    if len(missing_pieces) == 0:
        return True
    next_piece = missing_pieces.pop()
    for match in matches_by_piece[next_piece]:
        if are_positions_available(match, used_positions):
            #missing_pieces.pop()
            for pos in match:
                used_positions[pos] = next_piece
            if backtrack(missing_pieces, used_positions):
                return True
            for pos in match:
                del(used_positions[pos])
    missing_pieces.append(next_piece)
    return False
         
def play():
    game = list(input("Game: ").upper())
    if len(game) == 0:
        return None  # quit
    used_positions = {}
    if backtrack(game, used_positions):
        return used_positions
    return False  # no solution is possible

def print_solution(solution):
    for row_idx in range(N_ROWS):
        print()
        for col_idx in range(N_COLS):
            print(solution[(row_idx, col_idx)], end=" ")


prepare()

while True:
    result = play()
    if result is None:
        break
    elif result == False:
        print("This game has no solution.")
    else:
        print_solution(result)
    print("\n\n-------------\n")
    
