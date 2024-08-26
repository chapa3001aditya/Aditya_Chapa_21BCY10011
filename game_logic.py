def is_valid_move(player, character, move, game_state):
    """
    Validate if the move is allowed based on the current game state.
    """
    board = game_state['board']
    player_characters = game_state['players'][player]

    pos = find_character_position(player, character, board)
    if not pos:
        return False, "Character not found on the board."

    row, col = pos
    new_row, new_col = calculate_new_position(player, character, move, row, col)

    if new_row < 0 or new_row >= 5 or new_col < 0 or new_col >= 5:
        return False, "Move would take the character out of bounds."

    if board[new_row][new_col] and board[new_row][new_col].startswith(player):
        return False, "Move targets a friendly character."

    if character.startswith('H1') or character.startswith('H2'):
        if not validate_path_clear(player, character, move, row, col, new_row, new_col, board):
            return False, "Move path is blocked."

    return True, ""

def move_character(player, character, move, game_state):
    """
    Move the character on the board and update the game state.
    """
    board = game_state['board']
    pos = find_character_position(player, character, board)
    row, col = pos
    new_row, new_col = calculate_new_position(player, character, move, row, col)

    # Execute the move
    board[new_row][new_col] = character
    board[row][col] = ''

    # Handle combat (remove opponent's character if present)
    opponent = 'A' if player == 'B' else 'B'
    if board[new_row][new_col] and board[new_row][new_col].startswith(opponent):
        remove_character(opponent, board[new_row][new_col], game_state)

def check_winner(game_state):
    """
    Check if one player has won the game by eliminating all opponent's characters.
    """
    for player, characters in game_state['players'].items():
        if all(char == '' for char in characters):
            return 'A' if player == 'B' else 'B'
    return None

def find_character_position(player, character, board):
    """
    Find the current position of a character on the board.
    """
    for row in range(5):
        for col in range(5):
            if board[row][col] == character:
                return row, col
    return None

def calculate_new_position(player, character, move, row, col):
    """
    Calculate the new position based on the move command.
    """
    if move == 'L':
        return row, col - 1
    elif move == 'R':
        return row, col + 1
    elif move == 'F':
        return row - 1 if player == 'A' else row + 1, col
    elif move == 'B':
        return row + 1 if player == 'A' else row - 1, col
    elif move == 'FL':
        return row - 1, col - 1 if player == 'A' else row + 1, col + 1
    elif move == 'FR':
        return row - 1, col + 1 if player == 'A' else row + 1, col - 1
    elif move == 'BL':
        return row + 1, col - 1 if player == 'A' else row - 1, col + 1
    elif move == 'BR':
        return row + 1, col + 1 if player == 'A' else row - 1, col - 1

def validate_path_clear(player, character, move, start_row, start_col, end_row, end_col, board):
    """
    Validate if the path is clear for Hero1 and Hero2's moves.
    """
    delta_row = end_row - start_row
    delta_col = end_col - start_col
    steps = max(abs(delta_row), abs(delta_col))

    for step in range(1, steps):
        intermediate_row = start_row + (delta_row // steps) * step
        intermediate_col = start_col + (delta_col // steps) * step
        if board[intermediate_row][intermediate_col]:
            return False
    return True

def remove_character(player, character, game_state):
    """
    Remove a character from the player's list when it is killed.
    """
    game_state['players'][player].remove(character)
