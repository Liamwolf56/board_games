import tkinter as tk
from tkinter import messagebox
import sys

class Connect4App:
    def __init__(self, root, mode="PvP"):
        self.root = root
        self.root.title(f"Connect 4 - Mode: {mode}")
        self.root.geometry("550x600")
        self.root.config(bg="#2c3e50")
        self.board = [["" for _ in range(7)] for _ in range(6)]
        self.turn = "Red"
        self.game_over = False

        top_frame = tk.Frame(root, bg="#2c3e50")
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Button(top_frame, text="📖 How to Play", bg="#f39c12", fg="white", font=("Arial", 9, "bold"), command=self.show_rules).pack(side=tk.LEFT)

        self.status_label = tk.Label(root, text="Turn: Red Player", font=("Arial", 12, "bold"), bg="#2c3e50", fg="#e74c3c")
        self.status_label.pack(pady=5)

        board_frame = tk.Frame(root, bg="#2980b9", bd=5)
        board_frame.pack(pady=10)

        self.buttons = {}
        for r in range(6):
            for c in range(7):
                btn = tk.Button(board_frame, text="⚫", font=("Arial", 20), width=3, height=1, bg="#34495e", fg="#ecf0f1", command=lambda col=c: self.drop_piece(col))
                btn.grid(row=r, column=c, padx=2, pady=2)
                self.buttons[(r, c)] = btn

    def show_rules(self):
        messagebox.showinfo("How to Play", "Click any column to drop your piece! Be the first to connect 4 pieces horizontally, vertically, or diagonally.")

    def drop_piece(self, col):
        if self.game_over: return
        for r in reversed(range(6)):
            if self.board[r][col] == "":
                self.board[r][col] = self.turn
                color = "#e74c3c" if self.turn == "Red" else "#f1c40f"
                self.buttons[(r, col)].config(fg=color)
                if self.check_win(r, col):
                    self.game_over = True
                    messagebox.showinfo("Game Over", f"{self.turn} Player Wins!")
                    self.status_label.config(text=f"Winner: {self.turn}!", fg="#f1c40f")
                else:
                    self.turn = "Yellow" if self.turn == "Red" else "Red"
                    self.status_label.config(text=f"Turn: {self.turn} Player", fg=color)
                break

    def check_win(self, r, c):
        p = self.board[r][c]
        dirs = [(0,1), (1,0), (1,1), (1,-1)]
        for dr, dc in dirs:
            cnt = 1
            for step in (1, -1):
                nr, nc = r + dr*step, c + dc*step
                while 0 <= nr < 6 and 0 <= nc < 7 and self.board[nr][nc] == p:
                    cnt += 1
                    nr += dr*step
                    nc += dc*step
            if cnt >= 4: return True
        return False

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
    root = tk.Tk()
    app = Connect4App(root, mode)
    root.mainloop()
