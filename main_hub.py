import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox


class MasterGameHub:

  def __init__(self, root):
    self.root = root
    self.root.title("Master Board Game Hub")
    self.root.geometry("420x520")
    self.root.config(bg="#1e272e")

    # Title
    title_label = tk.Label(
        root,
        text="🏛️ Master Game Hub",
        font=("Arial", 20, "bold"),
        bg="#1e272e",
        fg="white",
    )
    title_label.pack(pady=15)

    # Game Mode Variable (PvP or PvAI)
    self.mode_var = tk.StringVar(value="PvP")

    mode_frame = tk.Frame(root, bg="#1e272e")
    mode_frame.pack(pady=5)

    tk.Label(
        mode_frame,
        text="Game Mode:",
        font=("Arial", 11, "bold"),
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
        activebackground="#1e272e",
        activeforeground="white",
    ).pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(
        mode_frame,
        text="Player vs AI",
        variable=self.mode_var,
        value="PvAI",
        bg="#1e272e",
        fg="white",
        selectcolor="#485460",
        activebackground="#1e272e",
        activeforeground="white",
    ).pack(side=tk.LEFT, padx=5)

    subtitle_label = tk.Label(
        root,
        text="Select a game to launch:",
        font=("Arial", 11),
        bg="#1e272e",
        fg="#d2dae2",
    )
    subtitle_label.pack(pady=10)

    # Frame for game buttons
    btn_frame = tk.Frame(root, bg="#1e272e")
    btn_frame.pack(pady=10)

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
      btn.pack(pady=6)

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
    quit_btn.pack(pady=15)

  def launch_game(self, folder_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    game_path = os.path.join(current_dir, folder_name, "app.py")
    selected_mode = self.mode_var.get()

    if os.path.exists(game_path):
      try:
        # Pass the selected mode as a command-line argument to the game app
        subprocess.Popen([sys.executable, game_path, selected_mode])
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
