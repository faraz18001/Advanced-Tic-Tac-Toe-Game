
# It's like the regular game but with 3 players which makes it way more fun
# The board size grows every time someone wins (until it hits 8x8) - pretty neat right?

def create_board(size):
    # Making an empty board... nothing fancy, just a bunch of spaces
    # It's like setting up a blank canvas, but for X's and O's
    board = []
    for _ in range(size):#literally created a nested matrix here!.
        row = []
        for _ in range(size):
            row.append(' ')
        board.append(row)
    return board

def print_board(board):
    # Printing out the board so humans can actually see what's going on
    # Added column numbers at the top and row numbers on the side
    # cuz nobody wants to count squares manually, right?
    size = len(board)
    
    # Print column numbers at the top
    print("\n   ", end="")
    for col in range(size):
        print(f"  {col} ", end="")
    print("  (Columns)")
    
    # Print the separator line
    print("   " + "----" * size)
    
    # Print each row with row numbers
    row_num = 0
    for row in board:
        print(f"{row_num} | ", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print(f" (Row {row_num})")
        print("   " + "----" * size)
        row_num += 1

def is_winner(board, player):
    # Checking if someone won... boring but necessary
    # Looking for three-in-a-row anywhere on the board
    size = len(board)
    
    # Check rows - like reading a book left to right
    for row in range(size):
        winner = True
        for col in range(size):
            if board[row][col] != player:
                winner = False
                break
        if winner:
            return True
    
    # Check columns - like reading a book top to bottom
    for col in range(size):
        winner = True
        for row in range(size):
            if board[row][col] != player:
                winner = False
                break
        if winner:
            return True
    
    # Check diagonal from top-left to bottom-right
    # Like drawing a line from your top-left pocket to your right shoe
    winner = True
    for i in range(size):
        if board[i][i] != player:
            winner = False
            break
    if winner:
        return True
    
    # Check diagonal from top-right to bottom-left
    # Like drawing a line from your top-right pocket to your left shoe
    winner = True
    for i in range(size):
        if board[i][size - 1 - i] != player:
            winner = False
            break
    if winner:
        return True
    
    return False

def get_available_moves(board):
    # Finding all the empty spots on the board
    # cuz we can't play where someone already played, duh!
    moves = []
    size = len(board)
    for row in range(size):
        for col in range(size):
            if board[row][col] == ' ':
                moves.append((row, col))
    return moves

def evaluate_board(board):
    # The AI uses this to figure out if it's winning or losing
    # +10 means AI is winning (woohoo!)
    # -10 means humans are winning (boooo!)
    # 0 means it's a draw (meh...)
    if is_winner(board, 'O'):  # AI wins
        return 10
    elif is_winner(board, 'X'):  # First human wins
        return -10
    elif is_winner(board, 'Y'):  # Second human wins
        return -10
    else:  # Nobody's winning yet
        return 0

def minimax(board, depth, is_maximizing, alpha, beta):
    # This is the AI's brain - it's thinking really hard about its next move
    # Don't worry if this looks like gibberish, it's just the AI being a smarty-pants
    # It basically looks at all possible future moves and picks the best one
    
    score = evaluate_board(board)
    
    # If someone won or the board is full, we're done here
    if score == 10 or score == -10:#base case#1 base#2
        return score, None
    
    if not get_available_moves(board):
        return 0, None#base case #3
    
    # If we've thought too many moves ahead, just stop
    # cuz even AI gets tired sometimes
    if depth == 0:#base case #4
        return score, None
    
    moves = get_available_moves(board)
    best_move = moves[0]
    
    if is_maximizing:  # AI's turn
        best_score = float('-inf')  # Starting with the worst possible score
        for move in moves:
            row, col = move
            board[row][col] = 'O'  # Try this move
            current_score, _ = minimax(board, depth - 1, False, alpha, beta)#recusion being used here
            board[row][col] = ' '  # Undo the move
            
            # If this move is better than our best so far, remember it
            if current_score > best_score:
                best_score = current_score
                best_move = move
            
            # Some fancy optimization stuff... don't worry about it
            alpha = max(alpha, best_score)#alpha cut off optimization
            if beta <= alpha:
                break
        
        return best_score, best_move
    
    else:  # Humans' turn
        best_score = float('inf')  # Starting with the best possible score
        for move in moves:
            row, col = move
            # Switching between X and Y for the two human players
            player = 'X' if len(moves) % 2 == 0 else 'Y'
            board[row][col] = player
            current_score, _ = minimax(board, depth - 1, True, alpha, beta)#recusion being used
            board[row][col] = ' '
            
            if current_score < best_score:
                best_score = current_score
                best_move = move
            
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        
        return best_score, best_move

def get_ai_move(board):
    # This is where the AI actually decides what move to make
    # For bigger boards, it doesn't think as many moves ahead
    # cuz ain't nobody got time for that
    size = len(board)
    if size <= 3:
        max_depth = 6  # For small boards, think harder
    elif size <= 4:
        max_depth = 4  # For medium boards, think less
    else:
        max_depth = 3  # For big boards, just wing it
    
    _, move = minimax(board, max_depth, True, float('-inf'), float('inf'))
    return move

def get_human_move(board, player):
    # Getting input from the human players
    # Keeps asking until they input something that actually makes sense
    size = len(board)
    while True:
        try:
            print(f"\nHey Player {player}, it's your turn!")
            move = input("Where do you wanna go? Type row,column (like 1,1): ")
            row, col = map(int, move.split(','))
            
            # Check if the move is valid (on the board and empty)
            if 0 <= row < size and 0 <= col < size and board[row][col] == ' ':
                return row, col
            else:
                print("Uh oh, you can't go there! Try again...")
        except (ValueError, IndexError):
            print("Bruh... Type it like this: row,column (example: 1,1)")

def play_game(size=3):
    # The main game loop - where all the magic happens!
    board = create_board(size)
    players = ['X', 'O', 'Y']  # X and Y are humans, O is the AI
    current_player_index = 0
    
    print("\n=== Welcome to the coolest Tic-Tac-Toe ever! ===")
    print("You're X, your friend is Y, and the AI is O")
    print("Type moves like this: row,column (example: 1,1)")
    
    while True:
        print_board(board)
        current_player = players[current_player_index]
        
        # Get the next move
        if current_player == 'O':
            print("\nAI is thinking... 🤔")
            row, col = get_ai_move(board)
            print(f"AI drops an O at: {row},{col}")
        else:
            row, col = get_human_move(board, current_player)
        
        # Make the move
        board[row][col] = current_player
        
        # Check if someone won
        if is_winner(board, current_player):
            print_board(board)
            if current_player == 'O':
                print("The AI wins! The robots are taking over! 🤖")
            else:
                print(f"Player {current_player} wins! Time to celebrate! 🎉")
            return min(size + 1, 8)  # Make the board bigger for next game
        
        # Check if it's a tie
        if not get_available_moves(board):
            print_board(board)
            print("It's a tie! Everyone's a winner! (sort of) 🤝")
            return min(size + 1, 8)
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % len(players)

def main():
    # This is where the party starts!
    size = 3  # Starting with a classic 3x3 board
    
    while True:
        size = play_game(size)
        if size >= 8:
            print("Wow, you've reached the maximum board size! You're a pro! 🏆")
        
        play_again = input("\nWanna play another round? (y/n): ").lower()
        if play_again != 'y':
            break

    print("Thanks for playing! Come back soon! 👋")

# This is where the magic begins when you run the file
if __name__ == "__main__":
    main()``
