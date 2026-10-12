import sys
import tkinter as tk
from tkinter import messagebox


class ShogiApp:

  def __init__(self, root, mode="PvP"):
    self.root = root
    self.root.title(f"Shogi (Japanese Chess) - Mode: {mode}")
    self.root.geometry("700x900")
    self.root.config(bg="#2c3e50")

    self.mode = mode
    self.selected_square = None
    self.turn = "Sente"  # Sente (Black) vs Gote (White)
    self.game_over = False
    self.valid_moves = []

    # Timer variables (300 seconds / 5 minutes per player)
    self.sente_time = 300
    self.gote_time = 300
    self.timer_running = True

    self.hands = {"Sente": [], "Gote": []}

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

    # Timer label on the top right
    self.timer_label = tk.Label(
        top_frame,
        text="Sente: 05:00 | Gote: 05:00",
        font=("Arial", 11, "bold"),
        bg="#2c3e50",
        fg="white",
    )
    self.timer_label.pack(side=tk.RIGHT)

    self.status_label = tk.Label(
        root,
        text="Turn: Sente (Black) - Select a piece",
        font=("Arial", 11, "bold"),
        bg="#2c3e50",
        fg="#1abc9c",
    )
    self.status_label.pack(pady=5)

    hands_frame = tk.Frame(root, bg="#34495e", bd=2, relief="solid")
    hands_frame.pack(fill=tk.X, padx=20, pady=5)

    self.gote_hand_label = tk.Label(
        hands_frame,
        text="Gote Hand (Captured): None",
        bg="#34495e",
        fg="#e74c3c",
        font=("Arial", 10),
    )
    self.gote_hand_label.pack(anchor="w", padx=5, pady=2)

    self.sente_hand_label = tk.Label(
        hands_frame,
        text="Sente Hand (Captured): None",
        bg="#34495e",
        fg="#2ecc71",
        font=("Arial", 10),
    )
    self.sente_hand_label.pack(anchor="w", padx=5, pady=2)

    self.board_frame = tk.Frame(root, bg="#1abc9c", bd=3, relief="solid")
    self.board_frame.pack(pady=10)

    self.setup_board_data()
    self.create_board_ui()
    self.update_timer()

  def show_rules(self):
    rules = (
        "SHOGI RULES & TIMER:\n\n"
        "• Green squares show valid traditional moves.\n"
        "• Watch your clock! Each player has 5 minutes.\n"
        "• Goal: Capture the opposing King (K / k)."
    )
    messagebox.showinfo("How to Play - Shogi", rules)

  def setup_board_data(self):
    self.board = [
        ["l", "n", "s", "g", "k", "g", "s", "n", "l"],
        [".", "r", ".", ".", ".", ".", ".", "b", "."],
        ["p", "p", "p", "p", "p", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P", "P"],
        [".", "B", ".", ".", ".", ".", ".", "R", "."],
        ["L", "N", "S", "G", "K", "G", "S", "N", "L"],
    ]

  def create_board_ui(self):
    self.buttons = {}
    for r in range(9):
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
    is_sente = piece.isupper()
    p_lower = piece.lower()
    fwd = -1 if is_sente else 1

    if p_lower == "p":
      nr, nc = r + fwd, c
      if 0 <= nr < 9 and 0 <= nc < 9:
        target = self.board[nr][nc]
        if target == "." or target.isupper() != is_sente:
          moves.append((nr, nc))
    elif p_lower == "k":
      for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
          if dr == 0 and dc == 0:
            continue
          nr, nc = r + dr, c + dc
          if 0 <= nr < 9 and 0 <= nc < 9:
            target = self.board[nr][nc]
            if target == "." or target.isupper() != is_sente:
              moves.append((nr, nc))
    elif p_lower == "r":
      for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        step = 1
        while True:
          nr, nc = r + dr * step, c + dc * step
          if not (0 <= nr < 9 and 0 <= nc < 9):
            break
          target = self.board[nr][nc]
          if target == ".":
            moves.append((nr, nc))
          else:
            if target.isupper() != is_sente:
              moves.append((nr, nc))
            break
          step += 1
    elif p_lower == "b":
      for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        step = 1
        while True:
          nr, nc = r + dr * step, c + dc * step
          if not (0 <= nr < 9 and 0 <= nc < 9):
            break
          target = self.board[nr][nc]
          if target == ".":
            moves.append((nr, nc))
          else:
            if target.isupper() != is_sente:
              moves.append((nr, nc))
            break
          step += 1
    elif p_lower == "g":
      for dr, dc in [
          (fwd, 0),
          (0, -1),
          (0, 1),
          (-fwd, 0),
          (fwd, -1),
          (fwd, 1),
      ]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 9 and 0 <= nc < 9:
          target = self.board[nr][nc]
          if target == "." or target.isupper() != is_sente:
            moves.append((nr, nc))
    elif p_lower == "s":
      for dr, dc in [(fwd, -1), (fwd, 0), (fwd, 1), (-fwd, -1), (-fwd, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 9 and 0 <= nc < 9:
          target = self.board[nr][nc]
          if target == "." or target.isupper() != is_sente:
            moves.append((nr, nc))
    elif p_lower == "l":
      step = 1
      while True:
        nr, nc = r + fwd * step, c
        if not (0 <= nr < 9 and 0 <= nc < 9):
          break
        target = self.board[nr][nc]
        if target == ".":
          moves.append((nr, nc))
        else:
          if target.isupper() != is_sente:
            moves.append((nr, nc))
          break
        step += 1
    elif p_lower == "n":
      for dc in [-1, 1]:
        nr, nc = r + (2 * fwd), c + dc
        if 0 <= nr < 9 and 0 <= nc < 9:
          target = self.board[nr][nc]
          if target == "." or target.isupper() != is_sente:
            moves.append((nr, nc))

    return moves

  def square_clicked(self, r, c):
    if self.game_over:
      return
    piece = self.board[r][c]

    if self.selected_square is None:
      if piece != ".":
        is_sente_piece = piece.isupper()
        current_is_sente = self.turn == "Sente"
        if (current_is_sente and is_sente_piece) or (
            not current_is_sente and not is_sente_piece
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
          messagebox.showinfo("🏆 Game Over!", f"{self.turn} captured the King!")
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
    self.turn = "Gote" if self.turn == "Sente" else "Sente"
    color_code = "#2ecc71" if self.turn == "Sente" else "#e74c3c"
    self.status_label.config(
        text=f"Turn: {self.turn} ({'Black' if self.turn=='Sente' else 'White'})",
        fg=color_code,
    )
    self.update_ui()

    if self.mode == "PvAI" and self.turn == "Gote" and not self.game_over:
      self.root.after(600, self.ai_move)

  def ai_move(self):
    import random

    gote_pieces = []
    for r in range(9):
      for c in range(9):
        p = self.board[r][c]
        if p != "." and p.islower():
          moves = self.get_valid_moves(r, c, p)
          if moves:
            gote_pieces.append((r, c, moves))

    if gote_pieces:
      fr, fc, moves = random.choice(gote_pieces)
      tr, tc = random.choice(moves)
      target = self.board[tr][tc]
      self.board[tr][tc] = self.board[fr][fc]
      self.board[fr][fc] = "."

      if target.lower() == "k":
        self.game_over = True
        self.timer_running = False
        messagebox.showinfo("🏆 Game Over!", "Gote AI captured the King!")
        return

    self.finish_turn()

  def update_timer(self):
    if self.timer_running and not self.game_over:
      if self.turn == "Sente":
        if self.sente_time > 0:
          self.sente_time -= 1
      else:
        if self.gote_time > 0:
          self.gote_time -= 1

      s_min, s_sec = divmod(self.sente_time, 60)
      g_min, g_sec = divmod(self.gote_time, 60)
      self.timer_label.config(
          text=f"Sente: {s_min:02d}:{s_sec:02d} | Gote: {g_min:02d}:{g_sec:02d}"
      )

      if self.sente_time == 0 or self.gote_time == 0:
        self.game_over = True
        self.timer_running = False
        loser = "Sente" if self.sente_time == 0 else "Gote"
        winner = "Gote" if loser == "Sente" else "Sente"
        messagebox.showinfo("Time Out!", f"{loser} ran out of time! {winner} wins!")

    self.root.after(1000, self.update_timer)

  def update_ui(self):
    for r in range(9):
      for c in range(9):
        bg_color = "#e67e22" if (r + c) % 2 == 0 else "#d35400"
        if self.selected_square == (r, c):
          bg_color = "#7b68ee"
        elif (r, c) in self.valid_moves:
          bg_color = "#2ecc71"

        txt = self.board[r][c] if self.board[r][c] != "." else ""
        fg_col = "#ffffff" if self.board[r][c].isupper() else "#111111"
        self.buttons[(r, c)].config(text=txt, bg=bg_color, fg=fg_col)

    sente_str = (
        ", ".join(self.hands["Sente"]).upper()
        if self.hands["Sente"]
        else "None"
    )
    gote_str = (
        ", ".join(self.hands["Gote"]).upper() if self.hands["Gote"] else "None"
    )
    self.sente_hand_label.config(text=f"Sente Hand (Captured): {sente_str}")
    self.gote_hand_label.config(text=f"Gote Hand (Captured): {gote_str}")


if __name__ == "__main__":
  mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
  root = tk.Tk()
  app = ShogiApp(root, mode)
  root.mainloop()
