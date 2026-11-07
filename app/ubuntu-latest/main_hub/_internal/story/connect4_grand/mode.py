import json
import os
import random
import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Button

KING_DATA = {
    "name": "Connect 4 Grand Master",
    "description": "The supreme vertical strategist who calculates traps five steps ahead!",
    "unlocked_by": "sequence",
}

class StoryConnect4GrandApp:
    def __init__(self, root, player_name="Liam", story_frame=None):
        self.root = root
        self.player_name = player_name
        self.story_frame = story_frame
        self.root.title(f"King 14: Connect 4 Grand Master — {self.player_name} vs Grand AI")
        self.root.geometry("460x520")
        
        self.rows = 6
        self.cols = 7
        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.buttons = []
        self.turn = "Player" # Player = Red, AI = Gold
        
        self.show_king_intro()
        
        self.status_label = Label(self.root, text=f"Your Turn ({self.player_name}) [Red] vs Grand AI [Gold]", font=("Arial", 11, "bold"))
        self.status_label.pack(pady=10)
        
        grid_frame = tk.Frame(self.root)
        grid_frame.pack(pady=5)
        
        for r in range(self.rows):
            row_btns = []
            for c in range(self.cols):
                btn = Button(grid_frame, text="", font=("Arial", 12, "bold"), width=5, height=2,
                             bg="#e0e0e0", command=lambda col=c: self.drop_piece(col))
                btn.grid(row=r, column=c, padx=2, pady=2)
                row_btns.append(btn)
            self.buttons.append(row_btns)
            
        Button(self.root, text="Surrender / Quit", command=self.handle_defeat, fg="red", width=15).pack(pady=10)

    def show_king_intro(self):
        intro_win = Toplevel(self.root)
        intro_win.title("King's Chamber")
        intro_win.geometry("380x220")
        
        Label(intro_win, text="👑 King 14: The Grid Grand Master 👑", font=("Arial", 12, "bold")).pack(pady=10)
        Label(intro_win, text=f"\"Penultimate node, {self.player_name}! Before you face the Chess Emperor, prove your mastery of gravity drops against me!\"", font=("Arial", 10, "italic"), wraplength=330, justify="center").pack(pady=10)
        
        Button(intro_win, text="Fight!", command=intro_win.destroy, width=15, bg="#4CAF50", fg="white").pack(pady=15)

    def drop_piece(self, col):
        if self.turn != "Player":
            return
            
        target_row = -1
        for r in range(self.rows - 1, -1, -1):
            if self.board[r][col] is None:
                target_row = r
                break
                
        if target_row == -1:
            return
            
        self.board[target_row][col] = "Player"
        self.buttons[target_row][col].config(bg="#ff4d4d", text="🔴")
        
        if self.check_win("Player"):
            self.handle_victory()
            return
            
        if self.is_board_full():
            messagebox.showinfo("Draw", "The Grand grid is full! It's a draw.")
            self.root.destroy()
            return
            
        self.turn = "AI"
        self.status_label.config(text="Grand Master AI is calculating master drop angles...")
        self.root.after(700, self.ai_move)

    def ai_move(self):
        valid_cols = [c for c in range(self.cols) if self.board[0][c] is None]
        if not valid_cols:
            return
            
        col = random.choice(valid_cols)
        target_row = -1
        for r in range(self.rows - 1, -1, -1):
            if self.board[r][col] is None:
                target_row = r
                break
                
        self.board[target_row][col] = "AI"
        self.buttons[target_row][col].config(bg="#ffeb3b", text="🟡")
        
        if self.check_win("AI"):
            self.handle_defeat()
            return
            
        if self.is_board_full():
            messagebox.showinfo("Draw", "The Grand grid is full! It's a draw.")
            self.root.destroy()
            return
            
        self.turn = "Player"
        self.status_label.config(text=f"Your Turn ({self.player_name}) [Red] vs Grand AI [Gold]")

    def check_win(self, owner):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != owner:
                    continue
                if c + 3 < self.cols and all(self.board[r][c+i] == owner for i in range(4)):
                    return True
                if r + 3 < self.rows and all(self.board[r+i][c] == owner for i in range(4)):
                    return True
                if r + 3 < self.rows and c + 3 < self.cols and all(self.board[r+i][c+i] == owner for i in range(4)):
                    return True
                if r + 3 < self.rows and c - 3 >= 0 and all(self.board[r+i][c-i] == owner for i in range(4)):
                    return True
        return False

    def is_board_full(self):
        return all(self.board[0][c] is not None for c in range(self.cols))

    def handle_victory(self):
        if self.story_frame:
            self.story_frame.kings_defeated_this_run += 1
            self.story_frame.update_header()

        messagebox.showinfo(
            "Victory!", 
            f"King 14: \"Unbelievable... You connected 4 past my grandmaster defense! The Final Boss awaits you, {self.player_name}!\""
        )
        self.root.destroy()

    def handle_defeat(self):
        self.root.destroy()
        if self.story_frame:
            self.story_frame.end_run(was_victory=False)

def run_mode(root, player_name="Liam", story_frame=None):
    app = StoryConnect4GrandApp(root, player_name=player_name, story_frame=story_frame)
    return app
