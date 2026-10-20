import os
import subprocess
import sys
import tkinter as tk

# Import modes from their respective folders
from arcade.mode import ArcadeModeFrame
from chess_puzzles.mode import ChessPuzzlesModeFrame
from history.mode import HistoryModeFrame
from story.mode import StoryModeFrame


class MainHubApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Master Board Game Hub")
    self.root.geometry("800x880")
    self.root.config(bg="#1e272e")

    # Title Banner
    title_label = tk.Label(
        root,
        text="🎮 MASTER BOARD GAME ARCADE & HUB 🎮",
        font=("Arial", 16, "bold"),
        bg="#1e272e",
        fg="#ffdd59",
    )
    title_label.pack(pady=10)

    # Navigation Bar
    nav_frame = tk.Frame(root, bg="#1e272e")
    nav_frame.pack(pady=5)

    tk.Button(
        nav_frame,
        text="🕹️ Arcade Mode",
        font=("Arial", 10, "bold"),
        bg="#0984e3",
        fg="white",
        width=15,
        command=lambda: self.show_screen("arcade"),
    ).pack(side=tk.LEFT, padx=5)

    tk.Button(
        nav_frame,
        text="📜 History Mode",
        font=("Arial", 10, "bold"),
        bg="#6c5ce7",
        fg="white",
        width=15,
        command=lambda: self.show_screen("history"),
    ).pack(side=tk.LEFT, padx=5)

    tk.Button(
        nav_frame,
        text="♟️ Chess Puzzles",
        font=("Arial", 10, "bold"),
        bg="#e17055",
        fg="white",
        width=15,
        command=lambda: self.show_screen("puzzles"),
    ).pack(side=tk.LEFT, padx=5)

    tk.Button(
        nav_frame,
        text="📖 Story Mode",
        font=("Arial", 10, "bold"),
        bg="#00b894",
        fg="white",
        width=15,
        command=lambda: self.show_screen("story"),
    ).pack(side=tk.LEFT, padx=5)

    # Container
    self.container = tk.Frame(root, bg="#1e272e")
    self.container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Initialize screens from sub-folders
    self.screens = {
        "arcade": ArcadeModeFrame(self.container, self),
        "history": HistoryModeFrame(self.container, self),
        "puzzles": ChessPuzzlesModeFrame(self.container, self),
        "story": StoryModeFrame(self.container, self),
    }

    self.show_screen("arcade")

  def show_screen(self, screen_name):
    for frame in self.screens.values():
      frame.pack_forget()
    self.screens[screen_name].pack(fill=tk.BOTH, expand=True)

  def launch_game(self, script_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, script_path)

    if not os.path.exists(full_path):
      tk.messagebox.showerror("Error", f"Game script not found:\n{full_path}")
      return

    mode = self.selected_mode.get() if hasattr(self, "selected_mode") else "PvP"

    # Automatically use virtual environment python if available
    venv_python = os.path.join(base_dir, "venv", "bin", "python3")
    python_executable = venv_python if os.path.exists(venv_python) else sys.executable

    subprocess.Popen([python_executable, full_path, mode])


if __name__ == "__main__":
  root = tk.Tk()
  app = MainHubApp(root)
  root.mainloop()
