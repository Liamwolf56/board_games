import sys
import tkinter as tk
from tkinter import messagebox


class TicTacToeApp:

  def __init__(self, root, mode="PvP"):
    self.root = root
    self.root.title(f"Tic-Tac-Toe - Mode: {mode}")
    self.root.geometry("500x620")
    self.root.config(bg="#2c3e50")

    self.mode = mode
    self.board = [["" for _ in range(3)] for _ in range(3)]
    self.turn = "X"
    self.game_over = False

    # Match Timer (180 seconds / 3 minutes per player)
    self.x_time = 180
    self.o_time = 180
    self.timer_running = True

    # Top Control Bar
    top_frame = tk.Frame(root, bg="#2c3e50")
    top_frame.pack(fill=tk.X, padx=10, pady=10)

    tk.Button(
        top_frame,
        text="📖 How to Play",
        bg="#f39c12",
        fg="white",
        font=("Arial", 9, "bold"),
        command=self.show_rules,
    ).pack(side=tk.LEFT)

    self.timer_label = tk.Label(
        top_frame,
        text="X: 03:00 | O: 03:00",
        font=("Arial", 11, "bold"),
        bg="#2c3e50",
        fg="white",
    )
    self.timer_label.pack(side=tk.RIGHT)

    self.status_label = tk.Label(
        root,
        text="Turn: Player X",
        font=("Arial", 14, "bold"),
        bg="#2c3e50",
        fg="#3498db",
    )
    self.status_label.pack(pady=5)

    # 3x3 Board Grid
    board_frame = tk.Frame(root, bg="#34495e", bd=4, relief="solid")
    board_frame.pack(pady=15)

    self.buttons = {}
    for r in range(3):
      for c in range(3):
        btn = tk.Button(
            board_frame,
            text="",
            font=("Arial", 32, "bold"),
            width=4,
            height=2,
            bg="#ecf0f1",
            relief="raised",
            command=lambda row=r, col=c: self.make_move(row, col),
        )
        btn.grid(row=r, column=c, padx=3, pady=3)
        self.buttons[(r, c)] = btn

    self.update_timer()

  def show_rules(self):
    rules = (
        "TIC-TAC-TOE RULES:\n\n"
        "• Take turns placing your mark (X or O) in empty squares.\n"
        "• First player to align 3 of their marks horizontally, vertically, or diagonally wins!"
    )
    messagebox.showinfo("How to Play - Tic-Tac-Toe", rules)

  def make_move(self, r, c):
    if self.game_over or self.board[r][c] != "":
      return

    self.board[r][c] = self.turn
    text_color = "#3498db" if self.turn == "X" else "#e74c3c"
    self.buttons[(r, c)].config(text=self.turn, fg=text_color, bg="#ffffff")

    win_combo = self.check_win()
    if win_combo:
      self.game_over = True
      self.timer_running = False
      # Highlight winning line in gold
      for wr, wc in win_combo:
        self.buttons[(wr, wc)].config(bg="#f1c40f", fg="#2c3e50")
      messagebox.showinfo("🏆 Game Over!", f"Player {self.turn} Wins!")
      self.status_label.config(
          text=f"Winner: Player {self.turn}!", fg="#f1c40f"
      )
    elif all(self.board[r][c] != "" for r in range(3) for c in range(3)):
      self.game_over = True
      self.timer_running = False
      messagebox.showinfo("Game Over", "It's a Draw!")
      self.status_label.config(text="Game Draw!", fg="#bdc3c7")
    else:
      self.turn = "O" if self.turn == "X" else "X"
      next_color = "#3498db" if self.turn == "X" else "#e74c3c"
      self.status_label.config(text=f"Turn: Player {self.turn}", fg=next_color)

      if self.mode == "PvAI" and self.turn == "O" and not self.game_over:
        self.root.after(400, self.ai_move)

  def ai_move(self):
    import random

    empty_cells = [
        (r, c)
        for r in range(3)
        for c in range(3)
        if self.board[r][c] == ""
    ]
    if empty_cells:
      r, c = random.choice(empty_cells)
      self.make_move(r, c)

  def check_win(self):
    b = self.board
    # Rows & Columns
    for i in range(3):
      if b[i][0] != "" and b[i][0] == b[i][1] == b[i][2]:
        return [(i, 0), (i, 1), (i, 2)]
      if b[0][i] != "" and b[0][i] == b[1][i] == b[2][i]:
        return [(0, i), (1, i), (2, i)]

    # Diagonals
    if b[0][0] != "" and b[0][0] == b[1][1] == b[2][2]:
      return [(0, 0), (1, 1), (2, 2)]
    if b[0][2] != "" and b[0][2] == b[1][1] == b[2][0]:
      return [(0, 2), (1, 1), (2, 0)]

    return None

  def update_timer(self):
    if self.timer_running and not self.game_over:
      if self.turn == "X":
        if self.x_time > 0:
          self.x_time -= 1
      else:
        if self.o_time > 0:
          self.o_time -= 1

      x_min, x_sec = divmod(self.x_time, 60)
      o_min, o_sec = divmod(self.o_time, 60)
      self.timer_label.config(
          text=f"X: {x_min:02d}:{x_sec:02d} | O: {o_min:02d}:{o_sec:02d}"
      )

      if self.x_time == 0 or self.o_time == 0:
        self.game_over = True
        self.timer_running = False
        loser = "X" if self.x_time == 0 else "O"
        winner = "O" if loser == "X" else "X"
        messagebox.showinfo("Time Out!", f"Player {loser} ran out of time! Player {winner} wins!")

    self.root.after(1000, self.update_timer)


if __name__ == "__main__":
  mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
  root = tk.Tk()
  app = TicTacToeApp(root, mode)
  root.mainloop()
