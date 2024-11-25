# yo these are the players we got (X, O, and Z)
PLAYERS = ['X', 'O', 'Z']  

# use this underscore to show empty spots n stuff
EMPTY = '_'  

def create_board():
    """make empty 3x3 board or smth"""
    # makes a 3x3 grid filled w/ empty spots using some fancy list comprehension lol
    return [[EMPTY for _ in range(3)] for _ in range(3)]

def print_board(board):
    """show the board or whatevr"""
    # gimme some space before printin
    print("\nCurrent Board:")
    # go thru each row n make it look nice w/ pipes n stuff
    for row in board:
        print(' | '.join(row))
        # add some dashes to make it look proper or w/e
        print('-' * 9)

def is_moves_left(board):
    """check if any empty spots left lol"""
    # checks if theres any empty cells left using that any() function which is pretty neat
    return any(EMPTY in row for row in board)

def make_move(board, position, player):
    """put player symbol on board or w/e"""
    # makes a copy of the board cuz we dont wanna mess up the og one
    new_board = [row[:] for row in board]
    # split that position tuple into row n col
    row, col = position
    # put the player's mark on the new board
    new_board[row][col] = player
    # send back the new version
    return new_board

def is_valid_move(board, position):
    """is this move valid? idk"""
    # grab the row n col from that position tuple
    row, col = position
    # make sure its in bounds n the spot is empty
    return (0 <= row <= 2 and 
            0 <= col <= 2 and 
            board[row][col] == EMPTY)

def check_winner(board, player):
    """did this player win or nah?"""
    # peep the rows for a winner
    for row in board:
        if row[0] == row[1] == row[2] == player:
            return True
    
    # now check them columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True
    
    # gotta check them diagonals too
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    
    # if we got here nobody won yet
    return False

def get_player_move(board, player):
    """get player move or smth"""
    # keep askin till we get a good move
    while True:
        try:
            # tell em whose turn it is
            print(f"\nPlayer {player}'s turn")
            # get their move inputs
            row = int(input("Enter row (0-2): "))
            col = int(input("Enter column (0-2): "))
            
            # check if its legit
            if is_valid_move(board, (row, col)):
                return (row, col)
            # if we get here the move was wack
            print("Invalid move! That spot is either taken or out of bounds.")
        except ValueError:
            # they typed smth that wasnt a number smh
            print("Please enter numbers between 0 and 2!")

def play_game():
    """main game loop or w/e"""
    # set up a fresh board
    board = create_board()
    # start w/ first player
    current_player = 0
    
    # print some intro stuff to look fancy
    print("\n=== Three Player Tic-Tac-Toe ===")
    print("Players: X, O, and Z")
    print("Enter row and column numbers (0-2) to make your move")
    
    # keep goin while there's moves left
    while is_moves_left(board):
        # show em the current state
        print_board(board)
        
        # get the move from whoever's turn it is
        move = get_player_move(board, PLAYERS[current_player])
        
        # update that board w/ the new move
        board = make_move(board, move, PLAYERS[current_player])
        
        # see if they won
        if check_winner(board, PLAYERS[current_player]):
            print_board(board)
            # ayy we got a winner
            print(f"\n🎉 Player {PLAYERS[current_player]} wins! 🎉")
            return
        
        # switch to next player using some modulo magic
        current_player = (current_player + 1) % 3
    
    # if the loop ends its cuz board is full n nobody won
    print_board(board)
    print("\n🤝 Game is a draw! 🤝")

# only run the game if we're runnin this file directly
if __name__ == "__main__":
    play_game()
