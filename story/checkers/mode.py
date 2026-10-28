import json
import os
import sys
import tkinter as tk
from tkinter import messagebox

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from checkers.app import CheckersApp

KING_DATA = {
    "game": "Checkers",
    "title": "Grandmaster Checkers",
    "intro": (
        "King me! Diagonal jumps and crowned pieces will sweep you off the"
        " board!"
    ),
    "victory": "Checkers supremacy! Your pieces have been completely jumped!",
    "defeat": "IMPOSSIBLE! Your crowned pieces smashed through my defenses!",
}


class StoryCheckersWrapper:

  def __init__(self, root):
    self.root = root
    self.root.title(f"Story Mode: {KING_DATA['title']}")
    self.root.geometry("520x160")
    self.root.config(bg="#1e272e")

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

    self.arcade_win = tk.Toplevel(root)
    self.arcade_app = CheckersApp(self.arcade_win, mode="PvAI")
    self.arcade_win.protocol(
        "WM_DELETE_WINDOW", lambda: self.root.destroy()
    )


if __name__ == "__main__":
  root = tk.Tk()
  app = StoryCheckersWrapper(root)
  root.mainloop()
