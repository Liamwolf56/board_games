import tkinter as tk
from tkinter import messagebox

class ShogiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Shogi (Japanese Chess)")
        self.root.geometry("650x700")
        self.root.config(bg="#2c3e50")

        title_label = tk.Label(root, text="⛩️ Shogi (Japanese Chess - 9x9)", font=("Arial", 16, "bold"), bg="#2c3e50", fg="white")
        title_label.pack(pady=10)

        self.board_frame = tk.Frame(root, bg="#1abc9c", bd=3, relief="solid")
        self.board_frame.pack(pady=10)

        self.buttons = {}
        self.create_board()

    def create_board(self):
        # 9x9 Shogi starting setup approximation (R=Rook, B=Bishop, G=Gold, S=Silver, N=Knight, L=Lance, K=King, P=Pawn)
        setup = [
            ["l", "n", "s", "g", "k", "g", "s", "n", "l"],
            [".", "r", ".", ".", ".", ".", ".", "b", "."],
            ["p", "p", "p", "p", "p", "p", "p", "p", "p"],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["P", "P", "P", "P", "P", "P", "P", "P", "P"],
            [".", "B", ".", ".", ".", ".", ".", "R", "."],
            ["L", "N", "S", "G", "K", "G", "S", "N", "L"]
        ]

        for r in range(9):
            for c in range(9):
                bg_color = "#e67e22" if (r + c) % 2 == 0 else "#d35400"
                btn = tk.Button(
                    self.board_frame,
                    text=setup[r][c] if setup[r][c] != "." else "",
                    font=("Arial", 14, "bold"),
                    width=3,
                    height=1,
                    bg="#f39c12",
                    activebackground="#e67e22",
                    command=lambda row=r, col=c: messagebox.showinfo("Shogi", f"Clicked Shogi square ({row}, {col})")
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[(r, c)] = btn

if __name__ == "__main__":
    root = tk.Tk()
    app = ShogiGUI(root)
    root.mainloop()
