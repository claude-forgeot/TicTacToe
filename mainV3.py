import tkinter as tk
import tkinter.messagebox
import random

# ==========================================
# GLOBAL VARIABLES 
# ==========================================

root = None
game_mode = None
actual_player = "X"
board = ["", "", "", "", "", "", "", "", ""]
grid_button = [None] * 9
game_ended = False
#   True when win or draw
difficulty_level = None
#   Easy, medium, hard

# ==========================================
# GAMEPLAY FUNCTIONS
# ==========================================

def victory(board):
    #   win conditions (rows, columns, diagonals)
    winning_lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]
    
    #   Bool to test if win 
    for line in winning_lines:
        a, b, c = line[0], line[1], line[2]
        if board[a] != "" and board[a] == board[b] == board[c]:
            return True
    return False

def verify_draw(board):
    #   Loop all 9 positions
    for position in board:
        if position == "":
            return False
    #   Draw
    return True

def get_empty_positions(board):
    empty_list = []
    for position in range(9):
        #   When empty, add to list
        if board[position] == "":
            empty_list.append(position)
    
    return empty_list

# ==========================================
# AI ALGORITHM (MINIMAX)
# ==========================================

def minimax(board, depth, is_maximizing, ai_sign, opponent_sign):
    
    #   If someone won the game
    if victory(board):
        if is_maximizing:
            #   If we're checking AI's moves and there's a win, opponent won
            return depth - 10
        else:
            #   If we're checking opponent's moves and there's a win, AI won
            return 10 - depth
    
    #   Draw test
    if verify_draw(board):
        return 0
    
    #   AI's turn (try to maximize score)
    if is_maximizing:
        best_score = -float('inf')
        #   Worst possible score for AI
        
        #   Try every empty position
        for position in get_empty_positions(board):
            #   Simulation of AI playing in this position
            board[position] = ai_sign
            
            #   Calculate score with recursion
            score = minimax(board, depth + 1, False, ai_sign, opponent_sign)
            
            #   Cancel move (backtrack)
            board[position] = ""
            
            #   Save the best score with max()
            best_score = max(score, best_score)
        
        return best_score
    
    #   Opponent's turn (try to minimize score)
    else:
        best_score = float('inf')  
        #   Worst possible score for opponent
        
        #   Try every empty position
        for position in get_empty_positions(board):
            #   Simulate opponent playing at this position
            board[position] = opponent_sign
            
            #   Calculate score
            score = minimax(board, depth + 1, True, ai_sign, opponent_sign)
            
            #   Cancel move (backtrack)
            board[position] = ""
            
            #   Keep track of the best score (minimum for opponent)
            best_score = min(score, best_score)
        
        return best_score


def find_best_move(board, ai_sign, opponent_sign):

    best_score = -float('inf')  
    #   Start with worst score
    best_position = None
    
    #   Test every empty position
    for position in get_empty_positions(board):
        #   Simulate AI playing at this position
        board[position] = ai_sign
        
        #   Calculate the score using minimax
        score = minimax(board, 0, False, ai_sign, opponent_sign)
        
        #   Undo the move
        board[position] = ""
        
        #   If move better than previous, remember it
        if score > best_score:
            best_score = score
            best_position = position
    
    return best_position


# ==========================================
# AI FUNCTION
# ==========================================

def ia(board, signe):
    
    if signe == "X":
        opponent_sign = "O"
    else:
        opponent_sign = "X"
        
    #   Difficulty
    if difficulty_level == "Easy":
        #   Easy
        empty_positions = get_empty_positions(board)
        chosen_position = random.choice(empty_positions)
    
    elif difficulty_level == "Medium":
        #   Medium
        if random.random() < 0.5:
            chosen_position = find_best_move(board, signe, opponent_sign)
        else:
            empty_positions = get_empty_positions(board)
            chosen_position = random.choice(empty_positions)
    
    else:
        #   Hard
        chosen_position = find_best_move(board, signe, opponent_sign)
        
    #   Get a valid position
    if chosen_position is None:
        return False
    
    #   Make sure the position is between 0 and 8
    if chosen_position < 0 or chosen_position > 8:
        return False
    
    #   Make sure the chosen position is empty
    if board[chosen_position] != "":
        return False
    
    #   Return the chosen position
    return chosen_position


# ==========================================
# GAME MECHANICS
# ==========================================

def test_click_case(position):

    global board, actual_player, game_ended, game_mode
    
    #   Ignore if game over or position taken
    if game_ended or board[position] != "":
        return
    
    #   Place player's sign on the board
    board[position] = actual_player
    
    #   Grid button
    grid_button[position].config(text=actual_player)
    
    #   Check if current player won
    if victory(board):
        tkinter.messagebox.showinfo(
            "Victory!", f"Player {actual_player} won!")
        game_ended = True
        return
    
    #   Check if it's a draw
    if verify_draw(board):
        tkinter.messagebox.showinfo(
            "Draw", "Try again.")
        game_ended = True
        return
    
    #   Switch to the other player
    if game_mode == "1v1":
        #   Player vs Player mode
        if actual_player == "X":
            actual_player = "O"
        else:
            actual_player = "X"
    
    elif game_mode == "1vsAI":
        #   Player vs AI mode
        if actual_player == "X":
            actual_player = "O"
            move_ia()  

def move_ia():

    global board, game_ended, actual_player, grid_button
    
    #   Call AI function
    position = ia(board, "O")
    
    #   Errors
    if position is False:
        tkinter.messagebox.showerror("Error", "AI couldn't make a move!")
        return
    
    #   AI's sign on the board
    board[position] = "O"
    
    #   Update button to show O
    grid_button[position].config(text="O")
    
    #   Check if AI won
    if victory(board):
        tkinter.messagebox.showinfo("Defeat", "The AI won!")
        game_ended = True
        return
    
    #   Check if draw
    if verify_draw(board):
        tkinter.messagebox.showinfo("Draw", "It's a draw!")
        game_ended = True
        return
    
    #   Switch to human player
    actual_player = "X"


def launch_game_difficulty(level):

    global difficulty_level, game_mode, board, actual_player,\
        grid_button, game_ended
    
    difficulty_level = level
    game_mode = "1vsAI"
    actual_player = "X"
    board = ["", "", "", "", "", "", "", "", ""]
    grid_button = [None] * 9
    game_ended = False
    
    #   Clear the window
    for widget in root.winfo_children():
        widget.destroy()
    
    create_game_grid()
    
    # Add reset button
    button_reset = tk.Button(
        root,
        text="Reset",
        width=15,
        font=("Arial", 12),
        command=reset_application
    )
    button_reset.pack(pady=10)


# ==========================================
# GRAPHIC INTERFACE
# ==========================================

def create_game_grid():

    global root, grid_button
    
    frame_grid = tk.Frame(root)
    frame_grid.pack()
    
    #   Buttons in 3x3 grid
    for position in range(9):
        #   Row and column for grid layout
        row = position // 3
        column = position % 3
        
        #   Create button
        button = tk.Button(
            frame_grid,
            text="",
            width=10,
            height=3,
            font=("Arial", 20),
            command=lambda p=position: test_click_case(p)
        )
        
        #   Button in grid
        button.grid(row=row, column=column, padx=5, pady=5)
        
        #   Store button pos
        grid_button[position] = button


def create_selection_menu():
    global root
    
    #   Clear window
    for widget in root.winfo_children():
        widget.destroy()
    
    #   Title
    label_title = tk.Label(
        root,
        text="Tic Tac Toe",
        font=("Arial", 24, "bold")
    )
    label_title.pack(pady=20)
    
    #   1v1 button
    button_1v1 = tk.Button(
        root,
        text="1 vs 1",
        width=20,
        height=2,
        font=("Arial", 14),
        command=lambda: start_game("1v1")
    )
    button_1v1.pack(pady=10)
    
    #   1vsAI button
    button_1vsAI = tk.Button(
        root,
        text="1 vs AI",
        width=20,
        height=2,
        font=("Arial", 14),
        command=lambda: start_game("1vsAI")
    )
    button_1vsAI.pack(pady=10)
    
    #   Quit button
    button_quit = tk.Button(
        root,
        text="Quit",
        width=20,
        height=2,
        font=("Arial", 14),
        command=root.quit
    )
    button_quit.pack(pady=10)


def start_game(mode):

    global game_mode, board, actual_player, grid_button, game_ended
    
    if mode == "1vsAI":
        #   Difficulty selection menu
        show_difficulty_menu()
    else:
        #   Start 1v1 game
        game_mode = mode
        actual_player = "X"
        board = ["", "", "", "", "", "", "", "", ""]
        grid_button = [None] * 9
        game_ended = False
        
        #   Clear window
        for widget in root.winfo_children():
            widget.destroy()
        
        create_game_grid()
        
        #   Add reset button
        button_reset = tk.Button(
            root,
            text="Restart",
            width=15,
            font=("Arial", 12),
            command=reset_application
        )
        button_reset.pack(pady=10)
        
        #   Mode label
        label_mode = tk.Label(
            root,
            text=f"Mode: {mode}",
            font=("Arial", 20)
        )
        label_mode.pack(pady=10)


def show_difficulty_menu():

    #   Clear window
    for widget in root.winfo_children():
        widget.destroy()
    
    #   Title
    label = tk.Label(
        root,
        text="Choose difficulty:",
        font=("Arial", 16)
    )
    label.pack(pady=10)
    
    #   Easy button
    easy_button = tk.Button(
        root,
        text="Easy",
        font=("Arial", 14),
        command=lambda: launch_game_difficulty("easy")
    )
    easy_button.pack(pady=10)
    
    #   Medium button
    medium_button = tk.Button(
        root,
        text="Medium",
        font=("Arial", 14),
        command=lambda: launch_game_difficulty("medium")
    )
    medium_button.pack(pady=10)
    
    #   Hard button
    hard_button = tk.Button(
        root,
        text="Hard",
        font=("Arial", 14),
        command=lambda: launch_game_difficulty("hard")
    )
    hard_button.pack(pady=10)
    
    #   Back button
    return_button = tk.Button(
        root,
        text="Back",
        font=("Arial", 14),
        command=create_selection_menu
    )
    return_button.pack(pady=10)


def reset_application():
    
    create_selection_menu()


def main():
    global root
    
    #   Main window
    root = tk.Tk()
    root.title("Tic Tac Toe")
    root.geometry("600x600")
    root.resizable(False, False)
    
    create_selection_menu()
    
    root.mainloop()


#   Start main
if __name__ == "__main__":
    main()