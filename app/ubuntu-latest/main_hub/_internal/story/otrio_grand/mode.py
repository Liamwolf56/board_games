import json
import os
import random
import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Button

KING_DATA = {
    "name": "Otrio Grand Master",
    "description": "The ring emperor who demands absolute concentric control across three dimensions!",
    "unlocked_by": "checkers",
}

class StoryOtrioGrandApp:
    def __init__(self, root, player_name="Liam", story_frame=None):
        self.root = root
        self.player_name = player_name
        self.story_frame = story_frame
        self.root.title(f"King 9: Otrio Grand Master — {self.player_name} vs King AI")
        self.root.geometry("460x520")
        
        self.show_king_intro()
        
        self.board = [[ [None, None, None] for _ in range(3)] for _ in range(3)]
        self.buttons = []
        self.turn = "Player" # Player = Red, AI = Purple
        
        self.status_label = Label(self.root, text=f"Your Turn ({self.player_name}) [Red] vs Grand Master AI [Purple]", font=("Arial", 11, "bold"))
        self.status_label.pack(pady=10)
        
        grid_frame = tk.Frame(self.root)
        grid_frame.pack(pady=5)
        
        for r in range(3):
            row_btns = []
            for c in range(3):
                btn = Button(grid_frame, text="[   ]", font=("Arial", 12, "bold"), width=9, height=3,
                             bg="#f0f0f0", command=lambda row=r, col=c: self.player_click(row, col))
                btn.grid(row=r, column=c, padx=4, pady=4)
                row_btns.append(btn)
            self.buttons.append(row_btns)
            
        Button(self.root, text="Surrender / Quit", command=self.handle_defeat, fg="red", width=15).pack(pady=10)

    def show_king_intro(self):
        intro_win = Toplevel(self.root)
        intro_win.title("King's Chamber")
        intro_win.geometry("380x220")
        
        Label(intro_win, text="👑 King 9: The Ring Emperor 👑", font=("Arial", 12, "bold")).pack(pady=10)
        Label(intro_win, text=f"\"You survived basic checkers, {self.player_name}? Now face the Grand Master of Otrio—where every ring is a trap!\"", font=("Arial", 10, "italic"), wraplength=330, justify="center").pack(pady=10)
        
        Button(intro_win, text="Fight!", command=intro_win.destroy, width=15, bg="#4CAF50", fg="white").pack(pady=15)

    def player_click(self, r, c):
        if self.turn != "Player":
            return
            
        placed_size = -1
        for s in range(3):
            if self.board[r][c][s] is None:
                self.board[r][c][s] = "Player"
                placed_size = s
                break
                
        if placed_size == -1:
            return
            
        self.update_button_text(r, c)
        
        if self.check_win("Player"):
            self.handle_victory()
            return
            
        if self.is_board_full():
            messagebox.showinfo("Draw", "The Grand Ring matrix is full! It's a draw.")
            self.root.destroy()
            return
            
        self.turn = "AI"
        self.status_label.config(text="Grand Master AI is calculating concentric traps...")
        self.root.after(700, self.ai_move)

    def ai_move(self):
        open_slots = []
        for r in range(3):
            for c in range(3):
                for s in range(3):
                    if self.board[r][c][s] is None:
                        open_slots.append((r, c, s))
                        
        if not open_slots:
            return
            
        r, c, s = random.choice(open_slots)
        self.board[r][c][s] = "AI"
        self.update_button_text(r, c)
        
        if self.check_win("AI"):
            self.handle_defeat()
            return
            
        if self.is_board_full():
            messagebox.showinfo("Draw", "The Grand Ring matrix is full! It's a draw.")
            self.root.destroy()
            return
            
        self.turn = "Player"
        self.status_label.config(text=f"Your Turn ({self.player_name}) [Red] vs Grand Master AI [Purple]")

    def update_button_text(self, r, c):
        p_count = sum(1 for x in self.board[r][c] if x == "Player")
        a_count = sum(1 for x in self.board[r][c] if x == "AI")
        text = f"P:{p_count} | A:{a_count}"
        bg_color = "#ffcccc" if p_count > a_count else ("#e1bee7" if a_count > p_count else "#e0e0e0")
        self.buttons[r][c].config(text=text, bg=bg_color)

    def check_win(self, owner):
        for r in range(3):
            for c in range(3):
                if all(self.board[r][c][s] == owner for s in range(3)):
                    return True
                    
        for s in range(3):
            for r in range(3):
                if all(self.board[r][c][s] == owner for c in range(3)):
                    return True
            for c in range(3):
                if all(self.board[r][c][s] == owner for r in range(3)):
                    return True
            if all(self.board[i][i][s] == owner for i in range(3)):
                return True
            if all(self.board[i][2-i][s] == owner for i in range(3)):
                return True
                
        return False

    def is_board_full(self):
        return all(self.board[r][c][s] is not None for r in range(3) for c in range(3) for s in range(3))

    def handle_victory(self):
        if self.story_frame:
            self.story_frame.kings_defeated_this_run += 1
            self.story_frame.update_header()

        messagebox.showinfo(
            "Victory!", 
            f"King 9: \"My Grand Ring matrix shattered! Extraordinary mind, {self.player_name}... King 10 awaits!\""
        )
        self.root.destroy()

    def handle_defeat(self):
        self.root.destroy()
        if self.story_frame:
            self.story_frame.end_run(was_victory=False)

def run_mode(root, player_name="Liam", story_frame=None):
    app = StoryOtrioGrandApp(root, player_name=player_name, story_frame=story_frame)
    return app
