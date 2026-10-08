import tkinter as tk
from tkinter import messagebox
import sys

class XiangqiApp:
    def __init__(self, root, mode="PvP"):
        self.root = root
        self.root.title(f"Xiangqi - Mode: {mode}")
        self.root.geometry("650x800")
        self.root.config(bg="#2c3e50")

        top_frame = tk.Frame(root, bg="#2c3e50")
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(top_frame, text="📖 How to Play Xiangqi", bg="#f39c12", fg="white", font=("Arial", 10, "bold"), command=self.show_rules).pack(side=tk.LEFT)
        tk.Label(top_frame, text="🏮 Chinese Chess (10x9)", font=("Arial", 10, "bold"), bg="#2c3e50", fg="white").pack(side=tk.RIGHT)

        self.board_frame = tk.Frame(root, bg="#d35400", bd=3, relief="solid")
        self.board_frame.pack(pady=10)
        self.create_board()

    def show_rules(self):
        rules = (
            "XIANGQI RULES:\n\n"
            "• Played on a 10x9 grid with a 'River' dividing the board in half.\n"
            "• Generals must stay inside a restricted 9-square 'Palace'.\n"
            "• Cannons jump over another piece to capture."
        )
        messagebox.showinfo("How to Play - Xiangqi", rules)

    def create_board(self):
        setup = [
            ["R", "H", "E", "A", "G", "A", "E", "H", "R"],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", "C", ".", ".", ".", ".", ".", "C", "."],
            ["S", ".", "S", ".", "S", ".", "S", ".", "S"],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["s", ".", "s", ".", "s", ".", "s", ".", "s"],
            [".", "c", ".", ".", ".", ".", ".", "c", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["r", "h", "e", "a", "g", "a", "e", "h", "r"]
        ]
        for r in range(10):
            for c in range(9):
                bg_color = "#f39c12" if (r + c) % 2 == 0 else "#e67e22"
                btn = tk.Button(self.board_frame, text=setup[r][c] if setup[r][c] != "." else "", font=("Arial", 12, "bold"), width=3, height=1, bg=bg_color)
                btn.grid(row=r, column=c, padx=1, pady=1)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
    root = tk.Tk()
    app = XiangqiApp(root, mode)
    root.mainloop()
