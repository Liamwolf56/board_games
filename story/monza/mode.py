import json
import os
import sys
import tkinter as tk
from tkinter import messagebox

# Add parent directory to path to import arcade monza module
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from monza.app import MonzaApp

KING_DATA = {
    "game": "Monza",
    "title": "Speed King Monza",
    "intro": (
        "Rev your engines! The color dice obey my speedway. You will never cross"
        " the finish line first!"
    ),
    "victory": (
        "Speedway victory! Your car spun out and was left in the dust!"
    ),
    "defeat": (
        "IMPOSSIBLE! You accelerated past the checkered flag and shattered my"
        " track record!"
    ),
}


class StoryMonzaWrapper:

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

    # Launch actual Arcade Monza App in a separate window in PvAI mode
    self.arcade_win = tk.Toplevel(root)
    self.arcade_app = MonzaApp(self.arcade_win, mode="PvAI")

    # Intercept use_die and ai_turn win checks for story hooks
    original_use_die = self.arcade_app.use_die

    def custom_use_die(idx):
      if self.arcade_app.game_over or not self.arcade_app.die_rolled or idx in self.arcade_app.used_dice_indices:
        return

      die_color = self.arcade_app.current_dice[idx]
      current_pos = self.arcade_app.car1_pos if self.arcade_app.turn == "Car 1" else self.arcade_app.car2_pos

      if current_pos >= 12:
        return

      required_color = self.arcade_app.track_color_names[current_pos]

      if die_color == required_color:
        self.arcade_app.used_dice_indices.add(idx)
        if self.arcade_app.turn == "Car 1":
          self.arcade_app.car1_pos += 1
        else:
          self.arcade_app.car2_pos += 1

        self.arcade_app.update_track_ui()
        self.arcade_app.update_dice_ui()

        pos = self.arcade_app.car1_pos if self.arcade_app.turn == "Car 1" else self.arcade_app.car2_pos
        if pos >= 12:
          self.arcade_app.game_over = True
          self.arcade_app.timer_running = False
          user_won = self.arcade_app.turn == "Car 1"

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
        else:
          next_needed = self.arcade_app.track_color_names[pos]
          self.arcade_app.status_label.config(
              text=f"Turn: {self.arcade_app.turn} - Next Tile Needed: [{next_needed}]",
              fg="#f1c40f",
          )
      else:
        messagebox.showwarning(
            "Mismatch",
            f"You clicked {die_color}, but the next tile needs {required_color}!",
        )

    def custom_ai_turn():
      if self.arcade_app.game_over:
        return

      self.arcade_app.roll_dice()

      moved = True
      while moved and not self.arcade_app.game_over:
        moved = False
        if self.arcade_app.car2_pos < 12:
          req_color = self.arcade_app.track_color_names[self.arcade_app.car2_pos]
          for idx, d_color in enumerate(self.arcade_app.current_dice):
            if idx not in self.arcade_app.used_dice_indices and d_color == req_color:
              self.arcade_app.use_die(idx)
              moved = True
              break

      if self.arcade_app.car2_pos >= 12:
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

      if not self.arcade_app.game_over:
        self.arcade_app.root.after(800, self.arcade_app.finish_turn)

    self.arcade_app.use_die = custom_use_die
    self.arcade_app.ai_turn = custom_ai_turn
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
  app = StoryMonzaWrapper(root)
  root.mainloop()
