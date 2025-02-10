import tkinter as tk
from tkinter import messagebox

# Окно игры
window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("400x500")
window.resizable(False, False)

# Глобальные переменные
current_player = ""
player_x = "X"
player_o = "O"
players = {"X": player_x, "O": player_o}

score_x = 0
score_o = 0
max_wins = 3

# Кнопки игрового поля
buttons = []

# Счётчики побед
label_score_x = None
label_score_o = None

# Флаг окончания партии
game_over = False


# Проверка наличия победителя
def check_winner():
    global game_over

    # Горизонтальная проверка
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            winner = buttons[i][0]["text"]
            game_over = True
            return winner

    # Вертикальная проверка
    for i in range(3):
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            winner = buttons[0][i]["text"]
            game_over = True
            return winner

    # Диагональная проверка
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        winner = buttons[0][0]["text"]
        game_over = True
        return winner

    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        winner = buttons[0][2]["text"]
        game_over = True
        return winner

    # Если все клетки заполнены, но победителя нет
    if all(all(button["text"] != "" for button in row) for row in buttons):
        game_over = True
        return "Tie"

    return None


# Обработка нажатия кнопки
def on_click(row, col):
    global current_player, game_over

    if game_over or buttons[row][col]['text'] != "":
        return

    buttons[row][col]['text'] = current_player

    winner = check_winner()

    if winner is not None:
        if winner == "Tie":
            messagebox.showinfo("Ничья!", "Все клетки заполнены! Ничья.")
        else:
            messagebox.showinfo(f"Победил игрок {winner}", f"Поздравляем игрока {winner}, вы выиграли!")

        update_scores(winner)
        reset_game()
    else:
        current_player = player_o if current_player == player_x else player_x


# Сброс игры
def reset_game():
    global current_player, game_over

    for row in buttons:
        for button in row:
            button.config(text="")

    current_player = player_x
    game_over = False


# Обновление счётчиков побед
def update_scores(winner):
    global score_x, score_o

    if winner == player_x:
        score_x += 1
    elif winner == player_o:
        score_o += 1

    label_score_x.config(text=f"Счёт X: {score_x}")
    label_score_o.config(text=f"Счёт O: {score_o}")

    if score_x >= max_wins or score_o >= max_wins:
        messagebox.showinfo("Победитель турнира!",
                            f"Игрок {'X' if score_x > score_o else 'O'} выиграл турнир!")
        new_game()


# Новый матч
def new_game():
    global score_x, score_o
    score_x = 0
    score_o = 0
    label_score_x.config(text=f"Счёт X: {score_x}")
    label_score_o.config(text=f"Счёт O: {score_o}")
    reset_game()


# Выбор символа для игрока
def choose_symbol(player):
    global current_player
    current_player = players[player]
    start_frame.grid_remove()
    window.update_idletasks()  # Обновить окно после удаления кнопки


# Создание кнопок игрового поля
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(window, text="", font=("Arial", 20), width=5, height=2, command=lambda r=i, c=j: on_click(r, c))
        btn.grid(row=i + 1, column=j)
        row.append(btn)
    buttons.append(row)

# Интерфейс выбора символа
start_frame = tk.Frame(window)
start_frame.grid(row=0, column=0, columnspan=3, pady=(50, 10))

start_label = tk.Label(start_frame, text="Выберите свой символ:", font=("Arial", 16))
start_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))

choose_x = tk.Button(start_frame, text="X", font=("Arial", 14), command=lambda: choose_symbol("X"))
choose_x.grid(row=1, column=0, padx=(40, 0))

choose_o = tk.Button(start_frame, text="O", font=("Arial", 14), command=lambda: choose_symbol("O"))
choose_o.grid(row=1, column=1, padx=(0, 40))

# Интерфейс счётчика побед
label_score_x = tk.Label(window, text=f"Счёт X: {score_x}", font=("Arial", 12))
label_score_x.grid(row=4, column=0, sticky='w', padx=(70, 0), pady=(20, 0))

label_score_o = tk.Label(window, text=f"Счёт O: {score_o}", font=("Arial", 12))
label_score_o.grid(row=4, column=1, sticky='e', padx=(0, 60), pady=(20, 0))

# Кнопка сброса
reset_button = tk.Button(window, text="Сбросить игру", font=("Arial", 12), command=reset_game)
reset_button.grid(row=5, column=0, columnspan=2, pady=(20, 0))

# Запуск главного цикла
window.mainloop()