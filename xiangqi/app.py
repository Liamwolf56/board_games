import sys
import tkinter as tk
from tkinter import messagebox


class XiangqiApp:

  def __init__(self, root, mode="PvP"):
    self.root = root
    self.root.title(f"Xiangqi (Chinese Chess) - Mode: {mode}")
    self.root.geometry("650x880")
    self.root.config(bg="#2c3e50")

    self.mode = mode
    self.selected_square = None
    self.turn = "Red"  # Red (Uppercase) vs Black (Lowercase)
    self.game_over = False
    self.valid_moves = []

    # Match Timer (300 seconds / 5 mins per player)
    self.red_time = 300
    self.black_time = 300
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
        text="Red: 05:00 | Black: 05:00",
        font=("Arial", 11, "bold"),
        bg="#2c3e50",
        fg="white",
    )
    self.timer_label.pack(side=tk.RIGHT)

    self.status_label = tk.Label(
        root,
        text="Turn: Red (Select a piece)",
        font=("Arial", 11, "bold"),
        bg="#2c3e50",
        fg="#1abc9c",
    )
    self.status_label.pack(pady=5)

    self.board_frame = tk.Frame(root, bg="#d35400", bd=3, relief="solid")
    self.board_frame.pack(pady=5)

    self.setup_board_data()
    self.create_board_ui()
    self.update_timer()

  def show_rules(self):
    rules = (
        "XIANGQI RULES & VALID MOVES:\n\n"
        "• 10x9 grid separated by a River.\n"
        "• Green squares show valid traditional moves for the selected piece.\n"
        "• Generals (G/g) must stay inside their 9-square Palace.\n"
        "• Goal: Capture the opposing General."
    )
    messagebox.showinfo("How to Play - Xiangqi", rules)

  def setup_board_data(self):
    # R=Chariot, H=Horse, E=Elephant, A=Advisor, G=General, C=Cannon, S=Soldier
    self.board = [
        ["R", "H", "E", "A", "G", "A", "E", "H", "R"],
        [".", ".", ".", ".", ".", ".", ".", ".", "."],
        [".", "C", ".", ".", ".", ".", ".", "C", "."],
        ["S", ".", "S", ".", "S", ".", "S", ".", "S"],
        [".", ".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", ".", "."],
        ["s", ".", "s", ".", "s", ".", "s", ".", "s"],
        [".", "c", ".", ".", ".", ".", ".", "c", "."],
        [".", ".", ".", ".", ".", ".", ".", ".", "."],
        ["r", "h", "e", "a", "g", "a", "e", "h", "r"],
    ]

  def create_board_ui(self):
    self.buttons = {}
    for r in range(10):
      for c in range(9):
        btn = tk.Button(
            self.board_frame,
            text="",
            font=("Arial", 12, "bold"),
            width=3,
            height=1,
            command=lambda row=r, col=c: self.square_clicked(row, col),
        )
        btn.grid(row=r, column=c, padx=1, pady=1)
        self.buttons[(r, c)] = btn
    self.update_ui()

  def get_valid_moves(self, r, c, piece):
    moves = []
    is_red = piece.isupper()
    p = piece.lower()

    if p == "s":  # Soldier
      fwd = -1 if is_red else 1
      nr, nc = r + fwd, c
      if 0 <= nr < 10 and 0 <= nc < 9:
        if self.board[nr][nc] == "." or self.board[nr][nc].isupper() != is_red:
          moves.append((nr, nc))
      # Cross river sideways movement
      crossed_river = (is_red and r < 5) or (not is_red and r > 4)
      if crossed_river:
        for dc in [-1, 1]:
          nc = c + dc
          if 0 <= nc < 9:
            if (
                self.board[r][nc] == "."
                or self.board[r][nc].isupper() != is_red
            ):
              moves.append((r, nc))

    elif p == "g":  # General
      palace_rows = range(7, 10) if is_red else range(0, 3)
      palace_cols = range(3, 6)
      for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if nr in palace_rows and nc in palace_cols:
          if self.board[nr][nc] == "." or self.board[nr][nc].isupper() != is_red:
            moves.append((nr, nc))

    elif p == "r":  # Chariot (Rook-like)
      for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        step = 1
        while True:
          nr, nc = r + dr * step, c + dc * step
          if not (0 <= nr < 10 and 0 <= nc < 9):
            break
          target = self.board[nr][nc]
          if target == ".":
            moves.append((nr, nc))
          else:
            if target.isupper() != is_red:
              moves.append((nr, nc))
            break
          step += 1

    elif p == "c":  # Cannon (moves like chariot, jumps 1 piece to capture)
      for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        step = 1
        jumped = False
        while True:
          nr, nc = r + dr * step, c + dc * step
          if not (0 <= nr < 10 and 0 <= nc < 9):
            break
          target = self.board[nr][nc]
          if not jumped:
            if target == ".":
              moves.append((nr, nc))
            else:
              jumped = True
          else:
            if target != ".":
              if target.isupper() != is_red:
                moves.append((nr, nc))
              break
          step += 1

    else:
      # General fallback for other pieces (adjacent steps)
      for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
          if dr == 0 and dc == 0:
            continue
          nr, nc = r + dr, c + dc
          if 0 <= nr < 10 and 0 <= nc < 9:
            target = self.board[nr][nc]
            if target == "." or target.isupper() != is_red:
              moves.append((nr, nc))

    return moves

  def square_clicked(self, r, c):
    if self.game_over:
      return
    piece = self.board[r][c]

    if self.selected_square is None:
      if piece != ".":
        is_red = piece.isupper()
        current_is_red = self.turn == "Red"
        if (current_is_red and is_red) or (not current_is_red and not is_red):
          self.selected_square = (r, c)
          self.valid_moves = self.get_valid_moves(r, c, piece)
          self.update_ui()
    else:
      sr, sc = self.selected_square
      if (r, c) in self.valid_moves:
        target_piece = self.board[r][c]
        self.board[r][c] = self.board[sr][sc]
        self.board[sr][sc] = "."

        if target_piece.lower() == "g":
          self.game_over = True
          self.timer_running = False
          messagebox.showinfo(
              "🏆 Game Over!", f"{self.turn} captured the General!"
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
    self.turn = "Black" if self.turn == "Red" else "Red"
    color_code = "#e74c3c" if self.turn == "Red" else "#f1c40f"
    self.status_label.config(text=f"Turn: {self.turn} Player", fg=color_code)
    self.update_ui()

    if self.mode == "PvAI" and self.turn == "Black" and not self.game_over:
      self.root.after(600, self.ai_move)

  def ai_move(self):
    import random

    black_pieces = []
    for r in range(10):
      for c in range(9):
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

      if target.lower() == "g":
        self.game_over = True
        self.timer_running = False
        messagebox.showinfo("🏆 Game Over!", "Black AI captured the General!")
        return

    self.finish_turn()

  def update_timer(self):
    if self.timer_running and not self.game_over:
      if self.turn == "Red":
        if self.red_time > 0:
          self.red_time -= 1
      else:
        if self.black_time > 0:
          self.black_time -= 1

      r_min, r_sec = divmod(self.red_time, 60)
      b_min, b_sec = divmod(self.black_time, 60)
      self.timer_label.config(
          text=f"Red: {r_min:02d}:{r_sec:02d} | Black: {b_min:02d}:{b_sec:02d}"
      )

      if self.red_time == 0 or self.black_time == 0:
        self.game_over = True
        self.timer_running = False
        loser = "Red" if self.red_time == 0 else "Black"
        winner = "Black" if loser == "Red" else "Red"
        messagebox.showinfo("Time Out!", f"{loser} ran out of time! {winner} wins!")

    self.root.after(1000, self.update_timer)

  def update_ui(self):
    for r in range(10):
      for c in range(9):
        bg_color = "#f39c12" if (r + c) % 2 == 0 else "#e67e22"
        if self.selected_square == (r, c):
          bg_color = "#7b68ee"
        elif (r, c) in self.valid_moves:
          bg_color = "#2ecc71"

        txt = self.board[r][c] if self.board[r][c] != "." else ""
        self.buttons[(r, c)].config(text=txt, bg=bg_color)


if __name__ == "__main__":
  mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
  root = tk.Tk()
  app = XiangqiApp(root, mode)
  root.mainloop()
