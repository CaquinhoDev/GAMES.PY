import tkinter as tk
import random
import time

# Inicialização das variáveis
human_score = 0
ai_score = 0
player1_score = 0
player2_score = 0
symbols = ['X', 'O']
human_moves = []
game_mode = None
turn = None
human_symbol = None
ai_symbol = None
board = None

def check_win(board, player):
    for row in board:
        if all([s == player for s in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2-i] == player for i in range(3)]):
        return True
    return False

def get_available_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                moves.append((i, j))
    return moves

def ai_move(board, ai_symbol, human_symbol, human_moves):
    available_moves = get_available_moves(board)
    if human_moves:
        preferred_moves = [move for move in human_moves if move in available_moves]
        if preferred_moves:
            move = random.choice(preferred_moves)
            human_moves.remove(move)
            return move
    for move in available_moves:
        board_copy = [row[:] for row in board]
        board_copy[move[0]][move[1]] = ai_symbol
        if check_win(board_copy, ai_symbol):
            return move
    for move in available_moves:
        board_copy = [row[:] for row in board]
        board_copy[move[0]][move[1]] = human_symbol
        if check_win(board_copy, human_symbol):
            return move
    return random.choice(available_moves)

def play_game():
    global human_symbol, ai_symbol, board, turn
    human_symbol, ai_symbol = random.sample(symbols, 2)
    board = [[" " for _ in range(3)] for _ in range(3)]
    turn = random.choice(['HUMANO', 'IA']) if game_mode == "AI" else "HUMANO1"
    update_status()
    update_board()

def cell_clicked(row, col):
    global turn, human_moves, human_score, ai_score, player1_score, player2_score
    if board[row][col] == " ":
        if game_mode == "AI":
            if turn == 'HUMANO':
                board[row][col] = human_symbol
                human_moves.append((row, col))
                animate_click(buttons[row][col])
                update_board()
                if check_win(board, human_symbol):
                    human_score += 1
                    update_status("HUMANO venceu!")
                    highlight_winning_combination(human_symbol)
                    return
                turn = 'IA'
                ai_turn()
        elif game_mode == "PVP":
            if turn == 'HUMANO1':
                board[row][col] = human_symbol
                animate_click(buttons[row][col])
                update_board()
                if check_win(board, human_symbol):
                    player1_score += 1
                    update_status("Player 1 venceu!")
                    highlight_winning_combination(human_symbol)
                    return
                turn = 'HUMANO2'
            elif turn == 'HUMANO2':
                board[row][col] = ai_symbol
                animate_click(buttons[row][col])
                update_board()
                if check_win(board, ai_symbol):
                    player2_score += 1
                    update_status("Player 2 venceu!")
                    highlight_winning_combination(ai_symbol)
                    return
                turn = 'HUMANO1'
    if all([cell != " " for row in board for cell in row]):
        update_status("DEU VELHA!")
        return

def ai_turn():
    global turn, human_moves, ai_score
    if turn == 'IA':
        row, col = ai_move(board, ai_symbol, human_symbol, human_moves)
        board[row][col] = ai_symbol
        animate_click(buttons[row][col])
        update_board()
        if check_win(board, ai_symbol):
            ai_score += 1
            update_status("IA venceu!")
            highlight_winning_combination(ai_symbol)
            return
        turn = 'HUMANO'
    if all([cell != " " for row in board for cell in row]):
        update_status("DEU VELHA!")
        return

def update_board():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=board[i][j], bg='lightgray')

def update_status(message=""):
    if game_mode == "AI":
        status_label.config(text=f"HUMANO: {human_score} | IA: {ai_score}  {message}")
    elif game_mode == "PVP":
        status_label.config(text=f"Player 1: {player1_score} | Player 2: {player2_score}  {message}")

def choose_ai():
    global game_mode
    game_mode = "AI"
    menu_frame.pack_forget()
    game_frame.pack()
    play_game()

def choose_pvp():
    global game_mode
    game_mode = "PVP"
    menu_frame.pack_forget()
    game_frame.pack()
    play_game()

def animate_click(button):
    original_bg = button.cget("bg")
    def flash():
        button.config(bg='yellow')
        button.update_idletasks()
        time.sleep(0.1)
        button.config(bg=original_bg)
    root.after(1, flash)

def highlight_winning_combination(player):
    for i in range(3):
        if all([board[i][j] == player for j in range(3)]):
            for j in range(3):
                buttons[i][j].config(bg='green')
            return
    for j in range(3):
        if all([board[i][j] == player for i in range(3)]):
            for i in range(3):
                buttons[i][j].config(bg='green')
            return
    if all([board[i][i] == player for i in range(3)]):
        for i in range(3):
            buttons[i][i].config(bg='green')
        return
    if all([board[i][2-i] == player for i in range(3)]):
        for i in range(3):
            buttons[i][2-i].config(bg='green')
        return

# Configurar a interface gráfica
root = tk.Tk()
root.title("Jogo da Velha")

menu_frame = tk.Frame(root)
menu_frame.pack()

tk.Label(menu_frame, text="Escolha o modo de jogo", font=('normal', 20)).pack(pady=20)
tk.Button(menu_frame, text="Jogar contra a IA", font=('normal', 20), command=choose_ai).pack(pady=10)
tk.Button(menu_frame, text="Jogar com outro jogador", font=('normal', 20), command=choose_pvp).pack(pady=10)

game_frame = tk.Frame(root)

buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(game_frame, text=" ", font=('normal', 40), width=5, height=2,
                                  command=lambda i=i, j=j: cell_clicked(i, j))
        buttons[i][j].grid(row=i, column=j)

status_label = tk.Label(game_frame, text="", font=('normal', 20))
status_label.grid(row=3, column=0, columnspan=3)

play_game_button = tk.Button(game_frame, text="Jogar Novamente", command=play_game, font=('normal', 20))
play_game_button.grid(row=4, column=0, columnspan=3)

root.mainloop()
