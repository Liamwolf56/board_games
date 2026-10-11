import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox


class MasterGameHub:

  def __init__(self, root):
    self.root = root
    self.root.title("Master Board Game Hub")
    self.root.geometry("460x680")
    self.root.config(bg="#1e272e")

    title_label = tk.Label(
        root,
        text="🏛️ Master Game Arcade",
        font=("Arial", 20, "bold"),
        bg="#1e272e",
        fg="white",
    )
    title_label.pack(pady=10)

    # Game Mode Selection
    self.mode_var = tk.StringVar(value="PvP")
    mode_frame = tk.Frame(root, bg="#1e272e")
    mode_frame.pack(pady=5)

    tk.Label(
        mode_frame,
        text="Mode:",
        font=("Arial", 10, "bold"),
        bg="#1e272e",
        fg="#d2dae2",
    ).pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(
        mode_frame,
        text="Player vs Player",
        variable=self.mode_var,
        value="PvP",
        bg="#1e272e",
        fg="white",
        selectcolor="#485460",
    ).pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(
        mode_frame,
        text="Player vs AI",
        variable=self.mode_var,
        value="PvAI",
        bg="#1e272e",
        fg="white",
        selectcolor="#485460",
    ).pack(side=tk.LEFT, padx=5)

    # Scrollable container or organized frame for buttons
    btn_frame = tk.Frame(root, bg="#1e272e")
    btn_frame.pack(pady=10)

    games = [
        ("♟️ Chess", "chess"),
        ("⛩️ Shogi", "shogi"),
        ("🏮 Xiangqi", "xiangqi"),
        ("🐘 Chaturanga", "chaturanga"),
        ("🔴 Connect 4", "connect_4"),
        ("❌ Tic-Tac-Toe", "tic_tac_toe"),
        ("🚀 Battleship", "battleship"),
        ("⭕ Otrio", "otrio"),
        ("🦁 Sequence for Kids", "sequence_for_kids"),
        ("🐊 Animal Upon Animal", "animal_upon_animal"),
        ("🏎️ Monza", "monza"),
    ]

    for text, folder_name in games:
      btn = tk.Button(
          btn_frame,
          text=text,
          font=("Arial", 10, "bold"),
          width=28,
          bg="#485460",
          fg="white",
          activebackground="#0be881",
          activeforeground="black",
          relief="flat",
          command=lambda f=folder_name: self.launch_game(f),
      )
      btn.pack(pady=3)

    quit_btn = tk.Button(
        root,
        text="Exit Hub",
        font=("Arial", 10, "bold"),
        width=15,
        bg="#ff3838",
        fg="white",
        relief="flat",
        command=root.quit,
    )
    quit_btn.pack(pady=10)

  def launch_game(self, folder_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    game_path = os.path.join(current_dir, folder_name, "app.py")
    if os.path.exists(game_path):
      subprocess.Popen([sys.executable, game_path, self.mode_var.get()])
    else:
      messagebox.showerror(
          "Error", f"Could not find 'app.py' inside '{folder_name}' folder!"
      )


if __name__ == "__main__":
  root = tk.Tk()
  app = MasterGameHub(root)
  root.mainloop()
