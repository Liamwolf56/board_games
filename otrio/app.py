import tkinter as tk
from tkinter import messagebox
import sys

class OtrioApp:
    def __init__(self, root, mode="PvP"):
        self.root = root
        self.root.title(f"Otrio - Mode: {mode}")
        self.root.geometry("450x550")
        self.root.config(bg="#2c3e50")
        self.turn = "Red"

        top_frame = tk.Frame(root, bg="#2c3e50")
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Button(top_frame, text="📖 How to Play", bg="#f39c12", fg="white", font=("Arial", 9, "bold"), command=self.show_rules).pack(side=tk.LEFT)

        self.status_label = tk.Label(root, text="Turn: Red Player", font=("Arial", 12, "bold"), bg="#2c3e50", fg="#e74c3c")
        self.status_label.pack(pady=5)

        board_frame = tk.Frame(root, bg="#34495e", bd=3)
        board_frame.pack(pady=10)

        # 3x3 board where each cell supports sizes: Big, Med, Small
        self.buttons = {}
        for r in range(3):
            for c in range(3):
                cell_frame = tk.Frame(board_frame, bg="#ecf0f1", bd=1, relief="solid")
                cell_frame.grid(row=r, column=c, padx=3, pady=3)
                for size in ["B", "M", "S"]:
                    btn = tk.Button(cell_frame, text=size, font=("Arial", 9, "bold"), width=2, command=lambda row=r, col=c, sz=size: self.place(row, col, sz))
                    btn.pack(side=tk.LEFT, padx=1)
                    self.buttons[(r, c, size)] = btn

    def show_rules(self):
        messagebox.showinfo("How to Play", "Otrio is nested Tic-Tac-Toe! Win by getting 3 pieces in a row of either:\n1. Same size in a line.\n2. Ascending/Descending size in a line.\n3. Concentric circles in 1 square.")

    def place(self, r, c, sz):
        btn = self.buttons[(r, c, sz)]
        color = "#e74c3c" if self.turn == "Red" else "#2980b9"
        btn.config(bg=color, fg="white", state=tk.DISABLED)
        self.turn = "Blue" if self.turn == "Red" else "Red"
        self.status_label.config(text=f"Turn: {self.turn} Player", fg="#2980b9" if self.turn == "Blue" else "#e74c3c")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
    root = tk.Tk()
    app = OtrioApp(root, mode)
    root.mainloop()
