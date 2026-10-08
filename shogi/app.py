import tkinter as tk
from tkinter import messagebox
import sys

class ShogiApp:
    def __init__(self, root, mode="PvP"):
        self.root = root
        self.root.title(f"Shogi - Mode: {mode}")
        self.root.geometry("650x780")
        self.root.config(bg="#2c3e50")

        self.mode = mode
        self.selected_square = None
        self.buttons = {}

        top_frame = tk.Frame(root, bg="#2c3e50")
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(top_frame, text="📖 How to Play", bg="#f39c12", fg="white", font=("Arial", 10, "bold"), command=self.show_rules).pack(side=tk.LEFT)
        
        self.status_label = tk.Label(top_frame, text="Turn: White (Select a piece)", font=("Arial", 10, "bold"), bg="#2c3e50", fg="#1abc9c")
        self.status_label.pack(side=tk.RIGHT)

        self.board_frame = tk.Frame(root, bg="#1abc9c", bd=3, relief="solid")
        self.board_frame.pack(pady=10)

        self.setup_board_data()
        self.create_board_ui()

    def show_rules(self):
        rules = (
            "SHOGI HINTS & RULES:\n\n"
            "• 9x9 Japanese Chess grid.\n"
            "• Drop Rule: Captured pieces turn into your color and can be placed back onto any empty square!\n"
            "• Kings (K/k) must be protected at all costs."
        )
        messagebox.showinfo("How to Play - Shogi", rules)

    def setup_board_data(self):
        self.board = [
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
        self.turn = "white"

    def create_board_ui(self):
        for r in range(9):
            for c in range(9):
                btn = tk.Button(
                    self.board_frame,
                    text="",
                    font=("Arial", 13, "bold"),
                    width=3,
                    height=1,
                    command=lambda row=r, col=c: self.square_clicked(row, col)
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[(r, c)] = btn
        self.update_ui()

    def square_clicked(self, r, c):
        piece = self.board[r][c]
        if self.selected_square is None:
            if piece != ".":
                is_white = piece.isupper()
                if (self.turn == "white" and is_white) or (self.turn == "black" and not is_white):
                    self.selected_square = (r, c)
                    self.buttons[(r, c)].config(bg="#7b68ee")
        else:
            sr, sc = self.selected_square
            self.board[r][c] = self.board[sr][sc]
            self.board[sr][sc] = "."
            self.selected_square = None
            self.turn = "black" if self.turn == "white" else "white"
            self.status_label.config(text=f"Turn: {self.turn.capitalize()}")
            self.update_ui()

    def update_ui(self):
        for r in range(9):
            for c in range(9):
                bg_color = "#e67e22" if (r + c) % 2 == 0 else "#d35400"
                txt = self.board[r][c] if self.board[r][c] != "." else ""
                self.buttons[(r, c)].config(text=txt, bg=bg_color)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
    root = tk.Tk()
    app = ShogiApp(root, mode)
    root.mainloop()
