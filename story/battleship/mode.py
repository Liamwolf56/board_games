import json
import os
import sys
import tkinter as tk
from tkinter import messagebox

# Add parent directory to path to import arcade battleship module
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from battleship.app import BattleshipApp

KING_DATA = {
    "game": "Battleship",
    "title": "Fleet Admiral Cannon",
    "intro": (
        "My naval fleet dominates these digital waters! Prepare to sink beneath"
        " the horizon!"
    ),
    "victory": (
        "Naval supremacy! Your fleet lies resting at the bottom of the"
        " ocean!"
    ),
    "defeat": (
        "IMPOSSIBLE! My entire command fleet has been torpedoed and sunk!"
    ),
}


class StoryBattleshipWrapper:

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

    # Launch actual Arcade Battleship App in a separate window in PvAI mode
    self.arcade_win = tk.Toplevel(root)
    self.arcade_app = BattleshipApp(self.arcade_win, mode="PvAI")

    # Intercept fire_shot and ai_fire to handle story win/loss hooks
    original_fire_shot = self.arcade_app.fire_shot

    def custom_fire_shot(r, c):
      if self.arcade_app.phase != "BATTLE" or self.arcade_app.game_over:
        return

      if self.arcade_app.turn == "Player 1":
        shots_grid = self.arcade_app.p1_shots
        target_ships = self.arcade_app.p2_ships
      else:
        shots_grid = self.arcade_app.p2_shots
        target_ships = self.arcade_app.p1_ships

      if shots_grid[r][c] != ".":
        return

      if target_ships[r][c] == "S":
        shots_grid[r][c] = "H"
        target_ships[r][c] = "H"
        self.arcade_app.target_buttons[(r, c)].config(
            text="💥", bg="#ee5253", state=tk.DISABLED
        )
        self.arcade_app.status_label.config(
            text=f"{self.arcade_app.turn}: DIRECT HIT! 💥 Fire again!",
            fg="#ff4757",
        )
      else:
        shots_grid[r][c] = "M"
        self.arcade_app.target_buttons[(r, c)].config(
            text="🌊", bg="#c8d6e5", fg="#222f3e", state=tk.DISABLED
        )
        self.arcade_app.status_label.config(
            text=f"{self.arcade_app.turn}: Splash! MISSED 🌊", fg="#fca510"
        )

      if not any("S" in row for row in target_ships):
        self.arcade_app.game_over = True
        self.arcade_app.timer_running = False
        user_won = self.arcade_app.turn == "Player 1"

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

      if self.arcade_app.mode == "PvAI":
        if not self.arcade_app.game_over:
          self.arcade_app.root.after(600, custom_ai_fire)

    def custom_ai_fire():
      if self.arcade_app.game_over:
        return

      unshot = [
          (r, c)
          for r in range(8)
          for c in range(8)
          if self.arcade_app.p2_shots[r][c] == "."
      ]
      if unshot:
        r, c = random.choice(unshot)
        if self.arcade_app.p1_ships[r][c] == "S":
          self.arcade_app.p2_shots[r][c] = "H"
          self.arcade_app.p1_ships[r][c] = "H"
        else:
          self.arcade_app.p2_shots[r][c] = "M"

        self.arcade_app.update_fleet_ui()

        if not any("S" in row for row in self.arcade_app.p1_ships):
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

    self.arcade_app.fire_shot = custom_fire_shot
    self.arcade_app.ai_fire = custom_ai_fire
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
  app = StoryBattleshipWrapper(root)
  root.mainloop()
