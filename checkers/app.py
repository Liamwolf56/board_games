import random
import sys
import tkinter as tk
from tkinter import messagebox


class CheckersApp:

  def __init__(self, root, mode="PvP"):
    self.root = root
    self.root.title(f"Checkers - Mode: {mode}")
    self.root.geometry("640x740")
    self.root.config(bg="#2c3e50")

    self.mode = mode
    self.turn = "Red"  # Red vs Blue
    self.game_over = False
    self.selected_piece = None  # (r, c)

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
        # Dark squares are playable (r + c is odd)
        is_dark = (r + c) % 2 == 1
        bg_color = "#4a6572" if is_dark else "#ecf0f1"

        btn = tk.Button(
            board_frame,
            text="",
            font=("Arial", 16, "bold"),
            width=4,
            height=2,
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
        "1. Click one of your pieces to select it, then click an empty diagonal square to move.\n"
        "2. Jump over opponent pieces diagonally to capture them.\n"
        "3. Reach the opposite end of the board to crown your piece into a KING (👑),\n"
        "   which can move and jump both forwards and backwards!\n"
        "4. Capture all opponent pieces to win!"
    )
    messagebox.showinfo("How to Play - Checkers", rules)

  def square_clicked(self, r, c):
    if self.game_over:
      return

    piece = self.board[r][c]
    is_red_piece = piece in ["r", "R"]
    is_blue_piece = piece in ["b", "B"]

    # If clicking own piece, select it
    if (self.turn == "Red" and is_red_piece) or (
        self.turn == "Blue" and is_blue_piece
    ):
      self.selected_piece = (r, c)
      self.update_board_ui()
      # Highlight selected square
      self.buttons[(r, c)].config(bg="#f1c40f")
      return

    # If a piece is selected and clicking an empty dark square, attempt move
    if self.selected_piece and piece == "":
      sr, sc = self.selected_piece
      if self.validate_and_execute_move(sr, sc, r, c):
        self.selected_piece = None
        self.check_win_condition()
        if not self.game_over:
          self.finish_turn()
      else:
        messagebox.showwarning("Invalid Move", "Illegal checkers move!")

  def validate_and_execute_move(self, sr, sc, tr, tc):
    piece = self.board[sr][sc]
    dr = tr - sr
    dc = tc - sc

    is_king = piece in ["R", "B"]
    is_red = piece in ["r", "R"]

    # Direction check for normal pieces
    if not is_king:
      if is_red and dr > 0:
        return False  # Red moves 'up' (decreasing row index)
      if not is_red and dr < 0:
        return False  # Blue moves 'down' (increasing row index)

    # Simple diagonal move (distance 1)
    if abs(dr) == 1 and abs(dc) == 1:
      self.board[tr][tc] = piece
      self.board[sr][sc] = ""
      self.promote_if_needed(tr, tc)
      return True

    # Jump capture move (distance 2)
    if abs(dr) == 2 and abs(dc) == 2:
      mid_r = (sr + tr) // 2
      mid_c = (sc + tc) // 2
      jumped_piece = self.board[mid_r][mid_c]

      if jumped_piece == "":
        return False

      is_opponent = (is_red and jumped_piece in ["b", "B"]) or (
          not is_red and jumped_piece in ["r", "R"]
      )
      if is_opponent:
        self.board[tr][tc] = piece
        self.board[sr][sc] = ""
        self.board[mid_r][mid_c] = ""  # Remove captured piece
        self.promote_if_needed(tr, tc)
        return True

    return False

  def promote_if_needed(self, r, c):
    piece = self.board[r][c]
    if piece == "r" and r == 0:
      self.board[r][c] = "R"
    elif piece == "b" and r == 7:
      self.board[r][c] = "B"

  def check_win_condition(self):
    red_count = sum(
        row.count("r") + row.count("R") for row in self.board
    )
    blue_count = sum(
        row.count("b") + row.count("B") for row in self.board
    )

    if red_count == 0:
      self.game_over = True
      self.timer_running = False
      messagebox.showinfo("🏆 Game Over!", "Blue Player Wins Checkers!")
      self.status_label.config(text="Winner: Blue Player!", fg="#3498db")
    elif blue_count == 0:
      self.game_over = True
      self.timer_running = False
      messagebox.showinfo("🏆 Game Over!", "Red Player Wins Checkers!")
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

    # Find all blue pieces and possible moves
    valid_moves = []
    for r in range(8):
      for c in range(8):
        if self.board[r][c] in ["b", "B"]:
          piece = self.board[r][c]
          is_king = piece == "B"
          directions = [-1, 1] if is_king else [1]

          for dr in directions:
            for dc in [-1, 1]:
              tr, tc = r + dr, c + dc
              if 0 <= tr < 8 and 0 <= tc < 8 and self.board[tr][tc] == "":
                valid_moves.append(((r, c), (tr, tc)))
              # Check jump
              jtr, jtc = r + (dr * 2), c + (dc * 2)
              if 0 <= jtr < 8 and 0 <= jtc < 8 and self.board[jtr][jtc] == "":
                mid_piece = self.board[r + dr][c + dc]
                if mid_piece in ["r", "R"]:
                  valid_moves.append(((r, c), (jtr, jtc)))

    if valid_moves:
      (sr, sc), (tr, tc) = random.choice(valid_moves)
      self.validate_and_execute_move(sr, sc, tr, tc)
      self.update_board_ui()
      self.check_win_condition()
      if not self.game_over:
        self.finish_turn()
    else:
      self.game_over = True
      self.timer_running = False
      messagebox.showinfo("Game Over", "Blue has no moves left! Red wins!")

  def update_board_ui(self):
    for r in range(8):
      for c in range(8):
        piece = self.board[r][c]
        is_dark = (r + c) % 2 == 1
        bg_color = "#4a6572" if is_dark else "#ecf0f1"

        txt = ""
        if piece == "r":
          txt = "🔴"
        elif piece == "R":
          txt = "👑RED"
        elif piece == "b":
          txt = "🔵"
        elif piece == "B":
          txt = "👑BLUE"

        self.buttons[(r, c)].config(text=txt, bg=bg_color)

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
