import tkinter as tk
from tkinter import messagebox
import sys

class ShogiApp:
    def __init__(self, root, mode="PvP"):
        self.root = root
        self.root.title(f"Shogi - Mode: {mode}")
        self.root.geometry("650x750")
        self.root.config(bg="#2c3e50")

        top_frame = tk.Frame(root, bg="#2c3e50")
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(top_frame, text="📖 How to Play Shogi", bg="#f39c12", fg="white", font=("Arial", 10, "bold"), command=self.show_rules).pack(side=tk.LEFT)
        tk.Label(top_frame, text="⛩️ Japanese Chess (9x9)", font=("Arial", 10, "bold"), bg="#2c3e50", fg="white").pack(side=tk.RIGHT)

        self.board_frame = tk.Frame(root, bg="#1abc9c", bd=3, relief="solid")
        self.board_frame.pack(pady=10)
        self.create_board()

    def show_rules(self):
        rules = (
            "SHOGI RULES:\n\n"
            "• Played on a 9x9 grid.\n"
            "• Drop Rule: Captured enemy pieces can be re-entered onto the board as your own pieces!\n"
            "• Goal: Checkmate the opposing King."
        )
        messagebox.showinfo("How to Play - Shogi", rules)

    def create_board(self):
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
                btn = tk.Button(self.board_frame, text=setup[r][c] if setup[r][c] != "." else "", font=("Arial", 13, "bold"), width=3, height=1, bg="#f39c12")
                btn.grid(row=r, column=c, padx=1, pady=1)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
    root = tk.Tk()
    app = ShogiApp(root, mode)
    root.mainloop()
