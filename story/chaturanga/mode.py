import json
import os
import sys
import tkinter as tk
from tkinter import messagebox

# Add parent directory to path to import arcade chaturanga module
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from chaturanga.app import ChaturangaApp

KING_DATA = {
    "game": "Chaturanga",
    "title": "Sovereign Ancient Raja",
    "intro": (
        "From the ancient sands of antiquity, my royal army of chariots and"
        " elephants stands ready to crush you!"
    ),
    "victory": (
        "Ancient victory! Your royal king falls beneath the ancient banner!"
    ),
    "defeat": (
        "IMPOSSIBLE! My ancient throne shatters! The legacy of Chaturanga"
        " is broken!"
    ),
}


class StoryChaturangaWrapper:

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

    # Launch actual Arcade Chaturanga App in a separate window in PvAI mode
    self.arcade_win = tk.Toplevel(root)
    self.arcade_app = ChaturangaApp(self.arcade_win, mode="PvAI")

    # Intercept check_game_over to handle story progression and permadeath
    def custom_check_game_over():
      p1_k, p2_k = False, False
      for r in range(8):
        for c in range(8):
          p = self.arcade_app.board[r][c]
          if p and p["type"] == "KING":
            if p["player"] == 1:
              p1_k = True
            elif p["player"] == 2:
              p2_k = True

      if not p1_k or not p2_k or self.arcade_app.time_p1 == 0 or self.arcade_app.time_p2 == 0:
        self.arcade_app.timer_running = False
        user_won = not p2_k or self.arcade_app.time_p2 == 0

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
        return True
      return False

    self.arcade_app.check_game_over = custom_check_game_over
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
  app = StoryChaturangaWrapper(root)
  root.mainloop()
