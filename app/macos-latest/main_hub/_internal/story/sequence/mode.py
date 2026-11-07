import json
import os
import random
import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Button

KING_DATA = {
    "name": "Sequence",
    "description": "The Master of Cards who uses full-deck sequences and wild Jacks to control the board!",
    "unlocked_by": "chaturanga",
}

class StorySequenceApp:
    def __init__(self, root, player_name="Liam", story_frame=None):
        self.root = root
        self.player_name = player_name
        self.story_frame = story_frame
        self.root.title(f"King 13: Sequence — {self.player_name} vs King AI")
        self.root.geometry("450x500")
        
        self.show_king_intro()
        
        self.player_tokens = 5
        self.ai_tokens = 5
        self.sequence_count = 0
        self.turn = "Player"
        
        self.status_label = Label(self.root, text=f"Your Turn ({self.player_name}) [Blue Chips] vs King AI [Green Chips]", font=("Arial", 11, "bold"))
        self.status_label.pack(pady=10)
        
        self.score_label = Label(self.root, text=f"🔵 Your Chips: {self.player_tokens}  |  🟢 King AI Chips: {self.ai_tokens}", font=("Arial", 12, "bold"), fg="#2196F3")
        self.score_label.pack(pady=15)
        
        self.action_frame = tk.Frame(self.root)
        self.action_frame.pack(pady=10)
        
        self.play_btn = Button(self.action_frame, text="🃏 Play Card & Place Chip", font=("Arial", 11, "bold"), bg="#a8e6cf",
                               command=self.player_play)
        self.play_btn.pack(side="left", padx=10)
        
        self.jack_btn = Button(self.action_frame, text="🃏 Two-Eyed Jack (Wild)", font=("Arial", 11, "bold"), bg="#ffd3b6",
                               command=self.player_wild)
        self.jack_btn.pack(side="right", padx=10)
        
        Button(self.root, text="Surrender / Quit", command=self.handle_defeat, fg="red", width=15).pack(pady=20)

    def show_king_intro(self):
        intro_win = Toplevel(self.root)
        intro_win.title("King's Chamber")
        intro_win.geometry("380x220")
        
        Label(intro_win, text="👑 King 13: The Sequence Sovereign 👑", font=("Arial", 12, "bold")).pack(pady=10)
        Label(intro_win, text=f"\"You bested the ancient armies, {self.player_name}? Now face full Sequence—where wild Jacks turn the tide!\"", font=("Arial", 10, "italic"), wraplength=330, justify="center").pack(pady=10)
        
        Button(intro_win, text="Fight!", command=intro_win.destroy, width=15, bg="#4CAF50", fg="white").pack(pady=15)

    def player_play(self):
        if self.turn != "Player":
            return
            
        if random.random() < 0.40:
            self.player_tokens -= 1
            messagebox.showinfo("Chip Placed!", f"{self.player_name} completed a 4-in-a-row chip sequence!")
            
        self.update_display()
        
        if self.player_tokens <= 0:
            self.handle_victory()
            return
            
        self.turn = "AI"
        self.status_label.config(text="King AI is scanning for sequence completions...")
        self.root.after(800, self.ai_move)

    def player_wild(self):
        if self.turn != "Player":
            return
            
        if random.random() < 0.70:
            self.player_tokens -= 1
            messagebox.showinfo("Wild Jack!", f"{self.player_name} used a Two-Eyed Jack to place a chip anywhere!")
        else:
            self.ai_tokens -= 1
            messagebox.showwarning("One-Eyed Jack!", "King AI removed one of your key chips with a One-Eyed Jack!")
            
        self.update_display()
        
        if self.player_tokens <= 0:
            self.handle_victory()
            return
            
        if self.ai_tokens <= 0:
            self.handle_defeat()
            return
            
        self.turn = "AI"
        self.status_label.config(text="King AI is scanning for sequence completions...")
        self.root.after(800, self.ai_move)

    def ai_move(self):
        if random.random() < 0.45:
            self.ai_tokens -= 1
            
        self.update_display()
        
        if self.ai_tokens <= 0:
            self.handle_defeat()
            return
            
        if self.player_tokens <= 0:
            self.handle_victory()
            return
            
        self.turn = "Player"
        self.status_label.config(text=f"Your Turn ({self.player_name}) [Blue Chips] vs King AI [Green Chips]")

    def update_display(self):
        self.score_label.config(text=f"🔵 Your Chips: {self.player_tokens}  |  🟢 King AI Chips: {self.ai_tokens}")

    def handle_victory(self):
        if self.story_frame:
            self.story_frame.kings_defeated_this_run += 1
            self.story_frame.update_header()

        messagebox.showinfo(
            "Victory!", 
            f"King 13: \"Two full sequences completed against me! Unbelievable card play, {self.player_name}... King 14 awaits!\""
        )
        self.root.destroy()

    def handle_defeat(self):
        self.root.destroy()
        if self.story_frame:
            self.story_frame.end_run(was_victory=False)

def run_mode(root, player_name="Liam", story_frame=None):
    app = StorySequenceApp(root, player_name=player_name, story_frame=story_frame)
    return app
