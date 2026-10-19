import random
import sys
import tkinter as tk
from tkinter import messagebox


class ReversiApp:

  def __init__(self, root, mode="PvP"):
    self.root = root
    self.root.title(f"Reversi (Othello) - Mode: {mode}")
    self.root.geometry("680x780")
    self.root.config(bg="#1e272e")

    self.mode = mode
    self.turn = "Black"  # Black vs White (Black goes first)
    self.game_over = False

    # 8x8 Board setup: "" = empty, "Black" = Black disc, "White" = White disc
    self.board = [["" for _ in range(8)] for _ in range(8)]
    self.init_board()

    # Timers (300 seconds / 5 mins)
    self.black_time = 300
    self.white_time = 300
    self.timer_running = True

    # Top Control Bar
    top_frame = tk.Frame(root, bg="#1e272e")
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
        text="Black: 05:00 | White: 05:00",
        font=("Arial", 11, "bold"),
        bg="#1e272e",
        fg="white",
    )
    self.timer_label.pack(side=tk.RIGHT)

    self.score_label = tk.Label(
        root,
        text="Black: 2 | White: 2",
        font=("Arial", 12, "bold"),
        bg="#1e272e",
        fg="#ffdd59",
    )
    self.score_label.pack(pady=3)

    self.status_label = tk.Label(
        root,
        text="Turn: Black Player - Click a highlighted green tile to place disc",
        font=("Arial", 12, "bold"),
        bg="#1e272e",
        fg="#3498db",
    )
    self.status_label.pack(pady=5)

    # Board Grid Container
    board_frame = tk.Frame(root, bg="#2c3e50", bd=4, relief="solid")
    board_frame.pack(pady=10)

    self.buttons = {}
    for r in range(8):
      for c in range(8):
        btn = tk.Button(
            board_frame,
            text="",
            font=("Arial", 10, "bold"),
            width=6,
            height=3,
            bg="#27ae60",
            command=lambda row=r, col=c: self.square_clicked(row, col),
        )
        btn.grid(row=r, column=c, padx=1, pady=1)
        self.buttons[(r, c)] = btn

    self.update_board_ui()
    self.update_timer()

  def init_board(self):
    # Standard Reversi center setup
    self.board[3][3] = "White"
    self.board[3][4] = "Black"
    self.board[4][3] = "Black"
    self.board[4][4] = "White"

  def show_rules(self):
    rules = (
        "REVERSI (OTHELLO) RULES:\n\n"
        "1. Valid placement squares are highlighted in GREEN.\n"
        "2. Placing your disc traps opponent discs horizontally, vertically, or diagonally.\n"
        "3. Trapped opponent discs flip over to your color.\n"
        "4. If you have no valid moves, your turn is skipped.\n"
        "5. Player with the most discs at the end wins!"
    )
    messagebox.showinfo("How to Play - Reversi", rules)

  def get_flips(self, r, c, player):
    if self.board[r][c] != "":
      return []

    opponent = "White" if player == "Black" else "Black"
    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1),
    ]
    all_flips = []

    for dr, dc in directions:
      curr_r, curr_r_path = r + dr, []
      curr_c = c + dc

      while 0 <= curr_r < 8 and 0 <= curr_c < 8:
        target = self.board[curr_r][curr_c]
        if target == opponent:
          curr_r_path.append((curr_r, curr_c))
        elif target == player:
          if curr_r_path:
            all_flips.extend(curr_r_path)
          break
        else:
          break
        curr_r += dr
        curr_c += dc

    return all_flips

  def get_valid_moves(self, player):
    valid = []
    for r in range(8):
      for c in range(8):
        if self.get_flips(r, c, player):
          valid.append((r, c))
    return valid

  def square_clicked(self, r, c):
    if self.game_over:
      return

    valid_moves = self.get_valid_moves(self.turn)
    if (r, c) not in valid_moves:
      messagebox.showwarning("Invalid Move", "You must place on a valid green square!")
      return

    # Execute move
    flips = self.get_flips(r, c, self.turn)
    self.board[r][c] = self.turn
    for fr, fc in flips:
      self.board[fr][fc] = self.turn

    self.update_board_ui()
    self.check_game_state()

  def check_game_state(self):
    self.turn = "White" if self.turn == "Black" else "Black"

    # Check if current player has valid moves; if not, pass turn back
    valid_moves = self.get_valid_moves(self.turn)
    if not valid_moves:
      self.turn = "White" if self.turn == "Black" else "Black"
      valid_moves = self.get_valid_moves(self.turn)
      if not valid_moves:
        # Game Over (neither player can move)
        self.game_over = True
        self.timer_running = False
        black_score = sum(row.count("Black") for row in self.board)
        white_score = sum(row.count("White") for row in self.board)

        if black_score > white_score:
          msg = f"Game Over! Black wins ({black_score} to {white_score})"
        elif white_score > black_score:
          msg = f"Game Over! White wins ({white_score} to {black_score})"
        else:
          msg = f"Game Over! It's a tie ({black_score} to {white_score})"

        messagebox.showinfo("🏆 Game Over!", msg)
        self.status_label.config(text=msg, fg="#f1c40f")
        return
      else:
        messagebox.showinfo(
            "Turn Passed",
            f"No valid moves available! Turn passes back to {self.turn}.",
        )

    color_code = "#3498db" if self.turn == "Black" else "#ecf0f1"
    self.status_label.config(
        text=f"Turn: {self.turn} Player - Place your disc", fg=color_code
    )
    self.update_board_ui()

    if self.mode == "PvAI" and self.turn == "White" and not self.game_over:
      self.root.after(600, self.ai_move)

  def ai_move(self):
    if self.game_over:
      return

    valid_moves = self.get_valid_moves("White")
    if valid_moves:
      r, c = random.choice(valid_moves)
      flips = self.get_flips(r, c, "White")
      self.board[r][c] = "White"
      for fr, fc in flips:
        self.board[fr][fc] = "White"

      self.update_board_ui()
      self.check_game_state()

  def update_board_ui(self):
    black_score = sum(row.count("Black") for row in self.board)
    white_score = sum(row.count("White") for row in self.board)
    self.score_label.config(text=f"Black Discs: {black_score} | White Discs: {white_score}")

    valid_moves = self.get_valid_moves(self.turn)

    for r in range(8):
      for c in range(8):
        piece = self.board[r][c]
        btn = self.buttons[(r, c)]

        if piece == "Black":
          btn.config(text="BLACK", bg="#2c3e50", fg="white")
        elif piece == "White":
          btn.config(text="WHITE", bg="#ecf0f1", fg="#2c3e50")
        elif (r, c) in valid_moves and not (self.mode == "PvAI" and self.turn == "White"):
          btn.config(text="•", bg="#2ecc71", fg="white")
        else:
          btn.config(text="", bg="#27ae60")

  def update_timer(self):
    if self.timer_running and not self.game_over:
      if self.turn == "Black":
        if self.black_time > 0:
          self.black_time -= 1
      else:
        if self.white_time > 0:
          self.white_time -= 1

      b_min, b_sec = divmod(self.black_time, 60)
      w_min, w_sec = divmod(self.white_time, 60)
      self.timer_label.config(
          text=f"Black: {b_min:02d}:{b_sec:02d} | White: {w_min:02d}:{w_sec:02d}"
      )

      if self.black_time == 0 or self.white_time == 0:
        self.game_over = True
        self.timer_running = False
        loser = "Black" if self.black_time == 0 else "White"
        winner = "White" if loser == "Black" else "Black"
        messagebox.showinfo("Time Out!", f"{loser} ran out of time! {winner} wins!")

    self.root.after(1000, self.update_timer)


if __name__ == "__main__":
  mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
  root = tk.Tk()
  app = ReversiApp(root, mode)
  root.mainloop()
