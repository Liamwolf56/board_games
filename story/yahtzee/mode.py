import json
import os
import sys
import tkinter as tk
from tkinter import messagebox

# Add parent directory to path to import arcade yahtzee module
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from yahtzee.app import YahtzeeApp

KING_DATA = {
    "game": "Yahtzee",
    "title": "High Roller Chance",
    "intro": (
        "Roll the dice and test your fate! Every combination favors my high"
        " stakes!"
    ),
    "victory": (
        "Yahtzee! Your high rolls fell short of my winning scorecard!"
    ),
    "defeat": (
        "IMPOSSIBLE! You rolled a perfect Yahtzee and broke my winning streak!"
    ),
}


class StoryYahtzeeWrapper:

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

    # Launch actual Arcade Yahtzee App in a separate window in PvAI mode
    self.arcade_win = tk.Toplevel(root)
    self.arcade_app = YahtzeeApp(self.arcade_win, mode="PvAI")

    # Intercept finish_turn to handle story progression and permadeath
    original_finish_turn = self.arcade_app.finish_turn

    def custom_finish_turn():
      self.arcade_app.dice_rolled_this_turn = False
      self.arcade_app.rolls_left = 3
      self.arcade_app.held = [False, False, False, False, False]
      self.arcade_app.roll_btn.config(text="🎲 Roll Dice (3 left)", bg="#2ecc71")

      p1_done = all(v is not None for v in self.arcade_app.p1_scores.values())
      p2_done = all(v is not None for v in self.arcade_app.p2_scores.values())

      if (
          p1_done
          and p2_done
          or self.arcade_app.p1_time == 0
          or self.arcade_app.p2_time == 0
      ):
        self.arcade_app.game_over = True
        self.arcade_app.timer_running = False

        p1_total = sum(
            v for v in self.arcade_app.p1_scores.values() if v is not None
        )
        p2_total = sum(
            v for v in self.arcade_app.p2_scores.values() if v is not None
        )

        # Player 1 is user, Player 2 is AI
        user_won = p1_total > p2_total

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

      self.arcade_app.turn = (
          "Player 2" if self.arcade_app.turn == "Player 1" else "Player 1"
      )
      color_code = (
          "#00d8d6" if self.arcade_app.turn == "Player 1" else "#ff4757"
      )
      self.arcade_app.status_label.config(
          text=f"Turn: {self.arcade_app.turn} - Click 'Roll Dice' to start",
          fg=color_code,
      )
      self.arcade_app.update_ui()

      if (
          self.arcade_app.mode == "PvAI"
          and self.arcade_app.turn == "Player 2"
          and not self.arcade_app.game_over
      ):
        self.arcade_app.root.after(800, self.arcade_app.ai_turn)

    self.arcade_app.finish_turn = custom_finish_turn
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
  app = StoryYahtzeeWrapper(root)
  root.mainloop()
