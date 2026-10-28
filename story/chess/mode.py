import json
import os
import sys
import tkinter as tk
from tkinter import messagebox
import importlib.util

# Bulletproof load of local chess/app.py, avoiding python-chess package collision
root_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
chess_app_path = os.path.join(root_dir, "chess", "app.py")
spec = importlib.util.spec_from_file_location("chess_app_local", chess_app_path)
chess_app_mod = importlib.util.module_from_spec(spec)
sys.modules["chess_app_local"] = chess_app_mod
spec.loader.exec_module(chess_app_mod)
ChessApp = chess_app_mod.ChessApp

KING_DATA = {
    "game": "Chess",
    "title": "Chess.com Final Boss",
    "intro": (
        "Welcome to the ultimate grandmaster engine. Checkmate awaits your"
        " king!"
    ),
    "victory": (
        "Grandmaster engine dominance! Your king has been decisively"
        " checkmated!"
    ),
    "defeat": (
        "IMPOSSIBLE! You checkmated the grandmaster engine! The realm is"
        " conquered!"
    ),
}


class StoryChessWrapper:

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
    self.arcade_app = ChessApp(self.arcade_win, mode="PvAI")
    self.arcade_win.protocol(
        "WM_DELETE_WINDOW", lambda: self.handle_exit(False)
    )

  def handle_exit(self, win):
    try:
      if win:
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
  app = StoryChessWrapper(root)
  root.mainloop()
