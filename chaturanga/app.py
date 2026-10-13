import sys
import tkinter as tk
from tkinter import messagebox


class ChaturangaApp:

  def __init__(self, root, mode="PvP"):
    self.root = root
    self.root.title(f"Chaturanga (Ancient Chess) - Mode: {mode}")
    self.root.geometry("600x780")
    self.root.config(bg="#34495e")

    self.mode = mode
    self.selected_square = None
    self.turn = "White"  # White vs Black
    self.game_over = False
    self.valid_moves = []

    # Match Timer (300 seconds / 5 mins)
    self.white_time = 300
    self.black_time = 300
    self.timer_running = True

    top_frame = tk.Frame(root, bg="#34495e")
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
        text="White: 05:00 | Black: 05:00",
        font=("Arial", 11, "bold"),
        bg="#34495e",
        fg="white",
    )
    self.timer_label.pack(side=tk.RIGHT)

    self.status_label = tk.Label(
        root,
        text="Turn: White (Select a piece)",
        font=("Arial", 11, "bold"),
        bg="#34495e",
        fg="#1abc9c",
    )
    self.status_label.pack(pady=5)

    self.board_frame = tk.Frame(root, bg="#2c3e50", bd=3, relief="solid")
    self.board_frame.pack(pady=5)

    self.setup_board_data()
    self.create_board_ui()
    self.update_timer()

  def show_rules(self):
    rules = (
        "CHATURANGA RULES & VALID MOVES:\n\n"
        "• 8x8 ancient predecessor to Chess.\n"
        "• Green squares show valid traditional moves for the selected piece.\n"
        "• Goal: Capture the opposing Raja (King - K/k)."
    )
    messagebox.showinfo("How to Play - Chaturanga", rules)

  def setup_board_data(self):
    # R=Ratha (Chariot), N=Ashva (Horse), E=Gaja (Elephant), M=Mantri (Counselor), K=Raja (King), P=Padati (Pawn)
    self.board = [
        ["R", "N", "E", "M", "K", "E", "N", "R"],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["p", "p", "p", "p", "p", "p", "p", "p", "p"],
        ["r", "n", "e", "m", "k", "e", "n", "r"],
    ]

  def create_board_ui(self):
    self.buttons = {}
    for r in range(8):
      for c in range(8):
        btn = tk.Button(
            self.board_frame,
            text="",
            font=("Arial", 18, "bold"),
            width=3,
            height=1,
            command=lambda row=r, col=c: self.square_clicked(row, col),
        )
        btn.grid(row=r, column=c, padx=1, pady=1)
        self.buttons[(r, c)] = btn
    self.update_ui()

  def get_valid_moves(self, r, c, piece):
    moves = []
    is_white = piece.isupper()
    p = piece.lower()
    fwd = -1 if is_white else 1

    if p == "p":  # Pawn
      nr, nc = r + fwd, c
      if 0 <= nr < 8 and 0 <= nc < 8:
        if self.board[nr][nc] == "." or self.board[nr][nc].isupper() != is_white:
          moves.append((nr, nc))
    elif p == "k":  # Raja (King)
      for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
          if dr == 0 and dc == 0:
            continue
          nr, nc = r + dr, c + dc
          if 0 <= nr < 8 and 0 <= nc < 8:
            if (
                self.board[nr][nc] == "."
                or self.board[nr][nc].isupper() != is_white
            ):
              moves.append((nr, nc))
    elif p == "r":  # Ratha (Chariot/Rook)
      for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        step = 1
        while True:
          nr, nc = r + dr * step, c + dc * step
          if not (0 <= nr < 8 and 0 <= nc < 8):
            break
          target = self.board[nr][nc]
          if target == ".":
            moves.append((nr, nc))
          else:
            if target.isupper() != is_white:
              moves.append((nr, nc))
            break
          step += 1
    elif p == "n":  # Ashva (Horse/Knight)
      for dr, dc in [
          (-2, -1),
          (-2, 1),
          (-1, -2),
          (-1, 2),
          (1, -2),
          (1, 2),
          (2, -1),
          (2, 1),
      ]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 8 and 0 <= nc < 8:
          target = self.board[nr][nc]
          if target == "." or target.isupper() != is_white:
            moves.append((nr, nc))
    else:
      # General fallback for Elephant, Counselor, etc. (1 step any direction)
      for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
          if dr == 0 and dc == 0:
            continue
          nr, nc = r + dr, c + dc
          if 0 <= nr < 8 and 0 <= nc < 8:
            if (
                self.board[nr][nc] == "."
                or self.board[nr][nc].isupper() != is_white
            ):
              moves.append((nr, nc))

    return moves

  def square_clicked(self, r, c):
    if self.game_over:
      return
    piece = self.board[r][c]

    if self.selected_square is None:
      if piece != ".":
        is_white = piece.isupper()
        current_is_white = self.turn == "White"
        if (current_is_white and is_white) or (
            not current_is_white and not is_white
        ):
          self.selected_square = (r, c)
          self.valid_moves = self.get_valid_moves(r, c, piece)
          self.update_ui()
    else:
      sr, sc = self.selected_square
      if (r, c) in self.valid_moves:
        target_piece = self.board[r][c]
        self.board[r][c] = self.board[sr][sc]
        self.board[sr][sc] = "."

        if target_piece.lower() == "k":
          self.game_over = True
          self.timer_running = False
          messagebox.showinfo(
              "🏆 Game Over!", f"{self.turn} captured the Raja (King)!"
          )
          self.status_label.config(
              text=f"Game Over: {self.turn} Wins!", fg="#f1c40f"
          )
          self.selected_square = None
          self.valid_moves = []
          self.update_ui()
          return

        self.finish_turn()
      else:
        if piece != "." and piece.isupper() == self.board[sr][sc].isupper():
          self.selected_square = (r, c)
          self.valid_moves = self.get_valid_moves(r, c, piece)
          self.update_ui()
        else:
          self.selected_square = None
          self.valid_moves = []
          self.update_ui()

  def finish_turn(self):
    self.selected_square = None
    self.valid_moves = []
    self.turn = "Black" if self.turn == "White" else "White"
    color_code = "#2ecc71" if self.turn == "White" else "#e74c3c"
    self.status_label.config(text=f"Turn: {self.turn} Player", fg=color_code)
    self.update_ui()

    if self.mode == "PvAI" and self.turn == "Black" and not self.game_over:
      self.root.after(600, self.ai_move)

  def ai_move(self):
    import random

    black_pieces = []
    for r in range(8):
      for c in range(8):
        p = self.board[r][c]
        if p != "." and p.islower():
          moves = self.get_valid_moves(r, c, p)
          if moves:
            black_pieces.append((r, c, moves))

    if black_pieces:
      fr, fc, moves = random.choice(black_pieces)
      tr, tc = random.choice(moves)
      target = self.board[tr][tc]
      self.board[tr][tc] = self.board[fr][fc]
      self.board[fr][fc] = "."

      if target.lower() == "k":
        self.game_over = True
        self.timer_running = False
        messagebox.showinfo("🏆 Game Over!", "Black AI captured the Raja!")
        return

    self.finish_turn()

  def update_timer(self):
    if self.timer_running and not self.game_over:
      if self.turn == "White":
        if self.white_time > 0:
          self.white_time -= 1
      else:
        if self.black_time > 0:
          self.black_time -= 1

      w_min, w_sec = divmod(self.white_time, 60)
      b_min, b_sec = divmod(self.black_time, 60)
      self.timer_label.config(
          text=f"White: {w_min:02d}:{w_sec:02d} | Black:"
          f" {b_min:02d}:{b_sec:02d}"
      )

      if self.white_time == 0 or self.black_time == 0:
        self.game_over = True
        self.timer_running = False
        loser = "White" if self.white_time == 0 else "Black"
        winner = "Black" if loser == "White" else "White"
        messagebox.showinfo("Time Out!", f"{loser} ran out of time! {winner} wins!")

    self.root.after(1000, self.update_timer)

  def update_ui(self):
    for r in range(8):
      for c in range(8):
        bg_color = "#f0d9b5" if (r + c) % 2 == 0 else "#b58863"
        if self.selected_square == (r, c):
          bg_color = "#7b68ee"
        elif (r, c) in self.valid_moves:
          bg_color = "#2ecc71"

        txt = self.board[r][c] if self.board[r][c] != "." else ""
        self.buttons[(r, c)].config(text=txt, bg=bg_color)


if __name__ == "__main__":
  mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
  root = tk.Tk()
  app = ChaturangaApp(root, mode)
  root.mainloop()
