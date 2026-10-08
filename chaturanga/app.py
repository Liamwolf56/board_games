import tkinter as tk
from tkinter import messagebox
import sys

class ChaturangaApp:
    def __init__(self, root, mode="PvP"):
        self.root = root
        self.root.title(f"Chaturanga - Mode: {mode}")
        self.root.geometry("600x700")
        self.root.config(bg="#34495e")

        top_frame = tk.Frame(root, bg="#34495e")
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(top_frame, text="📖 How to Play Chaturanga", bg="#f39c12", fg="white", font=("Arial", 10, "bold"), command=self.show_rules).pack(side=tk.LEFT)
        tk.Label(top_frame, text="🐘 Ancient Ancestor of Chess", font=("Arial", 10, "bold"), bg="#34495e", fg="white").pack(side=tk.RIGHT)

        title_label = tk.Label(root, text="Chaturanga Board", font=("Arial", 14, "bold"), bg="#34495e", fg="white")
        title_label.pack(pady=5)

        self.board_frame = tk.Frame(root, bg="#2c3e50", bd=3, relief="solid")
        self.board_frame.pack(pady=10)
        self.create_board()

    def show_rules(self):
        rules = (
            "CHATURANGA RULES:\n\n"
            "• The historical Indian predecessor to Chess (circa 6th century).\n"
            "• Played on an 8x8 board.\n"
            "• Pieces: Raja (King), Mantri (Counselor/General), Gaja (Elephant), Ashva (Horse), Ratha (Chariot), and Padati (Pawn)."
        )
        messagebox.showinfo("How to Play - Chaturanga", rules)

    def create_board(self):
        setup = [
            ["R", "N", "E", "M", "K", "E", "N", "R"],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["r", "n", "e", "m", "k", "e", "n", "r"]
        ]
        for r in range(8):
            for c in range(8):
                bg_color = "#f0d9b5" if (r + c) % 2 == 0 else "#b58863"
                btn = tk.Button(self.board_frame, text=setup[r][c] if setup[r][c] != "." else "", font=("Arial", 18, "bold"), width=3, height=1, bg=bg_color)
                btn.grid(row=r, column=c, padx=1, pady=1)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
    root = tk.Tk()
    app = ChaturangaApp(root, mode)
    root.mainloop()
