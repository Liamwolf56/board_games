import tkinter as tk
from tkinter import messagebox
import sys

class AnimalStackApp:
    def __init__(self, root, mode="PvP"):
        self.root = root
        self.root.title(f"Animal Upon Animal - Mode: {mode}")
        self.root.geometry("450x550")
        self.root.config(bg="#27ae60")
        self.stack = ["🐊 (Crocodile Base)"]

        top_frame = tk.Frame(root, bg="#27ae60")
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Button(top_frame, text="📖 How to Play", bg="#f39c12", fg="white", font=("Arial", 9, "bold"), command=self.show_rules).pack(side=tk.LEFT)

        self.status_label = tk.Label(root, text="Stack height: 1 animal", font=("Arial", 12, "bold"), bg="#27ae60", fg="white")
        self.status_label.pack(pady=5)

        btn_frame = tk.Frame(root, bg="#27ae60")
        btn_frame.pack(pady=10)

        animals = [("🐍 Snake", "🐍"), ("🦩 Flamingo", "🦩"), ("🐒 Monkey", "🐒"), ("🦔 Hedgehog", "🦔")]
        for name, icon in animals:
            tk.Button(btn_frame, text=f"Stack {name}", font=("Arial", 11, "bold"), bg="#f1c40f", width=18, command=lambda ic=icon: self.stack_animal(ic)).pack(pady=5)

    def show_rules(self):
        messagebox.showinfo("How to Play", "Roll the die and carefully stack your wooden animals on top of the crocodile without tumbling the pyramid!")

    def stack_animal(self, icon):
        self.stack.append(icon)
        self.status_label.config(text=f"Stack height: {len(self.stack)} animals! Top: {icon}")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
    root = tk.Tk()
    app = AnimalStackApp(root, mode)
    root.mainloop()
