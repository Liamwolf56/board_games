import json
import os
import sys
import tkinter as tk
from tkinter import messagebox

# Add parent directory to path to import arcade connect_4 module
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from connect_4.app import Connect4App

KING_DATA = {
    "game": "Connect 4",
    "title": "Grid Master Connect",
    "intro": (
        "Four in a row is my domain! Drop your discs carefully, for every"
        " column belongs to my grid!"
    ),
    "victory": (
        "Grid supremacy! Your pieces were blocked and left disconnected!"
    ),
    "defeat": (
        "IMPOSSIBLE! You connected four pieces across the grid and shattered"
        " my defenses!"
    ),
}


class StoryConnect4Wrapper:

  def __init__(self, root):
    self.root = root
    self.root.title(f"Story Mode: {KING_DATA['title']}")
    self.root.geometry("520x160")
    self.root.config(bg="#1e272e")

    # Story Header Banner
    header = tk.Frame(root, bg="#2c3e50", padx=10, pady=10)
    header.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    tk.Label(
        header,
        text=f"👑 {KING_DATA['title']}",
        font=("Arial", 14, "bold"),
        fg="#ffdd59",
        bg="#2c3e50",
    ).pack()
    tk.Label(
        header,
        text=f"💬 \"{KING_DATA['intro']}\"",
        font=("Arial", 10, "italic"),
        fg="#00d8d6",
        bg="#2c3e50",
        wraplength=460,
    ).pack(pady=5)

    # Launch actual Arcade Connect 4 App in a separate window in PvAI mode
    self.arcade_win = tk.Toplevel(root)
    self.arcade_app = Connect4App(self.arcade_win, mode="PvAI")

    # Intercept drop_piece to handle story win/loss hooks
    original_drop_piece = self.arcade_app.drop_piece

    def custom_drop_piece(col):
      if self.arcade_app.game_over:
        return

      target_row = -1
      for r in reversed(range(6)):
        if self.arcade_app.board[r][col] == "":
          target_row = r
          break

      if target_row != -1:
        self.arcade_app.board[target_row][col] = self.arcade_app.turn
        color_code = (
            "#e74c3c" if self.arcade_app.turn == "Red" else "#f1c40f"
        )
        self.arcade_app.buttons[(target_row, col)].config(bg=color_code)

        if self.arcade_app.check_win(target_row, col):
          self.arcade_app.game_over = True
          self.arcade_app.timer_running = False
          user_won = self.arcade_app.turn == "Red"

          try:
            if user_won:
              messagebox.showinfo(
                  "VICTORY! 🏆",
                  f"{KING_DATA['title']} cries out in defeat:\n\n\"{KING_DATA['defeat']}\"",
              )
              self.update_save(win=True)
            else:
              messagebox.showerror(
                  "PERMADEATH! 💀 Game Over",
                  f"{KING_DATA['title']} gloats over your defeat:\n\n\"{KING_DATA['victory']}\"\n\nRun"
                  " Reset!",
              )
              self.update_save(win=False)
          except Exception:
            pass

          try:
            self.arcade_win.destroy()
          except Exception:
            pass
          try:
            self.root.destroy()
          except Exception:
            pass
          return
        elif all(self.arcade_app.board[0][c] != "" for c in range(7)):
          self.arcade_app.game_over = True
          self.arcade_app.timer_running = False
          try:
            messagebox.showerror(
                "PERMADEATH! 💀 Game Over",
                f"{KING_DATA['title']} gloats over your defeat:\n\n\"{KING_DATA['victory']}\"\n\nRun"
                " Reset!",
            )
            self.update_save(win=False)
          except Exception:
            pass

          try:
            self.arcade_win.destroy()
          except Exception:
            pass
          try:
            self.root.destroy()
          except Exception:
            pass
          return
        else:
          self.arcade_app.turn = (
              "Yellow" if self.arcade_app.turn == "Red" else "Red"
          )
          next_color = (
              "#e74c3c" if self.arcade_app.turn == "Red" else "#f1c40f"
          )
          self.arcade_app.status_label.config(
              text=f"Turn: {self.arcade_app.turn} Player", fg=next_color
          )

          if (
              self.arcade_app.mode == "PvAI"
              and self.arcade_app.turn == "Yellow"
              and not self.arcade_app.game_over
          ):
            self.arcade_app.root.after(500, self.arcade_app.ai_move)

    self.arcade_app.drop_piece = custom_drop_piece
    self.arcade_win.protocol("WM_DELETE_WINDOW", lambda: self.root.destroy())

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
          data["current_stage_idx"] = 0

        with open(save_path, "w") as f:
          json.dump(data, f)
      except Exception:
        pass


if __name__ == "__main__":
  root = tk.Tk()
  app = StoryConnect4Wrapper(root)
  root.mainloop()
