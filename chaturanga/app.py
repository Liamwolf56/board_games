import tkinter as tk
from tkinter import messagebox


class ChaturangaGUI:

  def __init__(self, root):
    self.root = root
    self.root.title("Chaturanga (Ancient Chess)")
    self.root.geometry("600x650")
    self.root.config(bg="#34495e")

    # Title label
    title_label = tk.Label(
        root,
        text="🐘 Chaturanga (Ancient Chess)",
        font=("Arial", 16, "bold"),
        bg="#34495e",
        fg="white",
    )
    title_label.pack(pady=10)

    # Frame for the 8x8 board
    self.board_frame = tk.Frame(root, bg="#2c3e50", bd=3, relief="solid")
    self.board_frame.pack(pady=10)

    self.buttons = {}
    self.create_board()

  def create_board(self):
    # Simplified starting piece representations for Chaturanga
    # R=Ratha (Chariot), N=Ashva (Horse), E=Gaja (Elephant), M=Mantri (General), K=Raja (King), P=Padati (Pawn)
    initial_setup = [
        ["R", "N", "E", "M", "K", "E", "N", "R"],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        ["r", "n", "e", "m", "k", "e", "n", "r"],
    ]

    for r in range(8):
      for c in range(8):
        bg_color = "#f0d9b5" if (r + c) % 2 == 0 else "#b58863"

        btn = tk.Button(
            self.board_frame,
            text=initial_setup[r][c] if initial_setup[r][c] != "." else "",
            font=("Arial", 20, "bold"),
            width=3,
            height=1,
            bg=bg_color,
            activebackground=bg_color,
            command=lambda row=r, col=c: self.square_clicked(row, col),
        )
        btn.grid(row=r, column=c, padx=1, pady=1)
        self.buttons[(r, c)] = btn

  def square_clicked(self, row, col):
    piece = self.buttons[(row, col)]["text"]
    if piece:
      messagebox.showinfo(
          "Chaturanga Piece", f"You clicked piece '{piece}' at position ({row}, {col})"
      )
    else:
      messagebox.showinfo("Chaturanga Board", f"Empty square at position ({row}, {col})")


if __name__ == "__main__":
  root = tk.Tk()
  app = ChaturangaGUI(root)
  root.mainloop()
