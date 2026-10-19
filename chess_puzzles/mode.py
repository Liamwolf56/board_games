import tkinter as tk


class ChessPuzzlesModeFrame(tk.Frame):

  def __init__(self, parent, hub_app):
    super().__init__(parent, bg="#2c3e50", bd=2, relief="solid")
    self.hub_app = hub_app

    tk.Label(
        self,
        text="♟️ CHESS PUZZLE MODE",
        font=("Arial", 14, "bold"),
        bg="#2c3e50",
        fg="#ffdd59",
    ).pack(pady=20)

    tk.Label(
        self,
        text=(
            "Tactical Checkmate & Strategy Challenges\n(Folder:"
            " chess_puzzles/mode.py)"
        ),
        font=("Arial", 12),
        bg="#2c3e50",
        fg="white",
    ).pack(pady=40)
