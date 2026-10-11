import tkinter as tk
from tkinter import messagebox
import sys, random

class BattleshipApp:
    def __init__(self, root, mode="PvP"):
        self.root = root
        self.root.title(f"Battleship - Mode: {mode}")
        self.root.geometry("500x600")
        self.root.config(bg="#2c3e50")
        self.hits, self.shots = 0, 0

        top_frame = tk.Frame(root, bg="#2c3e50")
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Button(top_frame, text="📖 How to Play", bg="#f39c12", fg="white", font=("Arial", 9, "bold"), command=self.show_rules).pack(side=tk.LEFT)

        self.status_label = tk.Label(root, text="Shots: 0 | Hits: 0/5", font=("Arial", 12, "bold"), bg="#2c3e50", fg="#1abc9c")
        self.status_label.pack(pady=5)

        board_frame = tk.Frame(root, bg="#34495e", bd=3)
        board_frame.pack(pady=10)

        # 5 secret ship locations
        self.ships = set(random.sample([(r, c) for r in range(6) for c in range(6)], 5))
        self.buttons = {}

        for r in range(6):
            for c in range(6):
                btn = tk.Button(board_frame, text="🌊", font=("Arial", 16), width=3, height=1, bg="#2980b9", command=lambda row=r, col=c: self.fire(row, col))
                btn.grid(row=r, column=c, padx=2, pady=2)
                self.buttons[(r, c)] = btn

    def show_rules(self):
        messagebox.showinfo("How to Play", "Click the water grid to fire missiles! Find and sink all 5 hidden enemy ships.")

    def fire(self, r, c):
        btn = self.buttons[(r, c)]
        if btn["state"] == tk.DISABLED: return
        self.shots += 1
        if (r, c) in self.ships:
            btn.config(text="💥", bg="#e74c3c", state=tk.DISABLED)
            self.hits += 1
        else:
            btn.config(text="⚪", bg="#7f8c8d", state=tk.DISABLED)

        self.status_label.config(text=f"Shots: {self.shots} | Hits: {self.hits}/5")
        if self.hits == 5:
            messagebox.showinfo("Victory!", f"All enemy ships sunk in {self.shots} shots!")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
    root = tk.Tk()
    app = BattleshipApp(root, mode)
    root.mainloop()
