import json
import os
import sys
import tkinter as tk
from tkinter import messagebox

# Add parent directory to path to import arcade reversi module
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from reversi.app import ReversiApp

KING_DATA = {
    "game": "Reversi",
    "title": "High Lord Othello",
    "intro": (
        "Every disc shall flip to my color! Your board control will vanish into"
        " the shadows!"
    ),
    "victory": (
        "Othello supremacy! Your discs have been completely flipped and"
        " consumed!"
    ),
    "defeat": (
        "IMPOSSIBLE! My corner controls have collapsed! The Othello board"
        " shatters!"
    ),
}


class StoryReversiWrapper:

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

    # Launch actual Arcade Reversi App in a separate window in PvAI mode
    self.arcade_win = tk.Toplevel(root)
    self.arcade_app = ReversiApp(self.arcade_win, mode="PvAI")

    # Intercept check_game_state to handle story progression and permadeath
    def custom_check_game_state():
      self.arcade_app.turn = (
          "White" if self.arcade_app.turn == "Black" else "Black"
      )
      valid_moves = self.arcade_app.get_valid_moves(self.arcade_app.turn)

      if not valid_moves:
        self.arcade_app.turn = (
            "White" if self.arcade_app.turn == "Black" else "Black"
        )
        valid_moves = self.arcade_app.get_valid_moves(self.arcade_app.turn)
        if not valid_moves:
          self.arcade_app.game_over = True
          self.arcade_app.timer_running = False

          black_score = sum(
              row.count("Black") for row in self.arcade_app.board
          )
          white_score = sum(
              row.count("White") for row in self.arcade_app.board
          )

          # Black is user, White is AI
          user_won = black_score > white_score

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
        color_code = (
            "#3498db" if self.arcade_app.turn == "Black" else "#ecf0f1"
        )
        self.arcade_app.status_label.config(
            text=f"Turn: {self.arcade_app.turn} Player - Place your disc",
            fg=color_code,
        )

      self.arcade_app.update_board_ui()

      if (
          self.arcade_app.mode == "PvAI"
          and self.arcade_app.turn == "White"
          and not self.arcade_app.game_over
      ):
        self.arcade_app.root.after(600, self.arcade_app.ai_move)

    self.arcade_app.check_game_state = custom_check_game_state
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
  app = StoryReversiWrapper(root)
  root.mainloop()
