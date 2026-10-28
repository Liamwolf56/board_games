import json
import os
import sys
import tkinter as tk
from tkinter import messagebox

# Add parent directory to path to import arcade animal_upon_animal module
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from animal_upon_animal.app import AnimalUponAnimalApp

KING_DATA = {
    "game": "Animal Upon Animal",
    "title": "Stacked Menagerie Ringmaster",
    "intro": (
        "Stack the animals high before the pyramid tumbles! Your inventory"
        " will never clear under my watch!"
    ),
    "victory": (
        "Menagerie triumph! Your animal stack collapsed into a tangled heap!"
    ),
    "defeat": (
        "IMPOSSIBLE! You successfully stacked every animal without a single"
        " collapse!"
    ),
}


class StoryAnimalUponAnimalWrapper:

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

    # Launch actual Arcade Animal Upon Animal App in a separate window in PvAI mode
    self.arcade_win = tk.Toplevel(root)
    self.arcade_app = AnimalUponAnimalApp(self.arcade_win, mode="PvAI")

    # Intercept stack_animal win check for story hooks
    original_stack_animal = self.arcade_app.stack_animal

    def custom_stack_animal(animal_name):
      if self.arcade_app.game_over or not self.arcade_app.die_rolled:
        return

      inv = (
          self.arcade_app.p1_inventory
          if self.arcade_app.turn == "Player 1"
          else self.arcade_app.p2_inventory
      )
      other_inv = (
          self.arcade_app.p2_inventory
          if self.arcade_app.turn == "Player 1"
          else self.arcade_app.p1_inventory
      )

      if self.arcade_app.roll_result == "PASS_ANIMAL":
        inv.remove(animal_name)
        other_inv.append(animal_name)
        messagebox.showinfo(
            "Passed Animal!",
            f"{self.arcade_app.turn} passed a {animal_name} to the opponent!",
        )
        self.arcade_app.finish_turn()
        return

      collapse = len(self.arcade_app.pyramid) > 3 and random.random() < 0.15

      if collapse:
        messagebox.showwarning(
            "OH NO! COLLAPSE! 💥",
            f"The animal pyramid tumbled! {self.arcade_app.turn} takes an extra animal penalization!",
        )
        penalty = ["Snake", "Penguin", "Toucan"]
        inv.append(random.choice(penalty))
      else:
        inv.remove(animal_name)
        self.arcade_app.pyramid.append(f"📦 {animal_name} ({self.arcade_app.turn})")

      self.arcade_app.update_pyramid_ui()

      if len(inv) == 0:
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

      if self.arcade_app.roll_result == "PLACE_2":
        self.arcade_app.roll_result = "PLACE_1"
        self.arcade_app.status_label.config(
            text=f"{self.arcade_app.turn}: Select your 2nd animal to stack!",
            fg="#f1c40f",
        )
        self.arcade_app.update_hand_ui()
      else:
        self.arcade_app.finish_turn()

    self.arcade_app.stack_animal = custom_stack_animal
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
  app = StoryAnimalUponAnimalWrapper(root)
  root.mainloop()
