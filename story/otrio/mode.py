import json
import os
import sys
import tkinter as tk
from tkinter import messagebox

# Add parent directory to path to import arcade otrio module
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from otrio.app import OtrioApp

KING_DATA = {
    "game": "Otrio",
    "title": "Ringmaster Triad",
    "intro": (
        "Concentric rings and aligned triads obey my command! You cannot match"
        " my overlapping sequences!"
    ),
    "victory": (
        "Triad triumph! Your rings have been completely outmatched and"
        " blocked!"
    ),
    "defeat": (
        "IMPOSSIBLE! My concentric rings have been completely aligned and"
        " shattered!"
    ),
}


class StoryOtrioWrapper:

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

    # Launch actual Arcade Otrio App in a separate window in PvAI mode
    self.arcade_win = tk.Toplevel(root)
    self.arcade_app = OtrioApp(self.arcade_win, mode="PvAI")

    # Intercept square_clicked and ai_move win detection to handle story hooks
    original_square_clicked = self.arcade_app.square_clicked

    def custom_square_clicked(r, c):
      if self.arcade_app.game_over:
        return

      size = self.arcade_app.selected_size
      player = self.arcade_app.turn

      if self.arcade_app.inventory[player][size] <= 0:
        messagebox.showwarning(
            "No Rings Left", f"You have no remaining {size} rings left!"
        )
        return

      if self.arcade_app.board[r][c][size] is not None:
        messagebox.showwarning(
            "Slot Occupied", f"There is already a {size} ring in this square!"
        )
        return

      self.arcade_app.board[r][c][size] = player
      self.arcade_app.inventory[player][size] -= 1
      self.arcade_app.update_board_ui()
      self.arcade_app.update_inventory_ui()

      if self.arcade_app.check_win(player):
        self.arcade_app.game_over = True
        self.arcade_app.timer_running = False
        user_won = player == "Red"

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

      if all(
          count == 0 for count in self.arcade_app.inventory[player].values()
      ):
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

      self.arcade_app.finish_turn()

    def custom_ai_move():
      if self.arcade_app.game_over:
        return

      valid_moves = []
      for size in ["L", "M", "S"]:
        if self.arcade_app.inventory["Blue"][size] > 0:
          for r in range(3):
            for c in range(3):
              if self.arcade_app.board[r][c][size] is None:
                valid_moves.append((r, c, size))

      if valid_moves:
        r, c, size = random.choice(valid_moves)
        self.arcade_app.board[r][c][size] = "Blue"
        self.arcade_app.inventory["Blue"][size] -= 1
        self.arcade_app.update_board_ui()
        self.arcade_app.update_inventory_ui()

        if self.arcade_app.check_win("Blue"):
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

        self.arcade_app.finish_turn()

    self.arcade_app.square_clicked = custom_square_clicked
    self.arcade_app.ai_move = custom_ai_move
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
  app = StoryOtrioWrapper(root)
  root.mainloop()
