import random
import sys
import tkinter as tk
from tkinter import messagebox


class CheckersApp:

  def __init__(self, root, mode="PvP"):
    self.root = root
    self.root.title(f"Checkers - Mode: {mode}")
    self.root.geometry("680x780")
    self.root.config(bg="#2c3e50")

    self.mode = mode
    self.turn = "Red"  # Red vs Blue
    self.game_over = False
    self.selected_piece = None  # (r, c)
    self.valid_destinations = []  # List of valid (tr, tc) tuples

    # 8x8 Board setup: "" = empty, "r" = Red, "R" = Red King, "b" = Blue, "B" = Blue King
    self.board = [["" for _ in range(8)] for _ in range(8)]
    self.init_board()

    # Timers (300 seconds / 5 mins)
    self.red_time = 300
    self.blue_time = 300
    self.timer_running = True

    # Top Control Bar
    top_frame = tk.Frame(root, bg="#2c3e50")
    top_frame.pack(fill=tk.X, padx=10, pady=10)

    tk.Button(
        top_frame,
        text="How to Play",
        bg="#f39c12",
        fg="white",
        font=("Arial", 9, "bold"),
        command=self.show_rules,
    ).pack(side=tk.LEFT)

    self.timer_label = tk.Label(
        top_frame,
        text="Red: 05:00 | Blue: 05:00",
        font=("Arial", 11, "bold"),
        bg="#2c3e50",
        fg="white",
    )
    self.timer_label.pack(side=tk.RIGHT)

    self.status_label = tk.Label(
        root,
        text="Turn: Red Player - Select a piece to move",
        font=("Arial", 12, "bold"),
        bg="#2c3e50",
        fg="#e74c3c",
    )
    self.status_label.pack(pady=5)

    # Board Grid Container
    board_frame = tk.Frame(root, bg="#34495e", bd=4, relief="solid")
    board_frame.pack(pady=10)

    self.buttons = {}
    for r in range(8):
      for c in range(8):
        is_dark = (r + c) % 2 == 1
        bg_color = "#34495e" if is_dark else "#ecf0f1"

        btn = tk.Button(
            board_frame,
            text="",
            font=("Arial", 10, "bold"),
            width=6,
            height=3,
            bg=bg_color,
            command=lambda row=r, col=c: self.square_clicked(row, col),
        )
        btn.grid(row=r, column=c, padx=1, pady=1)
        self.buttons[(r, c)] = btn

    self.update_board_ui()
    self.update_timer()

  def init_board(self):
    # Place Blue pieces on top rows (0, 1, 2)
    for r in range(3):
      for c in range(8):
        if (r + c) % 2 == 1:
          self.board[r][c] = "b"

    # Place Red pieces on bottom rows (5, 6, 7)
    for r in range(5, 8):
      for c in range(8):
        if (r + c) % 2 == 1:
          self.board[r][c] = "r"

  def show_rules(self):
    rules = (
        "CHECKERS RULES:\n\n"
        "1. Click a piece to select it. Valid moves will turn GREEN!\n"
        "2. Click any GREEN square to execute your move.\n"
        "3. Jump over opponent pieces diagonally to capture them.\n"
        "4. Reach the opposite end of the board to crown a KING!"
    )
    messagebox.showinfo("How to Play - Checkers", rules)

  def get_legal_moves(self, sr, sc):
    piece = self.board[sr][sc]
    if piece == "":
      return []

    moves = []
    is_king = piece in ["R", "B"]
    is_red = piece in ["r", "R"]

    # Red moves UP (-1 row index), Blue moves DOWN (+1 row index)
    if is_king:
      row_directions = [-1, 1]
    else:
      row_directions = [-1] if is_red else [1]

    for dr in row_directions:
      for dc in [-1, 1]:
        # 1. Standard Step
        tr, tc = sr + dr, sc + dc
        if 0 <= tr < 8 and 0 <= tc < 8 and self.board[tr][tc] == "":
          moves.append((tr, tc))

        # 2. Jump Capture
        jtr, jtc = sr + (dr * 2), sc + (dc * 2)
        if 0 <= jtr < 8 and 0 <= jtc < 8 and self.board[jtr][jtc] == "":
          mid_piece = self.board[sr + dr][sc + dc]
          if mid_piece != "":
            is_opp = (is_red and mid_piece in ["b", "B"]) or (
                not is_red and mid_piece in ["r", "R"]
            )
            if is_opp:
              moves.append((jtr, jtc))

    return moves

  def square_clicked(self, r, c):
    if self.game_over:
      return

    piece = self.board[r][c]
    is_red_piece = piece in ["r", "R"]
    is_blue_piece = piece in ["b", "B"]

    # 1. Select one of player's own pieces
    if (self.turn == "Red" and is_red_piece) or (
        self.turn == "Blue" and is_blue_piece
    ):
      self.selected_piece = (r, c)
      self.valid_destinations = self.get_legal_moves(r, c)
      self.update_board_ui()
      return

    # 2. Move to a valid highlighted destination square
    if self.selected_piece and (r, c) in self.valid_destinations:
      sr, sc = self.selected_piece
      self.execute_move(sr, sc, r, c)
      self.selected_piece = None
      self.valid_destinations = []
      self.check_win_condition()
      if not self.game_over:
        self.finish_turn()

  def execute_move(self, sr, sc, tr, tc):
    piece = self.board[sr][sc]
    dr = tr - sr
    dc = tc - sc

    # Move piece
    self.board[tr][tc] = piece
    self.board[sr][sc] = ""

    # If jump capture (distance = 2), remove captured piece
    if abs(dr) == 2 and abs(dc) == 2:
      mid_r = (sr + tr) // 2
      mid_c = (sc + tc) // 2
      self.board[mid_r][mid_c] = ""

    # Promote to King
    if piece == "r" and tr == 0:
      self.board[tr][tc] = "R"
    elif piece == "b" and tr == 7:
      self.board[tr][tc] = "B"

  def check_win_condition(self):
    red_count = sum(row.count("r") + row.count("R") for row in self.board)
    blue_count = sum(row.count("b") + row.count("B") for row in self.board)

    if red_count == 0:
      self.game_over = True
      self.timer_running = False
      messagebox.showinfo("Game Over", "Blue Player Wins Checkers!")
      self.status_label.config(text="Winner: Blue Player!", fg="#3498db")
    elif blue_count == 0:
      self.game_over = True
      self.timer_running = False
      messagebox.showinfo("Game Over", "Red Player Wins Checkers!")
      self.status_label.config(text="Winner: Red Player!", fg="#e74c3c")

  def finish_turn(self):
    self.turn = "Blue" if self.turn == "Red" else "Red"
    color_code = "#e74c3c" if self.turn == "Red" else "#3498db"
    self.status_label.config(
        text=f"Turn: {self.turn} Player - Select a piece", fg=color_code
    )
    self.update_board_ui()

    if self.mode == "PvAI" and self.turn == "Blue" and not self.game_over:
      self.root.after(600, self.ai_move)

  def ai_move(self):
    if self.game_over:
      return

    all_possible = []
    for r in range(8):
      for c in range(8):
        if self.board[r][c] in ["b", "B"]:
          moves = self.get_legal_moves(r, c)
          for dest in moves:
            all_possible.append(((r, c), dest))

    if all_possible:
      (sr, sc), (tr, tc) = random.choice(all_possible)
      self.execute_move(sr, sc, tr, tc)
      self.check_win_condition()
      if not self.game_over:
        self.finish_turn()

  def update_board_ui(self):
    for r in range(8):
      for c in range(8):
        piece = self.board[r][c]
        is_dark = (r + c) % 2 == 1
        btn = self.buttons[(r, c)]

        # Highlight selected piece
        if self.selected_piece == (r, c):
          btn.config(bg="#f1c40f", fg="#2c3e50")
          continue

        # Highlight valid movement paths
        if (r, c) in self.valid_destinations:
          btn.config(text="MOVE", bg="#2ecc71", fg="white")
          continue

        # Standard board pieces
        if piece == "r":
          btn.config(text="RED", bg="#e74c3c", fg="white")
        elif piece == "R":
          btn.config(text="K-RED", bg="#c0392b", fg="#f1c40f")
        elif piece == "b":
          btn.config(text="BLUE", bg="#3498db", fg="white")
        elif piece == "B":
          btn.config(text="K-BLUE", bg="#2980b9", fg="#f1c40f")
        else:
          bg_col = "#2c3e50" if is_dark else "#ecf0f1"
          btn.config(text="", bg=bg_col)

  def update_timer(self):
    if self.timer_running and not self.game_over:
      if self.turn == "Red":
        if self.red_time > 0:
          self.red_time -= 1
      else:
        if self.blue_time > 0:
          self.blue_time -= 1

      r_min, r_sec = divmod(self.red_time, 60)
      b_min, b_sec = divmod(self.blue_time, 60)
      self.timer_label.config(
          text=f"Red: {r_min:02d}:{r_sec:02d} | Blue: {b_min:02d}:{b_sec:02d}"
      )

      if self.red_time == 0 or self.blue_time == 0:
        self.game_over = True
        self.timer_running = False
        loser = "Red" if self.red_time == 0 else "Blue"
        winner = "Blue" if loser == "Red" else "Red"
        messagebox.showinfo("Time Out!", f"{loser} ran out of time! {winner} wins!")

    self.root.after(1000, self.update_timer)


if __name__ == "__main__":
  mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
  root = tk.Tk()
  app = CheckersApp(root, mode)
  root.mainloop()
