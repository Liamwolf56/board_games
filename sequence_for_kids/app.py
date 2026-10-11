import tkinter as tk
from tkinter import messagebox
import sys, random

class SequenceKidsApp:
    def __init__(self, root, mode="PvP"):
        self.root = root
        self.root.title(f"Sequence for Kids - Mode: {mode}")
        self.root.geometry("550x650")
        self.root.config(bg="#2c3e50")

        animals = ["🦁", "🐘", "🦒", "🐵", "🐸", "🐻", "🐶", "🐱"]
        self.board_animals = [random.choice(animals) for _ in range(25)]

        top_frame = tk.Frame(root, bg="#2c3e50")
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Button(top_frame, text="📖 How to Play", bg="#f39c12", fg="white", font=("Arial", 9, "bold"), command=self.show_rules).pack(side=tk.LEFT)

        self.status_label = tk.Label(root, text="Place chip on matching animal to get 4 in a row!", font=("Arial", 11, "bold"), bg="#2c3e50", fg="#1abc9c")
        self.status_label.pack(pady=5)

        board_frame = tk.Frame(root, bg="#34495e", bd=3)
        board_frame.pack(pady=10)

        for i in range(25):
            btn = tk.Button(board_frame, text=self.board_animals[i], font=("Arial", 18), width=3, height=1, bg="#f39c12", command=lambda idx=i: self.claim(idx))
            btn.grid(row=i//5, column=i%5, padx=2, pady=2)

    def show_rules(self):
        messagebox.showinfo("How to Play", "Play animal cards and match them on the board! First to place 4 chips in a row wins.")

    def claim(self, idx):
        messagebox.showinfo("Sequence for Kids", f"Chip placed on {self.board_animals[idx]}!")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
    root = tk.Tk()
    app = SequenceKidsApp(root, mode)
    root.mainloop()
