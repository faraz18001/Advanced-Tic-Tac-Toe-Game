
PLAYERS = ['X', 'O', 'A']  # Define the three players - X is human, O and A are AI
EMPTY = '_'  # Symbol for empty cell

def create_board():
    """Create an empty 3x3 board"""
    return [[EMPTY for _ in range(3)] for _ in range(3)]

def print_board(board):
    """Print the current state of the board in a readable format"""
    for row in board:
        # Join cells with | and print each row
        print(' | '.join(row))
        # Print separator line
        print('-' * 9)

def is_moves_left(board):
    """Check if there are any empty cells left on the board"""
    # Iterate through each cell and return True if any empty cell found
    return any(EMPTY in row for row in board)

def make_move(board, position, player):
    """Make a move on the board and return the new board state"""
    # Create a new board (to maintain immutability)
    new_board = [row[:] for row in board]
    row, col = position
    new_board[row][col] = player
    return new_board

def is_valid_move(board, position):
    """Check if a move is valid (cell is empty and within bounds)"""
    row, col = position
    # Check if position is within bounds and cell is empty
    return (0 <= row <= 2 and 
            0 <= col <= 2 and 
            board[row][col] == EMPTY)

def evaluate_board(board, player_index):
    """Evaluate the board state for the given player
    Returns:
        10 if the player wins
        -10 if another player wins
        0 for no winner"""
    
    # Check rows for a win
    for row in board:
        if row[0] == row[1] == row[2] != EMPTY:
            return 10 if row[0] == PLAYERS[player_index] else -10
    
    # Check columns for a win
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != EMPTY:
            return 10 if board[0][col] == PLAYERS[player_index] else -10
    
    # Check diagonal from top-left to bottom-right
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return 10 if board[0][0] == PLAYERS[player_index] else -10
    
    # Check diagonal from top-right to bottom-left
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return 10 if board[0][2] == PLAYERS[player_index] else -10
    
    # Return 0 if no winner
    return 0

def minimax(board, depth, player_index, is_max):
    """Implement the minimax algorithm for three players
    Args:
        board: Current game board
        depth: Current depth in game tree
        player_index: Current player's index (0, 1, or 2)
        is_max: True if maximizing player, False if minimizing"""
    
    # Get the board evaluation for current player
    score = evaluate_board(board, player_index)
    
    # Return score if this is a terminal state
    if score == 10:  # Current player wins
        return score - depth
    if score == -10:  # Other player wins
        return score + depth
    if not is_moves_left(board):  # Game is draw
        return 0
    
    # If maximizing player's turn
    if is_max:
        best = float('-inf')
        # Try all possible moves
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    # Make the move
                    new_board = make_move(board, (i, j), PLAYERS[player_index])
                    # Recursively find the best value
                    best = max(best, minimax(new_board, depth + 1, 
                                          player_index, False))
        return best
    
    # If minimizing player's turn
    else:
        best = float('inf')
        next_player = (player_index + 1) % 3  # Get next player's index
        # Try all possible moves
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    # Make the move
                    new_board = make_move(board, (i, j), PLAYERS[next_player])
                    # Recursively find the best value
                    best = min(best, minimax(new_board, depth + 1, 
                                          player_index, True))
        return best

def find_best_move(board, player_index):
    """Find the best possible move for the current player"""
    best_val = float('-inf')
    best_move = (-1, -1)
    
    # Try all possible moves
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                # Make the move
                new_board = make_move(board, (i, j), PLAYERS[player_index])
                # Calculate value of this move
                move_val = minimax(new_board, 0, player_index, False)
                
                # Update best_move if this move is better
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val
    
    return best_move

def get_human_move(board):
    """Get and validate human player's move"""
    while True:
        try:
            # Get row and column input from user
            row = int(input("Enter row (0-2): "))
            col = int(input("Enter column (0-2): "))
            
            # Check if move is valid
            if is_valid_move(board, (row, col)):
                return (row, col)
            print("Invalid move, try again")
        except ValueError:
            print("Please enter numbers between 0 and 2")

def play_game():
    """Main game loop"""
    board = create_board()  # Initialize empty board
    current_player = 0  # Start with player X (human)
    
    # Continue while there are moves left
    while is_moves_left(board):
        print(f"\nPlayer {PLAYERS[current_player]}'s turn")
        print_board(board)
        
        # Get move based on player type (human or AI)
        if current_player == 0:  # Human player
            move = get_human_move(board)
        else:  # AI players
            move = find_best_move(board, current_player)
            if move == (-1, -1):
                print("Game Draw!")
                return
        
        # Make the move
        board = make_move(board, move, PLAYERS[current_player])
        
        # Check if current player won
        if evaluate_board(board, current_player) == 10:
            print_board(board)
            print(f"\nPlayer {PLAYERS[current_player]} wins!")
            return
        
        # Move to next player
        current_player = (current_player + 1) % 3
    
    # If no moves left and no winner, it's a draw
    print_board(board)
    print("\nGame Draw!")

# Start the game
if __name__ == "__main__":
    play_game()
