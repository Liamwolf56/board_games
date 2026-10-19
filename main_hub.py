import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox


class MainHubApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Master Board Game Arcade")
    self.root.geometry("700x880")
    self.root.config(bg="#1e272e")

    self.selected_mode = tk.StringVar(value="PvP")

    # Title Banner
    title_label = tk.Label(
        root,
        text="🎮 MASTER BOARD GAME ARCADE 🎮",
        font=("Arial", 16, "bold"),
        bg="#1e272e",
        fg="#ffdd59",
    )
    title_label.pack(pady=15)

    # Mode Selector Frame
    mode_frame = tk.Frame(root, bg="#2c3e50", bd=2, relief="solid")
    mode_frame.pack(pady=10, padx=20, fill=tk.X)

    tk.Label(
        mode_frame,
        text="Select Game Mode:",
        font=("Arial", 11, "bold"),
        bg="#2c3e50",
        fg="white",
    ).pack(side=tk.LEFT, padx=15, pady=8)

    tk.Radiobutton(
        mode_frame,
        text="Player vs Player (PvP)",
        variable=self.selected_mode,
        value="PvP",
        font=("Arial", 10, "bold"),
        bg="#2c3e50",
        fg="#00d8d6",
        selectcolor="#1e272e",
        activebackground="#2c3e50",
    ).pack(side=tk.LEFT, padx=10)

    tk.Radiobutton(
        mode_frame,
        text="Player vs AI (PvAI)",
        variable=self.selected_mode,
        value="PvAI",
        font=("Arial", 10, "bold"),
        bg="#2c3e50",
        fg="#ff4757",
        selectcolor="#1e272e",
        activebackground="#2c3e50",
    ).pack(side=tk.LEFT, padx=10)

    # Game List Grid (15 Games)
    games_frame = tk.Frame(root, bg="#1e272e")
    games_frame.pack(pady=15, padx=20)

    games = [
        ("♟️ Chess", "chess/app.py"),
        ("🦹 Shogi", "shogi/app.py"),
        ("🀄 Xiangqi", "xiangqi/app.py"),
        ("📜 Chaturanga", "chaturanga/app.py"),
        ("🏁 Checkers", "checkers/app.py"),
        ("⚪ Reversi", "reversi/app.py"),
        ("🔴 Connect 4", "connect4/app.py"),
        ("❌ Tic-Tac-Toe", "tictactoe/app.py"),
        ("🚢 Battleship", "battleship/app.py"),
        ("⭕ Otrio", "otrio/app.py"),
        ("🦁 Sequence for Kids", "sequence_for_kids/app.py"),
        ("🐊 Animal Upon Animal", "animal_upon_animal/app.py"),
        ("🏎️ Monza", "monza/app.py"),
        ("🎲 Yahtzee", "yahtzee/app.py"),
        ("🧠 Mastermind", "mastermind/app.py"),
    ]

    row = 0
    col = 0
    for title, script_path in games:
      btn = tk.Button(
          games_frame,
          text=title,
          font=("Arial", 11, "bold"),
          width=22,
          height=2,
          bg="#34495e",
          fg="white",
          activebackground="#0abde3",
          activeforeground="white",
          command=lambda path=script_path: self.launch_game(path),
      )
      btn.grid(row=row, column=col, padx=8, pady=8)

      col += 1
      if col > 1:
        col = 0
        row += 1

  def launch_game(self, script_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, script_path)

    if not os.path.exists(full_path):
      messagebox.showerror("Error", f"Game script not found:\n{full_path}")
      return

    mode = self.selected_mode.get()
    subprocess.Popen([sys.executable, full_path, mode])


if __name__ == "__main__":
  root = tk.Tk()
  app = MainHubApp(root)
  root.mainloop()
