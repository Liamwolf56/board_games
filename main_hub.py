import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox


class MasterGameHub:

  def __init__(self, root):
    self.root = root
    self.root.title("Master Board Game Hub")
    self.root.geometry("400x480")
    self.root.config(bg="#1e272e")

    # Title
    title_label = tk.Label(
        root,
        text="🏛️ Master Game Hub",
        font=("Arial", 20, "bold"),
        bg="#1e272e",
        fg="white",
    )
    title_label.pack(pady=20)

    subtitle_label = tk.Label(
        root,
        text="Select a game to launch:",
        font=("Arial", 11),
        bg="#1e272e",
        fg="#d2dae2",
    )
    subtitle_label.pack(pady=5)

    # Frame for game buttons
    btn_frame = tk.Frame(root, bg="#1e272e")
    btn_frame.pack(pady=20)

    # Games mapped to their folder names
    games = [
        ("♟️ Chess", "chess"),
        ("⛩️ Shogi (Japanese Chess)", "shogi"),
        ("🏮 Xiangqi (Chinese Chess)", "xiangqi"),
        ("🐘 Chaturanga (Ancient Chess)", "chaturanga"),
    ]

    for text, folder_name in games:
      btn = tk.Button(
          btn_frame,
          text=text,
          font=("Arial", 11, "bold"),
          width=26,
          height=2,
          bg="#485460",
          fg="white",
          activebackground="#0be881",
          activeforeground="black",
          relief="flat",
          command=lambda f=folder_name: self.launch_game(f),
      )
      btn.pack(pady=8)

    # Quit Button
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
    # Determine the path to the game's app.py inside its folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    game_path = os.path.join(current_dir, folder_name, "app.py")

    if os.path.exists(game_path):
      try:
        # Launch the game script independently using the current python executable
        subprocess.Popen([sys.executable, game_path])
      except Exception as e:
        messagebox.showerror(
            "Error", f"Failed to launch {folder_name.capitalize()}: {e}"
        )
    else:
      messagebox.showerror(
          "Not Found",
          f"Could not find 'app.py' inside the '{folder_name}' folder!",
      )


if __name__ == "__main__":
  root = tk.Tk()
  app = MasterGameHub(root)
  root.mainloop()
