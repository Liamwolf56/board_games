import tkinter as tk
from tkinter import messagebox
import sys, random

class MonzaApp:
    def __init__(self, root, mode="PvP"):
        self.root = root
        self.root.title(f"Monza - Mode: {mode}")
        self.root.geometry("500x550")
        self.root.config(bg="#2c3e50")
        self.pos = 0

        top_frame = tk.Frame(root, bg="#2c3e50")
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Button(top_frame, text="📖 How to Play", bg="#f39c12", fg="white", font=("Arial", 9, "bold"), command=self.show_rules).pack(side=tk.LEFT)

        self.status_label = tk.Label(root, text="Position: Start Line (0/10)", font=("Arial", 12, "bold"), bg="#2c3e50", fg="#1abc9c")
        self.status_label.pack(pady=10)

        tk.Button(root, text="🎲 Roll 6 Colored Dice", font=("Arial", 12, "bold"), bg="#e74c3c", fg="white", command=self.roll_dice).pack(pady=10)
        self.dice_label = tk.Label(root, text="Dice: [ - - - - - - ]", font=("Arial", 14), bg="#2c3e50", fg="#f1c40f")
        self.dice_label.pack(pady=10)

    def show_rules(self):
        messagebox.showinfo("How to Play", "Roll 6 colored dice! Match the dice colors to the color sequence on the race track to zoom your race car ahead!")

    def roll_dice(self):
        colors = ["🔴", "🔵", "🟢", "🟡", "⚪", "🟣"]
        rolled = [random.choice(colors) for _ in range(6)]
        self.dice_label.config(text="Dice: " + " ".join(rolled))
        self.pos = min(10, self.pos + random.randint(1, 3))
        self.status_label.config(text=f"Position: Space {self.pos}/10")
        if self.pos == 10:
            messagebox.showinfo("Finish Line!", "🏎️ You won the Monza Grand Prix!")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
    root = tk.Tk()
    app = MonzaApp(root, mode)
    root.mainloop()
