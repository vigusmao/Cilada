# Python 3
# Jogo Cilada (original Gridlock)
# https://github.com/vigusmao/Cilada


from collections import defaultdict
from random import randint

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

games = { \
    1: "AABCDDEFGIKN",
    2: "ABCDDEFFGJKM",
    3: "ABCCDEFFIJMN",
    4: "ABDDEEFFIKMN",
    5: "ABBCDEFFIJKM",
    6: "ABBCCCDFIJKM",
    7: "ABBCCCDDEFFKJ",
    8: "ABBCCCDDHKLN",
    9: "ABBBCCDDEFFHL",
    10: "ABBBCCDDEFFLN",
    11: "ABBBCCCDDFFGI",
    12: "AABCDEFFGIJM",
    13: "AABCDDEFGKNM",
    14: "AABCDEFFGHIJ",
    15: "AABCDEFFGJMN",
    16: "AABCCDEFIJKM",
    17: "AABCCDDEEFFHN",
    18: "AABCCCDDGHIL",
    19: "AABBCCDFGIJK",
    20: "AABBCCDFGJLN",
    21: "AABBCCCDEFFIJ",
    22: "AABBCCCDEFFJN",
    23: "AABBCCCDJKLM",
    24: "AABBCCCDDEFHK",
    25: "AABBCCCDEFFIJ",
    26: "AABBFGIJKMN",
    27: "AABBBCFFGJMN",
    28: "AABBBCCCDDFGL",
    29: "AAABCCDEEFFIJ",
    30: "AAABCCDEEFFHJ",
    31: "AAABCDDEEFFGN",
    32: "AAABCCDDEEFKM",
    33: "AAABBCEFJKMN",
    34: "AAABBEFFGJMN",
    35: "AAABBBCCCDFGH",
    36: "AAABBBCCEFFIJ",
    37: "AAABCDEFGIMN",
    38: "AAABCCDDEEFHL",
    39: "AAABCCCDGIJL",
    40: "AAABBCEFIJKM",
    41: "AAABBCCCDDEEFF",
    42: "AAABBCCDGKHM",
    43: "AAAABBCCDEFGI",
    44: "AAACCCDEIJLN",
    45: "AAABBCCCIJLN",
    46: "AAAABCCDEEFHM",
    47: "AAAABCCDEEFIM",
    48: "AAAABBBCCCGFJ",
    49: "AAAABBBCCDEEFF",
    50: "BBBDDEFFKLMN"}

N_ROWS = len(board)
N_COLS = len(board[0])
TOTAL_POSITIONS = N_ROWS * N_COLS


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
    if len(used_positions) == TOTAL_POSITIONS:
        return True
    if len(missing_pieces) == 0:
        return False
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
         
def read_game():
    print("\n\n-------------\n")

    done = False
    while not done:
        sample_game = randint(1, len(games))
        game = input("Game number (1--%d) or pieces (e.g., %s): "
                     % (len(games), games[sample_game]))
        try:
            game = int(game)
            if game < 1 or game > len(games):
                print("Please select a game between 1 and %d." % len(games))
                continue
            game = games[game]
            print("Game pieces: %s" % game)
            done = True
        except ValueError:
            game = list(game.upper())
            done = True
            for piece in game:
                if piece not in shapes_by_piece:
                    print("Invalid piece: %s. Please try again." % piece)
                    done = False
                    break
            
    if len(game) == 0:
        return None
    return list(game)
    
def solve(game):
    used_positions = {}
    if backtrack(game, used_positions):
        return used_positions
    return False  # no solution is possible

def print_solution(solution):
    for row_idx in range(N_ROWS):
        print()
        for col_idx in range(N_COLS):
            print(solution[(row_idx, col_idx)], end=" ")

def list_games():
    print("\n\nSuggested games:\n")
    for game, pieces in games.items():
        print("Game %d: %s" % (game, pieces))


prepare()
list_games()

while True:
    game = read_game()
    if game is None:
        break
    result = solve(game)
    if result:
        print_solution(result)
    else:
        print("This game has no solution.")
    
    
