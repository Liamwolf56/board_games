import tkinter as tk
from tkinter import messagebox
import sys

class ChaturangaApp:
    def __init__(self, root, mode="PvP"):
        self.root = root
        self.root.title(f"Chaturanga - Mode: {mode}")
        self.root.geometry("600x750")
        self.root.config(bg="#34495e")

        self.mode = mode
        self.selected_square = None
        self.buttons = {}
        self.game_over = False

        top_frame = tk.Frame(root, bg="#34495e")
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(top_frame, text="📖 How to Play", bg="#f39c12", fg="white", font=("Arial", 9, "bold"), command=self.show_rules).pack(side=tk.LEFT)
        
        # Win declaration buttons for friends playing together
        win_frame = tk.Frame(top_frame, bg="#34495e")
        win_frame.pack(side=tk.RIGHT)
        tk.Button(win_frame, text="White Wins!", bg="#27ae60", fg="white", font=("Arial", 9, "bold"), command=lambda: self.declare_winner("White")).pack(side=tk.LEFT, padx=2)
        tk.Button(win_frame, text="Black Wins!", bg="#c0392b", fg="white", font=("Arial", 9, "bold"), command=lambda: self.declare_winner("Black")).pack(side=tk.LEFT, padx=2)

        self.status_label = tk.Label(root, text="Turn: White (Select a piece)", font=("Arial", 11, "bold"), bg="#34495e", fg="#1abc9c")
        self.status_label.pack(pady=5)

        self.board_frame = tk.Frame(root, bg="#2c3e50", bd=3, relief="solid")
        self.board_frame.pack(pady=5)
        
        self.setup_board_data()
        self.create_board_ui()

    def show_rules(self):
        messagebox.showinfo("How to Play - Chaturanga", "Capture or trap the opposing Raja (King) to win! Use the 'White Wins!' or 'Black Wins!' buttons at the top to end the game.")

    def setup_board_data(self):
        self.board = [
            ["R", "N", "E", "M", "K", "E", "N", "R"],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["r", "n", "e", "m", "k", "e", "n", "r"]
        ]
        self.turn = "white"

    def create_board_ui(self):
        for r in range(8):
            for c in range(8):
                btn = tk.Button(self.board_frame, text="", font=("Arial", 18, "bold"), width=3, height=1, command=lambda row=r, col=c: self.square_clicked(row, col))
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[(r, c)] = btn
        self.update_ui()

    def square_clicked(self, r, c):
        if self.game_over:
            return
        piece = self.board[r][c]
        if self.selected_square is None:
            if piece != ".":
                is_white = piece.isupper()
                if (self.turn == "white" and is_white) or (self.turn == "black" and not is_white):
                    self.selected_square = (r, c)
                    self.buttons[(r, c)].config(bg="#7b68ee")
        else:
            sr, sc = self.selected_square
            self.board[r][c] = self.board[sr][sc]
            self.board[sr][sc] = "."
            self.selected_square = None
            self.turn = "black" if self.turn == "white" else "white"
            self.status_label.config(text=f"Turn: {self.turn.capitalize()}")
            self.update_ui()

    def declare_winner(self, winner):
        self.game_over = True
        messagebox.showinfo("🏆 Game Over!", f"Victory! {winner} side has won the match!")
        self.status_label.config(text=f"Game Over: {winner} Won!", fg="#f1c40f")

    def update_ui(self):
        for r in range(8):
            for c in range(8):
                bg_color = "#f0d9b5" if (r + c) % 2 == 0 else "#b58863"
                txt = self.board[r][c] if self.board[r][c] != "." else ""
                self.buttons[(r, c)].config(text=txt, bg=bg_color)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
    root = tk.Tk()
    app = ChaturangaApp(root, mode)
    root.mainloop()
