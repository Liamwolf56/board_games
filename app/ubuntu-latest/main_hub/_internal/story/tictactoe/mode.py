import json
import os
import random
import tkinter as tk
from tkinter import messagebox

KING_DATA = {
    "game": "Tic-Tac-Toe",
    "title": "King Ultimate Gridlock",
    "intro": (
        "Bask in the perfection of my endless ties! You shall never break this"
        " gridlock!"
    ),
    "victory": (
        "Hahaha! As expected, another fool trapped in my infinite draw!"
    ),
    "defeat": (
        "CURSES! A mark was placed where it shouldn't be... My gridlock is"
        " shattered!"
    ),
}


class StoryTicTacToe:

  def __init__(self, root):
    self.root = root
    self.root.title(f"Story Mode: {KING_DATA['title']}")
    self.root.geometry("440x560")
    self.root.config(bg="#1e272e")

    self.board = [""] * 9
    self.game_over = False

    # Display King Title Banner
    tk.Label(
        root,
        text=f"👑 {KING_DATA['title']}",
        font=("Arial", 14, "bold"),
        fg="#ffdd59",
        bg="#1e272e",
    ).pack(pady=10)

    # King Dialogue Header
    dialogue_frame = tk.Frame(root, bg="#2c3e50", padx=10, pady=10)
    dialogue_frame.pack(fill=tk.X, padx=15, pady=5)
    tk.Label(
        dialogue_frame,
        text=f"💬 \"{KING_DATA['intro']}\"",
        font=("Arial", 10, "italic"),
        fg="#00d8d6",
        bg="#2c3e50",
        wraplength=380,
    ).pack()

    # Status Label
    self.status_lbl = tk.Label(
        root,
        text="Your Turn (X) vs Balanced AI (O)",
        font=("Arial", 10, "bold"),
        fg="white",
        bg="#1e272e",
    )
    self.status_lbl.pack(pady=5)

    # Board Grid
    grid_frame = tk.Frame(root, bg="#1e272e")
    grid_frame.pack(pady=10)

    self.buttons = []
    for i in range(9):
      btn = tk.Button(
          grid_frame,
          text="",
          font=("Arial", 22, "bold"),
          width=4,
          height=2,
          bg="#34495e",
          fg="white",
          command=lambda idx=i: self.make_move(idx),
      )
      btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
      self.buttons.append(btn)

  def make_move(self, idx):
    if self.board[idx] == "" and not self.game_over:
      # Player Move (X)
      self.board[idx] = "X"
      self.buttons[idx].config(text="X", fg="#0984e3")

      if self.check_winner(self.board, "X"):
        self.handle_player_win()
        return
      elif "" not in self.board:
        self.handle_player_loss("Endless Tie - King's Gridlock holds!")
        return

      self.status_lbl.config(text="King Gridlock is thinking...")
      self.root.update_idletasks()
      self.root.after(300, self.ai_move)

  def ai_move(self):
    if self.game_over:
      return

    empty_indices = [i for i, spot in enumerate(self.board) if spot == ""]
    if not empty_indices:
      return

    # Balanced AI: 70% smart play, 30% casual opening to let the player win
    if random.random() < 0.3:
      best_move = random.choice(empty_indices)
    else:
      best_score = -float("inf")
      best_move = -1
      for i in empty_indices:
        self.board[i] = "O"
        score = self.minimax(self.board, 0, False)
        self.board[i] = ""
        if score > best_score:
          best_score = score
          best_move = i

    if best_move != -1:
      self.board[best_move] = "O"
      self.buttons[best_move].config(text="O", fg="#e74c3c")

      if self.check_winner(self.board, "O"):
        self.handle_player_loss("King Ultimate Gridlock outsmarted you!")
        return
      elif "" not in self.board:
        self.handle_player_loss("Endless Tie - King's Gridlock holds!")
        return

    self.status_lbl.config(text="Your Turn (X)")

  def minimax(self, board, depth, is_maximizing):
    if self.check_winner(board, "O"):
      return 10 - depth
    if self.check_winner(board, "X"):
      return depth - 10
    if "" not in board:
      return 0

    if is_maximizing:
      max_eval = -float("inf")
      for i in range(9):
        if board[i] == "":
          board[i] = "O"
          eval_score = self.minimax(board, depth + 1, False)
          board[i] = ""
          max_eval = max(max_eval, eval_score)
      return max_eval
    else:
      min_eval = float("inf")
      for i in range(9):
        if board[i] == "":
          board[i] = "X"
          eval_score = self.minimax(board, depth + 1, True)
          board[i] = ""
          min_eval = min(min_eval, eval_score)
      return min_eval

  def check_winner(self, board, player):
    wins = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),  # Rows
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),  # Columns
        (0, 4, 8),
        (2, 4, 6),  # Diagonals
    ]
    return any(
        board[a] == board[b] == board[c] == player for a, b, c in wins
    )

  def handle_player_win(self):
    self.game_over = True
    messagebox.showinfo(
        "VICTORY! 🏆",
        f"{KING_DATA['title']} cries out in defeat:\n\n\"{KING_DATA['defeat']}\"",
    )
    self.update_save(win=True)
    self.root.destroy()

  def handle_player_loss(self, reason):
    self.game_over = True
    messagebox.showerror(
        "PERMADEATH! 💀 Game Over",
        f"{KING_DATA['title']} gloats over your defeat:\n\n\"{KING_DATA['victory']}\"\n\nRun"
        " Reset!",
    )
    self.update_save(win=False)
    self.root.destroy()

  def update_save(self, win):
    save_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "progress.json",
    )
    if os.path.exists(save_path):
      try:
        with open(save_path, "r") as f:
          data = json.load(f)

        if win:
          data["current_stage_idx"] += 1
        else:
          data["current_stage_idx"] = 0  # Ironman Permadeath reset

        with open(save_path, "w") as f:
          json.dump(data, f)
      except Exception:
        pass


if __name__ == "__main__":
  root = tk.Tk()
  app = StoryTicTacToe(root)
  root.mainloop()
