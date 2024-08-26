from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from game_logic import is_valid_move, move_character, check_winner

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Game State
game_state = {
    'players': {},
    'board': [['' for _ in range(5)] for _ in range(5)],
    'turn': 'A'  # Player A starts
}

def reset_game_state():
    global game_state
    game_state = {
        'board': [['' for _ in range(5)] for _ in range(5)],
        'turn': 'A'
    }

# Initialize the game with player positions
def initialize_game():
    game_state['players'] = {
        'A': ['A-P1', 'A-H1', 'A-H2', 'A-P2', 'A-P3'],
        'B': ['B-P1', 'B-H1', 'B-H2', 'B-P2', 'B-P3']
    }
    game_state['board'][0] = game_state['players']['A']
    game_state['board'][4] = game_state['players']['B']
    game_state['turn'] = 'A'  # Player A starts

# Route to serve the game page
@app.route('/')
def index():
    reset_game_state() 
    return render_template('index.html')

# Socket event for initializing the game
@socketio.on('initialize')
def handle_initialize():
    initialize_game()
    emit('game_state', game_state, broadcast=True)

# Socket event for handling player moves
@socketio.on('player_move')
def handle_player_move(data):
    player = data['player']
    character = data['character']
    move = data['move']
    
    if game_state['turn'] != player:
        emit('invalid_move', {'error': 'Not your turn!'}, to=request.sid)
        return
    
    valid, message = is_valid_move(player, character, move, game_state)
    if valid:
        move_character(player, character, move, game_state)
        winner = check_winner(game_state)
        if winner:
            emit('game_over', {'winner': winner}, broadcast=True)
            return
        game_state['turn'] = 'B' if game_state['turn'] == 'A' else 'A'
        emit('game_state', game_state, broadcast=True)
    else:
        emit('invalid_move', {'error': message}, to=request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True)
