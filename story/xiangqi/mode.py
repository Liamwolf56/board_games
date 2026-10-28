import json
import os
import random
import tkinter as tk
from tkinter import messagebox

KING_DATA = {
    "game": "Chess",
    "title": "Grandmaster Dark King (Final Boss)",
    "intro": (
        "You have reached the final throne! Checkmate is inevitable, and my"
        " shadow royal court will end your campaign here!"
    ),
    "victory": (
        "CHECKMATE! Your king falls before the supreme strategic mastery of"
        " shadows! Campaign reset!"
    ),
    "defeat": (
        "IMPOSSIBLE! A final sacrifice shattered my royal defenses! You are"
        " the ultimate champion of the Realm of 15 Kings!"
    ),
}


class StoryChessBoss:

  def __init__(self, root):
    self.root = root
    self.root.title(f"Story Mode: {KING_DATA['title']}")
    self.root.geometry("480x580")
    self.root.config(bg="#1e272e")

    self.selected = None
    self.turn = "Player"
    self.game_over = False

    self.board = [
        ["r", "n", "q", "k", "r"],
        ["p", "p", "p", "p", "p"],
        [".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P"],
        ["R", "N", "Q", "K", "R"],
    ]

    self.symbols = {
        "K": "♔",
        "Q": "♕",
        "R": "♖",
        "N": "♘",
        "P": "♙",
        "k": "♚",
        "q": "♛",
        "r": "♜",
        "n": "♞",
        "p": "♟",
        ".": "",
    }

    tk.Label(
        root,
        text=f"👑 {KING_DATA['title']}",
        font=("Arial", 14, "bold"),
        fg="#ffdd59",
        bg="#1e272e",
    ).pack(pady=10)

    d_frame = tk.Frame(root, bg="#2c3e50", padx=10, pady=8)
    d_frame.pack(fill=tk.X, padx=15, pady=5)
    tk.Label(
        d_frame,
        text=f"💬 \"{KING_DATA['intro']}\"",
        font=("Arial", 10, "italic"),
        fg="#00d8d6",
        bg="#2c3e50",
        wraplength=420,
    ).pack()

    self.status_lbl = tk.Label(
        root,
        text="Final Stage: Your Turn (White Pieces ♔) — Select a Piece",
        font=("Arial", 11, "bold"),
        fg="white",
        bg="#1e272e",
    )
    self.status_lbl.pack(pady=5)

    grid_frame = tk.Frame(root, bg="#2c3e50", padx=10, pady=10)
    grid_frame.pack(pady=5)

    self.grid_buttons = []
    for r in range(5):
      row_btns = []
      for c in range(5):
        bg_col = "#eeeed2" if (r + c) % 2 == 0 else "#769656"
        btn = tk.Button(
            grid_frame,
            text=self.symbols[self.board[r][c]],
            font=("Arial", 18, "bold"),
            width=3,
            height=1,
            bg=bg_col,
            command=lambda row=r, col=c: self.on_cell_click(row, col),
        )
        btn.grid(row=r, column=c, padx=2, pady=2)
        row_btns.append(btn)
      self.grid_buttons.append(row_btns)

  def on_cell_click(self, r, c):
    if self.game_over or self.turn != "Player":
      return
    piece = self.board[r][c]
    if self.selected is None:
      if piece != "." and piece.isupper():
        self.selected = (r, c)
        self.grid_buttons[r][c].config(bg="#f1c40f")
    else:
      sr, sc = self.selected
      sel_piece = self.board[sr][sc]
      if (sr, sc) == (r, c):
        self.deselect()
        return
      elif piece != "." and piece.isupper():
        self.deselect()
        self.selected = (r, c)
        self.grid_buttons[r][c].config(bg="#f1c40f")
        return

      captured = self.board[r][c]
      self.board[r][c] = sel_piece
      self.board[sr][sc] = "."
      self.deselect()
      self.update_board_ui()

      if captured == "k":
        self.handle_win()
        return

      self.turn = "AI"
      self.status_lbl.config(text="Grandmaster Dark King is contemplating...")
      self.root.after(700, self.ai_move)

  def deselect(self):
    if self.selected:
      sr, sc = self.selected
      bg_col = "#eeeed2" if (sr + sc) % 2 == 0 else "#769656"
      self.grid_buttons[sr][sc].config(bg=bg_col)
      self.selected = None
    self.status_lbl.config(text="Final Stage: Your Turn (White Pieces ♔)")

  def ai_move(self):
    if self.game_over:
      return
    ai_pieces = [
        (r, c)
        for r in range(5)
        for c in range(5)
        if self.board[r][c] != "." and self.board[r][c].islower()
    ]
    if not ai_pieces:
      self.handle_win()
      return

    moves = []
    for sr, sc in ai_pieces:
      for dr in range(-1, 2):
        for dc in range(-1, 2):
          tr, tc = sr + dr, sc + dc
          if 0 <= tr < 5 and 0 <= tc < 5:
            target = self.board[tr][tc]
            if target == "." or target.isupper():
              priority = 2 if target == "K" else (1 if target.isupper() else 0)
              moves.append((priority, (sr, sc), (tr, tc)))

    if not moves:
      self.handle_win()
      return

    moves.sort(key=lambda x: x[0], reverse=True)
    best_move = moves[0] if moves[0][0] > 0 else random.choice(moves)
    _, (sr, sc), (tr, tc) = best_move
    captured = self.board[tr][tc]
    self.board[tr][tc] = self.board[sr][sc]
    self.board[sr][sc] = "."
    self.update_board_ui()

    if captured == "K":
      self.handle_loss()
      return

    self.turn = "Player"
    self.status_lbl.config(
        text="Final Stage: Your Turn (White Pieces ♔) — Select a Piece"
    )

  def update_board_ui(self):
    for r in range(5):
      for c in range(5):
        piece = self.board[r][c]
        bg_col = "#eeeed2" if (r + c) % 2 == 0 else "#769656"
        self.grid_buttons[r][c].config(text=self.symbols[piece], bg=bg_col)

  def handle_win(self):
    self.game_over = True
    messagebox.showinfo(
        "ULTIMATE VICTORY! 🏆👑",
        f"You have conquered the Realm of 15 Kings!\n\n\"{KING_DATA['defeat']}\"",
    )
    self.update_save(win=True)
    self.root.destroy()

  def handle_loss(self):
    self.game_over = True
    messagebox.showerror(
        "PERMADEATH! 💀 Campaign Reset",
        f"{KING_DATA['title']} laughs from the shadow throne:\n\n\"{KING_DATA['victory']}\"",
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
        data["current_stage_idx"] = data["current_stage_idx"] + 1 if win else 0
        with open(save_path, "w") as f:
          json.dump(data, f)
      except Exception:
        pass


if __name__ == "__main__":
  root = tk.Tk()
  app = StoryChessBoss(root)
  root.mainloop()
