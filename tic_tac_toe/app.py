import tkinter as tk
from tkinter import messagebox
import sys

class TicTacToeApp:
    def __init__(self, root, mode="PvP"):
        self.root = root
        self.root.title(f"Tic-Tac-Toe - Mode: {mode}")
        self.root.geometry("400x500")
        self.root.config(bg="#2c3e50")
        self.turn = "X"
        self.board = [""] * 9
        self.game_over = False

        top_frame = tk.Frame(root, bg="#2c3e50")
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Button(top_frame, text="📖 How to Play", bg="#f39c12", fg="white", font=("Arial", 9, "bold"), command=self.show_rules).pack(side=tk.LEFT)

        self.status_label = tk.Label(root, text="Turn: Player X", font=("Arial", 12, "bold"), bg="#2c3e50", fg="#1abc9c")
        self.status_label.pack(pady=5)

        board_frame = tk.Frame(root, bg="#34495e", bd=3)
        board_frame.pack(pady=10)

        self.buttons = []
        for i in range(9):
            btn = tk.Button(board_frame, text="", font=("Arial", 24, "bold"), width=3, height=1, bg="#ecf0f1", command=lambda idx=i: self.click(idx))
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.buttons.append(btn)

    def show_rules(self):
        messagebox.showinfo("How to Play", "Get 3 of your marks (X or O) in a row horizontally, vertically, or diagonally to win!")

    def click(self, idx):
        if self.board[idx] == "" and not self.game_over:
            self.board[idx] = self.turn
            self.buttons[idx].config(text=self.turn, fg="#e74c3c" if self.turn == "X" else "#2980b9")
            if self.check_win(self.turn):
                self.game_over = True
                messagebox.showinfo("Game Over", f"Player {self.turn} Wins!")
                self.status_label.config(text=f"Winner: Player {self.turn}!", fg="#f1c40f")
            elif "" not in self.board:
                self.game_over = True
                messagebox.showinfo("Game Over", "It's a Draw!")
                self.status_label.config(text="Game Draw!", fg="#bdc3c7")
            else:
                self.turn = "O" if self.turn == "X" else "X"
                self.status_label.config(text=f"Turn: Player {self.turn}")

    def check_win(self, p):
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        return any(self.board[a]==self.board[b]==self.board[c]==p for a,b,c in wins)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
    root = tk.Tk()
    app = TicTacToeApp(root, mode)
    root.mainloop()
