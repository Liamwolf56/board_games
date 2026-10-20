import sys
import tkinter as tk
from tkinter import messagebox


class XiangqiApp:

  def __init__(self, root, mode="PvP"):
    self.root = root
    self.root.title(f"Xiangqi (Chinese Chess) - Mode: {mode}")
    self.root.geometry("680x820")
    self.root.config(bg="#f4c2c2")

    self.mode = mode
    self.board = [[None for _ in range(9)] for _ in range(10)]
    self.turn = 1
    self.selected_square = None

    self.time_red = 600
    self.time_black = 600
    self.timer_running = True

    # Reliable Monochrome Unicode Symbols for Xiangqi
    self.symbols = {
        "GENERAL": "♔",
        "ADVISOR": "★",
        "ELEPHANT": "♗",
        "HORSE": "♘",
        "CHARIOT": "♖",
        "CANNON": "◎",
        "SOLDIER": "●",
    }

    top_frame = tk.Frame(root, bg="#f4c2c2")
    top_frame.pack(fill=tk.X, padx=10, pady=10)

    tk.Button(
        top_frame,
        text="New Game",
        bg="#c0392b",
        fg="white",
        font=("Arial", 9, "bold"),
        command=self.new_game,
    ).pack(side=tk.LEFT, padx=5)

    tk.Button(
        top_frame,
        text="How to Play",
        bg="#34495e",
        fg="white",
        font=("Arial", 9, "bold"),
        command=self.show_instructions,
    ).pack(side=tk.LEFT, padx=5)

    self.timer_label = tk.Label(
        top_frame,
        text="Red: 10:00 | Black: 10:00",
        font=("Arial", 10, "bold"),
        bg="#f4c2c2",
        fg="#c0392b",
    )
    self.timer_label.pack(side=tk.RIGHT, padx=5)

    self.status_label = tk.Label(
        top_frame,
        text="Red's Turn",
        font=("Arial", 11, "bold"),
        bg="#f4c2c2",
        fg="#c0392b",
    )
    self.status_label.pack(side=tk.RIGHT, padx=10)

    board_frame = tk.Frame(root, bg="#e67e22", bd=4, relief="solid")
    board_frame.pack(pady=10)

    self.squares = {}
    for r in range(10):
      for c in range(9):
        btn = tk.Button(
            board_frame,
            text="",
            font=("Arial", 14, "bold"),
            width=3,
            height=1,
            bg="#fde3a7",
            command=lambda row=r, col=c: self.on_square_click(row, col),
        )
        btn.grid(row=r, column=c, padx=1, pady=1)
        self.squares[(r, c)] = btn

    self.setup_board()
    self.update_ui()
    self.run_timer()

  def setup_board(self):
    self.board = [[None for _ in range(9)] for _ in range(10)]
    self.turn = 1
    self.time_red = 600
    self.time_black = 600

    black_back = [
        "CHARIOT",
        "HORSE",
        "ELEPHANT",
        "ADVISOR",
        "GENERAL",
        "ADVISOR",
        "ELEPHANT",
        "HORSE",
        "CHARIOT",
    ]
    for c, p in enumerate(black_back):
      self.board[0][c] = {"type": p, "player": 2}

    self.board[2][1] = {"type": "CANNON", "player": 2}
    self.board[2][7] = {"type": "CANNON", "player": 2}
    for c in range(0, 9, 2):
      self.board[3][c] = {"type": "SOLDIER", "player": 2}

    for c in range(0, 9, 2):
      self.board[6][c] = {"type": "SOLDIER", "player": 1}
    self.board[7][1] = {"type": "CANNON", "player": 1}
    self.board[7][7] = {"type": "CANNON", "player": 1}

    red_back = [
        "CHARIOT",
        "HORSE",
        "ELEPHANT",
        "ADVISOR",
        "GENERAL",
        "ADVISOR",
        "ELEPHANT",
        "HORSE",
        "CHARIOT",
    ]
    for c, p in enumerate(red_back):
      self.board[9][c] = {"type": p, "player": 1}

  def new_game(self):
    self.setup_board()
    self.selected_square = None
    self.update_ui()

  def show_instructions(self):
    messagebox.showinfo(
        "How to Play Xiangqi",
        "• Xiangqi is Chinese Chess played across a river.\n• Cannons must jump"
        " over another piece to capture.\n• Goal: Capture the opponent's"
        " General (♔).",
    )

  def run_timer(self):
    if self.timer_running:
      if self.turn == 1:
        self.time_red = max(0, self.time_red - 1)
      else:
        self.time_black = max(0, self.time_black - 1)

      mr, sr = divmod(self.time_red, 60)
      mb, sb = divmod(self.time_black, 60)
      self.timer_label.config(
          text=f"Red: {mr:02d}:{sr:02d} | Black: {mb:02d}:{sb:02d}"
      )

      if self.time_red == 0 or self.time_black == 0:
        winner = "Black" if self.time_red == 0 else "Red"
        messagebox.showinfo("Time Out", f"Time's up! {winner} wins!")
        return

      self.root.after(1000, self.run_timer)

  def on_square_click(self, r, c):
    piece = self.board[r][c]

    if self.selected_square is None:
      if piece and piece["player"] == self.turn:
        self.selected_square = (r, c)
        self.highlight_squares(r, c)
    else:
      sr, sc = self.selected_square
      if (sr, sc) == (r, c):
        self.selected_square = None
        self.update_ui()
        return

      target = self.board[r][c]
      if target is None or target["player"] != self.turn:
        self.board[r][c] = self.board[sr][sc]
        self.board[sr][sc] = None
        self.selected_square = None
        self.turn = 2 if self.turn == 1 else 1
        self.update_ui()

        if self.turn == 2 and not self.check_game_over():
          self.root.after(400, self.ai_move)
      else:
        self.selected_square = (r, c)
        self.highlight_squares(r, c)

  def highlight_squares(self, r, c):
    self.update_ui()
    self.squares[(r, c)].config(bg="#7b68ee")
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
      nr, nc = r + dr, c + dc
      if 0 <= nr < 10 and 0 <= nc < 9:
        self.squares[(nr, nc)].config(bg="#85bb65")

  def ai_move(self):
    if self.check_game_over():
      return
    import random

    moves = []
    for r in range(10):
      for c in range(9):
        p = self.board[r][c]
        if p and p["player"] == 2:
          for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 10 and 0 <= nc < 9:
              t = self.board[nr][nc]
              if t is None or t["player"] != 2:
                moves.append(((r, c), (nr, nc)))

    if moves:
      (sr, sc), (tr, tc) = random.choice(moves)
      self.board[tr][tc] = self.board[sr][sc]
      self.board[sr][sc] = None

    self.turn = 1
    self.update_ui()
    self.check_game_over()

  def check_game_over(self):
    r_gen, b_gen = False, False
    for r in range(10):
      for c in range(9):
        p = self.board[r][c]
        if p and p["type"] == "GENERAL":
          if p["player"] == 1:
            r_gen = True
          elif p["player"] == 2:
            b_gen = True

    if not r_gen:
      messagebox.showinfo("Game Over", "Black Wins!")
      return True
    if not b_gen:
      messagebox.showinfo("Game Over", "Red Wins!")
      return True
    return False

  def update_ui(self):
    for r in range(10):
      for c in range(9):
        btn = self.squares[(r, c)]
        btn.config(bg="#fde3a7")
        p = self.board[r][c]
        if p:
          sym = self.symbols[p["type"]]
          fg_col = "#c0392b" if p["player"] == 1 else "#2c3e50"
          btn.config(text=sym, fg=fg_col)
        else:
          btn.config(text="")

    turn_str = "Red's Turn" if self.turn == 1 else "Black's Turn"
    color_code = "#c0392b" if self.turn == 1 else "#2c3e50"
    self.status_label.config(text=turn_str, fg=color_code)


if __name__ == "__main__":
  mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
  root = tk.Tk()
  app = XiangqiApp(root, mode)
  root.mainloop()
