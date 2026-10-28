import json
import os
import sys
import tkinter as tk
from tkinter import messagebox

# Add parent directory to path to import arcade mastermind module
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from mastermind.app import MastermindApp

KING_DATA = {
    "game": "Mastermind",
    "title": "Codebreaker Oracle",
    "intro": (
        "Every combination is locked behind my cryptic cipher! Crack the"
        " secret code if you dare!"
    ),
    "victory": (
        "Cipher secure! Your guesses fell short of the hidden code!"
    ),
    "defeat": (
        "IMPOSSIBLE! You cracked my code and bypassed all security ciphers!"
    ),
}


class StoryMastermindWrapper:

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

    # Launch actual Arcade Mastermind App in a separate window
    self.arcade_win = tk.Toplevel(root)
    self.arcade_app = MastermindApp(self.arcade_win, mode="Solo")

    # Intercept submit_guess and update_timer to handle win/loss hooks
    original_submit_guess = self.arcade_app.submit_guess

    def custom_submit_guess():
      if self.arcade_app.game_over or self.arcade_app.active_peg_slot < 4:
        return

      black_pegs = 0
      white_pegs = 0
      secret_copy = list(self.arcade_app.secret_code)
      guess_copy = list(self.arcade_app.current_guess)

      for i in range(4):
        if guess_copy[i] == secret_copy[i]:
          black_pegs += 1
          secret_copy[i] = None
          guess_copy[i] = None

      for i in range(4):
        if guess_copy[i] is not None and guess_copy[i] in secret_copy:
          white_pegs += 1
          secret_copy[secret_copy.index(guess_copy[i])] = None

      row_idx = self.arcade_app.max_attempts - 1 - self.arcade_app.current_attempt
      fb_text = f"● x{black_pegs} | ○ x{white_pegs}"
      self.arcade_app.rows_ui[row_idx]["feedback"].config(text=fb_text)

      if black_pegs == 4:
        self.arcade_app.game_over = True
        self.arcade_app.timer_running = False
        try:
          messagebox.showinfo(
              "VICTORY! 🏆",
              f"{KING_DATA['title']} cries out in defeat:\n\n\"{KING_DATA['defeat']}\"",
          )
          self.update_save(win=True)
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

      self.arcade_app.current_attempt += 1

      if self.arcade_app.current_attempt >= self.arcade_app.max_attempts:
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

      self.arcade_app.current_guess = ["", "", "", ""]
      self.arcade_app.active_peg_slot = 0
      self.arcade_app.submit_btn.config(state=tk.DISABLED)
      self.arcade_app.status_label.config(
          text=f"Attempt {self.arcade_app.current_attempt + 1}/10: Select 4 colors for your guess"
      )
      self.arcade_app.update_active_row_ui()

    self.arcade_app.submit_guess = custom_submit_guess
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
  app = StoryMastermindWrapper(root)
  root.mainloop()
