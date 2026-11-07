import sys
import tkinter as tk
from tkinter import messagebox


class Connect4App:

  def __init__(self, root, mode="PvP"):
    self.root = root
    self.root.title(f"Connect 4 - Mode: {mode}")
    self.root.geometry("600x740")
    self.root.config(bg="#2c3e50")

    self.mode = mode
    self.board = [["" for _ in range(7)] for _ in range(6)]
    self.turn = "Red"
    self.game_over = False

    self.red_time = 300
    self.yellow_time = 300
    self.timer_running = True

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
        text="Red: 05:00 | Yellow: 05:00",
        font=("Arial", 11, "bold"),
        bg="#2c3e50",
        fg="white",
    )
    self.timer_label.pack(side=tk.RIGHT)

    self.status_label = tk.Label(
        root,
        text="Turn: Red Player",
        font=("Arial", 13, "bold"),
        bg="#2c3e50",
        fg="#e74c3c",
    )
    self.status_label.pack(pady=5)

    # Column drop buttons at the top
    drop_frame = tk.Frame(root, bg="#2c3e50")
    drop_frame.pack(pady=5)
    for c in range(7):
      btn = tk.Button(
          drop_frame,
          text=f"▼ {c+1}",
          font=("Arial", 10, "bold"),
          width=5,
          bg="#485460",
          fg="white",
          command=lambda col=c: self.drop_piece(col),
      )
      btn.grid(row=0, column=c, padx=3)

    # Board Container
    board_frame = tk.Frame(root, bg="#2980b9", bd=5, relief="solid")
    board_frame.pack(pady=10)

    self.buttons = {}
    for r in range(6):
      for c in range(7):
        # Using buttons for grid slots so we can control their background color perfectly
        cell = tk.Button(
            board_frame,
            text="",
            width=5,
            height=2,
            bg="#34495e",
            state=tk.DISABLED,
            relief="flat",
        )
        cell.grid(row=r, column=c, padx=2, pady=2)
        self.buttons[(r, c)] = cell

    self.update_timer()

  def show_rules(self):
    rules = (
        "CONNECT 4 RULES:\n\n"
        "• Click the '▼' buttons at the top of each column to drop your piece.\n"
        "• Red goes first, followed by Yellow.\n"
        "• First to connect 4 matching colored pieces horizontally, vertically, or diagonally wins!"
    )
    messagebox.showinfo("How to Play - Connect 4", rules)

  def drop_piece(self, col):
    if self.game_over:
      return

    target_row = -1
    for r in reversed(range(6)):
      if self.board[r][col] == "":
        target_row = r
        break

    if target_row != -1:
      self.board[target_row][col] = self.turn
      # Set explicit solid background color for the dropped piece
      color_code = "#e74c3c" if self.turn == "Red" else "#f1c40f"
      self.buttons[(target_row, col)].config(bg=color_code)

      if self.check_win(target_row, col):
        self.game_over = True
        self.timer_running = False
        messagebox.showinfo("🏆 Game Over!", f"{self.turn} Player Wins!")
        self.status_label.config(
            text=f"Winner: {self.turn} Player!", fg="#f1c40f"
        )
      elif all(self.board[0][c] != "" for c in range(7)):
        self.game_over = True
        self.timer_running = False
        messagebox.showinfo("Game Over", "It's a Draw!")
        self.status_label.config(text="Game Draw!", fg="#bdc3c7")
      else:
        self.turn = "Yellow" if self.turn == "Red" else "Red"
        next_color = "#e74c3c" if self.turn == "Red" else "#f1c40f"
        self.status_label.config(
            text=f"Turn: {self.turn} Player", fg=next_color
        )

        if self.mode == "PvAI" and self.turn == "Yellow" and not self.game_over:
          self.root.after(500, self.ai_move)

  def ai_move(self):
    import random

    valid_cols = [c for c in range(7) if self.board[0][c] == ""]
    if valid_cols:
      ai_col = random.choice(valid_cols)
      self.drop_piece(ai_col)

  def check_win(self, r, c):
    p = self.board[r][c]
    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in dirs:
      cnt = 1
      for step in (1, -1):
        nr, nc = r + dr * step, c + dc * step
        while 0 <= nr < 6 and 0 <= nc < 7 and self.board[nr][nc] == p:
          cnt += 1
          nr += dr * step
          nc += dc * step
      if cnt >= 4:
        return True
    return False

  def update_timer(self):
    if self.timer_running and not self.game_over:
      if self.turn == "Red":
        if self.red_time > 0:
          self.red_time -= 1
      else:
        if self.yellow_time > 0:
          self.yellow_time -= 1

      r_min, r_sec = divmod(self.red_time, 60)
      y_min, y_sec = divmod(self.yellow_time, 60)
      self.timer_label.config(
          text=f"Red: {r_min:02d}:{r_sec:02d} | Yellow:"
          f" {y_min:02d}:{y_sec:02d}"
      )

      if self.red_time == 0 or self.yellow_time == 0:
        self.game_over = True
        self.timer_running = False
        loser = "Red" if self.red_time == 0 else "Yellow"
        winner = "Yellow" if loser == "Red" else "Red"
        messagebox.showinfo("Time Out!", f"{loser} ran out of time! {winner} wins!")

    self.root.after(1000, self.update_timer)


if __name__ == "__main__":
  mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
  root = tk.Tk()
  app = Connect4App(root, mode)
  root.mainloop()
