import json
import os
import random
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Label, Button

from leaderboard import record_score, load_leaderboard
from story.sequence_for_kids.mode import KING_DATA as k1
from story.connect4.mode import KING_DATA as k2
from story.otrio.mode import KING_DATA as k3
from story.battleship.mode import KING_DATA as k4
from story.animal_upon_animal.mode import KING_DATA as k5
from story.monza.mode import KING_DATA as k6
from story.tic_tac_toe.mode import KING_DATA as k7
from story.checkers.mode import KING_DATA as k8
from story.reversi.mode import KING_DATA as k9
from story.shogi.mode import KING_DATA as k10
from story.xiangqi.mode import KING_DATA as k11
from story.chaturanga.mode import KING_DATA as k12
from story.yahtzee.mode import KING_DATA as k13
from story.mastermind.mode import KING_DATA as k14
from story.chess.mode import KING_DATA as k15

# Master pools: 14 randomizable gauntlet kings + 1 fixed final boss
GAUNTLET_POOL = [
    ("story.sequence_for_kids.mode", {"name": "High Lord Wild Unicorn", "desc": "Sequence for Kids"}),
    ("story.connect4.mode", {"name": "Gridmaster First Strike", "desc": "Connect 4"}),
    ("story.otrio.mode", {"name": "High Lord Concentric Ring", "desc": "Otrio"}),
    ("story.battleship.mode", {"name": "Admiral Blind Grid", "desc": "Battleship"}),
    ("story.animal_upon_animal.mode", {"name": "High Sovereign Apex Stack", "desc": "Animal Upon Animal"}),
    ("story.monza.mode", {"name": "High Lord Turbo Combo", "desc": "Monza"}),
    ("story.tic_tac_toe.mode", {"name": "King Ultimate Gridlock", "desc": "Tic-Tac-Toe"}),
    ("story.checkers.mode", {"name": "High King Crown Jump", "desc": "Checkers"}),
    ("story.reversi.mode", {"name": "Sovereign Flipside", "desc": "Reversi"}),
    ("story.shogi.mode", {"name": "Emperor Dragon King", "desc": "Shogi"}),
    ("story.xiangqi.mode", {"name": "Grand General Sky Cannon", "desc": "Xiangqi"}),
    ("story.chaturanga.mode", {"name": "Raja Four-Fold War", "desc": "Chaturanga"}),
    ("story.yahtzee.mode", {"name": "High Lord Five-of-a-Kind", "desc": "Yahtzee"}),
    ("story.mastermind.mode", {"name": "Grandmaster Cipher Lock", "desc": "Mastermind"}),
]
FINAL_BOSS = ("story.chess.mode", {"name": "King Chess.com", "desc": "Chess"})

class StoryModeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.player_name = None
        self.kings_defeated_this_run = 0
        self.current_run_nodes = []
        
        self.title_label = tk.Label(self, text="⚔️ Story Mode: King's Gauntlet ⚔️", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)
        
        self.score_label = tk.Label(
            self, 
            text="Start a new run to begin!", 
            font=("Arial", 11, "bold"), 
            fg="#2196F3"
        )
        self.score_label.pack(pady=2)

        tk.Button(
            self, 
            text="🏆 View Leaderboard", 
            font=("Arial", 11, "bold"), 
            bg="#ffd700", 
            fg="#000000",
            command=self.show_leaderboard
        ).pack(pady=5)
        
        tk.Label(
            self, 
            text="Defeat as many Kings as possible! Every run has a randomized order. A single loss ends your run.", 
            font=("Arial", 10, "italic")
        ).pack(pady=5)
        
        canvas = tk.Canvas(self, height=350)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.nodes_frame = tk.Frame(canvas)
        
        self.nodes_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.nodes_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        
        tk.Button(self, text="Back to Main Menu", command=self.go_back).pack(pady=10)
        
        self.current_run_nodes = list(GAUNTLET_POOL) + [FINAL_BOSS]
        self.refresh_map()

    def start_new_run_if_needed(self):
        if not self.player_name:
            user_input = simpledialog.askstring(
                "New Story Campaign", 
                "Enter Player Name for this Gauntlet Run:", 
                initialvalue="Liam"
            )
            if user_input and user_input.strip():
                self.player_name = user_input.strip()
            else:
                self.player_name = "Challenger"
                
            self.kings_defeated_this_run = 0
            
            # Randomize the 14 gauntlet nodes for this run
            shuffled_pool = list(GAUNTLET_POOL)
            random.shuffle(shuffled_pool)
            self.current_run_nodes = shuffled_pool + [FINAL_BOSS]
            
            self.update_header()
            self.refresh_map()

    def update_header(self):
        if self.player_name:
            self.title_label.config(text=f"⚔️ Story Mode: {self.player_name}'s Campaign ⚔️")
            self.score_label.config(text=f"Current Run Progress: {self.kings_defeated_this_run}/15 Kings Defeated")

    def end_run(self, was_victory=False):
        final_score = self.kings_defeated_this_run
        name = self.player_name or "Challenger"
        
        record_score(name, final_score, beat_chess=was_victory)
        
        if was_victory:
            messagebox.showinfo(
                "🏆 GRAND CHAMPION! 🏆",
                f"CONGRATULATIONS {name}!\nYou defeated all 15 Kings and conquered King Chess.com!\n"
                f"Your score of {final_score} with ⭐ status has been recorded on the Leaderboard."
            )
        else:
            messagebox.showinfo(
                "☠️ GAME OVER ☠️",
                f"Your run has ended, {name}.\nFinal Score: {final_score} Kings Defeated.\n"
                f"Your result has been posted to the Leaderboard!"
            )
            
        self.player_name = None
        self.kings_defeated_this_run = 0
        self.current_run_nodes = list(GAUNTLET_POOL) + [FINAL_BOSS]
        self.title_label.config(text="⚔️ Story Mode: King's Gauntlet ⚔️")
        self.score_label.config(text="Start a new run to begin!")
        self.refresh_map()

    def go_back(self):
        if self.controller and hasattr(self.controller, "show_screen"):
            self.controller.show_screen("arcade")
        else:
            self.pack_forget()

    def show_leaderboard(self):
        lb_window = Toplevel(self)
        lb_window.title("Story Mode Leaderboard")
        lb_window.geometry("400x450")
        
        Label(lb_window, text="🏆 Hall of Champions 🏆", font=("Arial", 14, "bold")).pack(pady=10)
        
        data = load_leaderboard()
                
        if not data:
            Label(lb_window, text="No scores recorded yet!", font=("Arial", 10)).pack(pady=20)
        else:
            for i, entry in enumerate(data):
                disp_name = entry.get("display_name", entry.get("name", "Player"))
                kings = entry.get("kings_defeated", 0)
                text = f"{i+1}. {disp_name} — {kings}/15 Kings Defeated"
                Label(lb_window, text=text, font=("Arial", 11)).pack(anchor="w", padx=25, pady=4)
                
        Button(lb_window, text="Close", command=lb_window.destroy, width=12).pack(pady=15)

    def refresh_map(self):
        for widget in self.nodes_frame.winfo_children():
            widget.destroy()
            
        for idx, (mod_path, king_info) in enumerate(self.current_run_nodes):
            state = "normal" if self.kings_defeated_this_run >= idx else "disabled"
            is_done = " ✅" if self.kings_defeated_this_run > idx else ""
            prefix = "👑 FINAL BOSS: " if idx == 14 else f"King {idx+1}: "
            
            btn = tk.Button(
                self.nodes_frame,
                text=f"{prefix}{king_info['name']} ({king_info['desc']}){is_done}",
                font=("Arial", 10, "bold" if idx == 14 else "normal"),
                bg="#e1bee7" if idx == 14 else "#f0f0f0",
                width=42,
                state=state,
                command=lambda i=idx, mp=mod_path: self.launch_generic(i, mp)
            )
            btn.pack(pady=3)

    def launch_generic(self, idx, mod_name):
        if idx > 0 and self.kings_defeated_this_run < idx:
            messagebox.showwarning("Node Locked", "You must defeat the previous Kings to unlock this node!")
            return
            
        self.start_new_run_if_needed()
        if not self.player_name:
            return
            
        import importlib
        try:
            mod = importlib.import_module(mod_name)
        except Exception as e:
            messagebox.showerror("Module Error", f"Could not load game module {mod_name}:\n{e}")
            return
            
        game_window = Toplevel(self)
        king_name = self.current_run_nodes[idx][1]['name']
        game_window.title(f"Node {idx+1}: {king_name} — Player: {self.player_name}")
        
        try:
            app = mod.run_mode(game_window, player_name=self.player_name, story_frame=self)
        except Exception as e:
            messagebox.showerror("Launch Error", f"Could not start game:\n{e}")
            game_window.destroy()
            return
            
        self.wait_window(game_window)
        self.refresh_map()
