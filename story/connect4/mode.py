import os, json, tkinter as tk
from tkinter import messagebox

KING_DATA = {
    "game": "Connect 4",
    "title": "Gridmaster First Strike",
    "intro": "I go first and take the center column! Victory is mathematically mine!",
    "victory": "Four in a row! First-player advantage reigns supreme once again!",
    "defeat": "BLOCKED?! How did you counter my middle column drop?!"
}

class StoryConnect4:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Story Mode: {KING_DATA['title']}")
        self.root.geometry("460x520")
        self.root.config(bg="#1e272e")
        self.rows, self.cols = 6, 7
        self.grid = [["" for _ in range(7)] for _ in range(6)]
        
        tk.Label(root, text=f"👑 {KING_DATA['title']}", font=("Arial", 14, "bold"), fg="#ffdd59", bg="#1e272e").pack(pady=10)
        d = tk.Frame(root, bg="#2c3e50", padx=10, pady=5); d.pack(fill=tk.X, padx=15, pady=5)
        tk.Label(d, text=f"💬 \"{KING_DATA['intro']}\"", font=("Arial", 10, "italic"), fg="#00d8d6", bg="#2c3e50", wraplength=400).pack()

        g_frame = tk.Frame(root, bg="#1e272e"); g_frame.pack(pady=10)
        self.btns = []
        for r in range(6):
            row_btns = []
            for c in range(7):
                b = tk.Button(g_frame, text="", font=("Arial", 12, "bold"), width=4, height=2, bg="#34495e", command=lambda col=c: self.drop(col))
                b.grid(row=r, column=c, padx=2, pady=2)
                row_btns.append(b)
            self.btns.append(row_btns)

    def drop(self, col):
        for r in reversed(range(6)):
            if self.grid[r][col] == "":
                self.grid[r][col] = "X"
                self.btns[r][col].config(bg="#f1c40f")
                if self.check_win("X"): self.handle_win(); return
                self.ai_drop()
                return

    def ai_drop(self):
        for c in [3, 2, 4, 1, 5, 0, 6]:
            for r in reversed(range(6)):
                if self.grid[r][c] == "":
                    self.grid[r][c] = "O"
                    self.btns[r][c].config(bg="#e74c3c")
                    if self.check_win("O"): self.handle_loss()
                    return

    def check_win(self, p):
        for r in range(6):
            for c in range(7):
                if c+3 < 7 and all(self.grid[r][c+i] == p for i in range(4)): return True
                if r+3 < 6 and all(self.grid[r+i][c] == p for i in range(4)): return True
                if r+3 < 6 and c+3 < 7 and all(self.grid[r+i][c+i] == p for i in range(4)): return True
                if r-3 >= 0 and c+3 < 7 and all(self.grid[r-i][c+i] == p for i in range(4)): return True
        return False

    def handle_win(self):
        messagebox.showinfo("VICTORY! 🏆", f"{KING_DATA['title']} cries out in defeat:\n\n\"{KING_DATA['defeat']}\"")
        self.save(True); self.root.destroy()

    def handle_loss(self):
        messagebox.showerror("PERMADEATH! 💀", f"{KING_DATA['title']} gloats:\n\n\"{KING_DATA['victory']}\"\n\nRun Reset!")
        self.save(False); self.root.destroy()

    def save(self, win):
        p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "progress.json")
        if os.path.exists(p):
            try:
                with open(p, "r") as f: d = json.load(f)
                d["current_stage_idx"] = d["current_stage_idx"] + 1 if win else 0
                with open(p, "w") as f: json.dump(d, f)
            except Exception: pass

if __name__ == "__main__":
    root = tk.Tk(); StoryConnect4(root); root.mainloop()
