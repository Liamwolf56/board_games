import json
import os
import sys
import tkinter as tk
from tkinter import messagebox

# Add parent directory to path to import arcade sequence_for_kids module
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from sequence_for_kids.app import SequenceForKidsApp

KING_DATA = {
    "game": "Sequence for Kids",
    "title": "Safari Master Jenga",
    "intro": (
        "The wildlife animals of the savanna march to my rhythm! Connect your"
        " chips if you can!"
    ),
    "victory": (
        "Savannah victory! Your animal sequence was blocked and broken!"
    ),
    "defeat": (
        "IMPOSSIBLE! You connected your animal chips across the entire board!"
    ),
}


class StorySequenceForKidsWrapper:

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

    # Launch actual Arcade Sequence For Kids App in a separate window in PvAI mode
    self.arcade_win = tk.Toplevel(root)
    self.arcade_app = SequenceForKidsApp(self.arcade_win, mode="PvAI")

    # Intercept board_clicked and ai_move win checks for story hooks
    original_board_clicked = self.arcade_app.board_clicked

    def custom_board_clicked(r, c):
      if self.arcade_app.game_over:
        return

      if self.arcade_app.selected_card_idx is None:
        messagebox.showwarning(
            "Select Card First", "Please select a card from your hand first!"
        )
        return

      hand = (
          self.arcade_app.p1_hand
          if self.arcade_app.turn == "Player 1"
          else self.arcade_app.p2_hand
      )
      card_animal = hand[self.arcade_app.selected_card_idx]
      board_animal = self.arcade_app.board_animals[r][c]

      if board_animal != card_animal:
        messagebox.showwarning(
            "Mismatch",
            f"This square is a {board_animal}, but your card is {card_animal}!",
        )
        return

      if self.arcade_app.board_chips[r][c] != "":
        messagebox.showwarning("Occupied", "This square already has a chip on it!")
        return

      self.arcade_app.board_chips[r][c] = self.arcade_app.turn
      hand[self.arcade_app.selected_card_idx] = random.choice(
          self.arcade_app.animals
      )
      self.arcade_app.selected_card_idx = None

      self.arcade_app.update_board_ui()
      self.arcade_app.update_hand_ui()

      if self.arcade_app.check_win(self.arcade_app.turn):
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

      self.arcade_app.finish_turn()

    def custom_ai_move():
      if self.arcade_app.game_over:
        return

      valid_move = None
      for idx, card in enumerate(self.arcade_app.p2_hand):
        for r in range(5):
          for c in range(5):
            if (
                self.arcade_app.board_animals[r][c] == card
                and self.arcade_app.board_chips[r][c] == ""
            ):
              valid_move = (idx, r, c)
              break
          if valid_move:
            break
        if valid_move:
          break

      if valid_move:
        idx, r, c = valid_move
        self.arcade_app.board_chips[r][c] = "Player 2"
        self.arcade_app.p2_hand[idx] = random.choice(self.arcade_app.animals)
        self.arcade_app.update_board_ui()
        self.arcade_app.update_hand_ui()

        if self.arcade_app.check_win("Player 2"):
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

    self.arcade_app.board_clicked = custom_board_clicked
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
  app = StorySequenceForKidsWrapper(root)
  root.mainloop()
