import tkinter as tk
from tkinter import messagebox
import sys

class ChaturangaApp:
    def __init__(self, root, mode="PvP"):
        self.root = root
        self.root.title(f"Chaturanga - Mode: {mode}")
        self.root.geometry("600x720")
        self.root.config(bg="#34495e")

        self.mode = mode
        self.selected_square = None
        self.buttons = {}

        top_frame = tk.Frame(root, bg="#34495e")
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(top_frame, text="📖 How to Play", bg="#f39c12", fg="white", font=("Arial", 10, "bold"), command=self.show_rules).pack(side=tk.LEFT)
        
        self.status_label = tk.Label(top_frame, text="Turn: White (Click a piece to move)", font=("Arial", 10, "bold"), bg="#34495e", fg="#1abc9c")
        self.status_label.pack(side=tk.RIGHT)

        self.board_frame = tk.Frame(root, bg="#2c3e50", bd=3, relief="solid")
        self.board_frame.pack(pady=10)
        
        self.setup_board_data()
        self.create_board_ui()

    def show_rules(self):
        rules = (
            "CHATURANGA HINTS & RULES:\n\n"
            "• Objective: Trap the enemy Raja (King).\n"
            "• Ratha (Chariot): Moves straight lines (like a Rook).\n"
            "• Ashva (Horse): Moves in L-shapes (like a Knight).\n"
            "• Gaja (Elephant): Moves exactly 2 squares diagonally, can jump!\n"
            "• Mantri (Counselor): Moves 1 square diagonally.\n"
            "• Raja (King): Moves 1 square in any direction."
        )
        messagebox.showinfo("How to Play - Chaturanga", rules)

    def setup_board_data(self):
        # Board state array
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
        self.turn = "white" # 'white' or 'black'

    def create_board_ui(self):
        for r in range(8):
            for c in range(8):
                bg_color = "#f0d9b5" if (r + c) % 2 == 0 else "#b58863"
                btn = tk.Button(
                    self.board_frame,
                    text="",
                    font=("Arial", 18, "bold"),
                    width=3,
                    height=1,
                    bg=bg_color,
                    activebackground=bg_color,
                    command=lambda row=r, col=c: self.square_clicked(row, col)
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[(r, c)] = btn
        self.update_ui()

    def square_clicked(self, r, c):
        piece = self.board[r][c]

        if self.selected_square is None:
            if piece != ".":
                # Check turn color
                is_white_piece = piece.isupper()
                if (self.turn == "white" and is_white_piece) or (self.turn == "black" and not is_white_piece):
                    self.selected_square = (r, c)
                    self.highlight_moves(r, c)
        else:
            sr, sc = self.selected_square
            # Move piece
            self.board[r][c] = self.board[sr][sc]
            self.board[sr][sc] = "."
            self.selected_square = None
            
            # Switch turn
            self.turn = "black" if self.turn == "white" else "white"
            self.status_label.config(text=f"Turn: {self.turn.capitalize()}")
            self.update_ui()

            if self.mode == "PvAI" and self.turn == "black":
                self.root.after(500, self.ai_move)

    def highlight_moves(self, r, c):
        self.update_ui()
        self.buttons[(r, c)].config(bg="#7b68ee") # Selected highlight
        # Give friendly hints: highlight adjacent or reasonable helper squares
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 8 and 0 <= nc < 8 and (dr != 0 or dc != 0):
                    self.buttons[(nr, nc)].config(bg="#a9dfbf") # Suggested move helper

    def update_ui(self):
        for r in range(8):
            for c in range(8):
                bg_color = "#f0d9b5" if (r + c) % 2 == 0 else "#b58863"
                txt = self.board[r][c] if self.board[r][c] != "." else ""
                self.buttons[(r, c)].config(text=txt, bg=bg_color)

    def ai_move(self):
        # Basic automated move for AI mode
        import random
        pieces = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c].islower():
                    pieces.append((r, c))
        if pieces:
            fr, fc = random.choice(pieces)
            tr, tc = max(0, fr - 1), fc # move forward if possible
            self.board[tr][tc] = self.board[fr][fc]
            self.board[fr][fc] = "."
            self.turn = "white"
            self.status_label.config(text="Turn: White")
            self.update_ui()

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
    root = tk.Tk()
    app = ChaturangaApp(root, mode)
    root.mainloop()
