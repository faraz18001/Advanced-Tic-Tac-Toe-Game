import time
import sys
import os
from colorama import init, Fore, Back, Style
import pandas as pd

# Initialize colorama for cross-platform color support
init()

# Define color schemes for players and UI
COLORS = {
    'X': Fore.BLUE + Style.BRIGHT,
    'O': Fore.RED + Style.BRIGHT,
    'Y': Fore.GREEN + Style.BRIGHT,
    'board': Fore.WHITE,
    'header': Fore.WHITE + Style.NORMAL,
    'error': Fore.RED + Style.BRIGHT,
    'success': Fore.GREEN + Style.BRIGHT,
    'prompt': Fore.MAGENTA + Style.BRIGHT
}

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

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

def print_board_animated(board):
    """Animated and colorful board printing."""
    size = len(board)
    clear_screen()
    
    # Print fancy header
    print(COLORS['header'] + "\n=== SUPER TIC-TAC-TOE BATTLE ===")
    #print("=" * 35 + Style.RESET_ALL + "\n")
    
    # Print column numbers with animation
    sys.stdout.write(COLORS['board'] + "   ")
    for col in range(size):
        sys.stdout.write(f"  {col} ")
        sys.stdout.flush()
        time.sleep(0.05)
    sys.stdout.write("  (Columns)\n")
    
    # Print separator line
    sys.stdout.write("   ")
    for _ in range(size):
        sys.stdout.write("----")
        sys.stdout.flush()
        time.sleep(0.02)
    sys.stdout.write("\n")
    
    # Print each row with colors and animation
    for row_num, row in enumerate(board):
        sys.stdout.write(COLORS['board'] + f"{row_num} |")
        sys.stdout.flush()
        time.sleep(0.05)
        
        for cell in row:
            color = COLORS.get(cell, Fore.WHITE) if cell != ' ' else Fore.WHITE
            sys.stdout.write(color + f" {cell} " + COLORS['board'] + "|")
            sys.stdout.flush()
            time.sleep(0.05)
        
        sys.stdout.write(f" (Row {row_num})\n")
        
        sys.stdout.write("   ")
        for _ in range(size):
            sys.stdout.write("----")
            sys.stdout.flush()
            time.sleep(0.02)
        sys.stdout.write("\n")
    
    print(Style.RESET_ALL)

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
    """Find all empty spots on the board."""
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

def minimax(board, depth, is_maximizing):

    score = evaluate_board(board)
    
    if score == 10 or score == -10 or depth == 0:
        return score, None
    
    moves = get_available_moves(board)
    if not moves:
        return 0, None
    
    best_move = moves[0]
    
    if is_maximizing:
        best_score = float('-inf')
        for move in moves:
            row, col = move
            board[row][col] = 'O'
            current_score, _ = minimax(board, depth - 1, False)
            board[row][col] = ' '
            
            if current_score > best_score:
                best_score = current_score
                best_move = move
            
            #alpha = max(alpha, best_score)
            #if beta <= alpha:
               # break
        
        return best_score, best_move
    
    else:
        best_score = float('inf')
        for move in moves:
            row, col = move
            player = 'X' if len(moves) % 2 == 0 else 'Y'
            board[row][col] = player
            current_score, _ = minimax(board, depth - 1, True)
            board[row][col] = ' '
            
            if current_score < best_score:
                best_score = current_score
                best_move = move
            
            #beta = min(beta, best_score)
            #if beta <= alpha:
                #break
        
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
    
    _, move = minimax(board, max_depth, True)
    return move

def get_human_move(board, player):
    """Get and validate human player's move with colored prompts."""
    size = len(board)
    while True:
        try:
            print(COLORS[player] + f"\n🎮 Player {player}'s turn!" + Style.RESET_ALL)
            print(COLORS['prompt'] + "Enter your move (row,column) like 1,1: " + Style.RESET_ALL, end='')
            move = input()
            row, col = map(int, move.split(','))
            
            if 0 <= row < size and 0 <= col < size and board[row][col] == ' ':
                return row, col
            else:
                print(COLORS['error'] + "⚠️  Oops! That spot is either taken or out of bounds!" + Style.RESET_ALL)
        except (ValueError, IndexError):
            print(COLORS['error'] + "❌ Please use the format: row,column (example: 1,1)" + Style.RESET_ALL)

def play_game(size=3):
    """Main game loop with colorful interface."""
    board = create_board(size)
    players = ['X', 'O', 'Y']
    current_player_index = 0
    
    # Welcome message
    print(COLORS['header'] + "\n🎮 Welcome to SUPER TIC-TAC-TOE! 🎮")
    print("X=Blue, O=Red (AI), Y=Green")
    print("Make moves like this: row,column (example: 1,1)" + Style.RESET_ALL)
    time.sleep(2)
    
    while True:
        print_board_animated(board)
        current_player = players[current_player_index]
        
        if current_player == 'O':  # AI's turn
            print(COLORS['O'] + "\n🤖 AI is calculating its master move..." + Style.RESET_ALL)
            time.sleep(1)
            row, col = get_ai_move(board)
            print(COLORS['O'] + f"🎯 AI chose: {row},{col}" + Style.RESET_ALL)
        else:
            row, col = get_human_move(board, current_player)
        
        board[row][col] = current_player
        
        if is_winner(board, current_player):
            print_board_animated(board)
            if current_player == 'O':
                print(COLORS['O'] + "\n🤖 The AI emerges victorious! The machines are rising! 🤖" + Style.RESET_ALL)
            else:
                print(COLORS[current_player] + f"\n🎉 Player {current_player} wins! Time to celebrate! 🎊" + Style.RESET_ALL)
            return min(size + 1, 8)
        
        if not get_available_moves(board):
            print_board_animated(board)
            print(COLORS['header'] + "\n🤝 It's a tie! Everyone's a winner! 🤝" + Style.RESET_ALL)
            return min(size + 1, 8)
        
        current_player_index = (current_player_index + 1) % len(players)

def main():
    """Main function with colorful game flow."""
    size = 3
    
    while True:
        size = play_game(size)
        if size >= 8:
            print(COLORS['success'] + "\n🏆 Incredible! You've reached the maximum board size! 🏆" + Style.RESET_ALL)
        
        print(COLORS['prompt'] + "\nWant to play another round? (y/n): " + Style.RESET_ALL, end='')
        if input().lower() != 'y':
            break

    print(COLORS['header'] + "\n👋 Thanks for playing! Come back soon! 👋" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
