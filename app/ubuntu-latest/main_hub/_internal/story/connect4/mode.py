import sys
import tkinter as tk
from tkinter import messagebox

KING_DATA = {
    "name": "Gridmaster First Strike",
    "desc": "Connect 4"
}

class Connect4App:
    def __init__(self, root, player_name="Player", story_frame=None):
        self.root = root
        self.player_name = player_name
        self.story_frame = story_frame
        self.mode = "PvAI"
        
        self.root.title(f"Story Mode: {self.player_name} vs Gridmaster First Strike")
        self.root.geometry("600x740")
        self.root.config(bg="#2c3e50")

        self.board = [["" for _ in range(7)] for _ in range(6)]
        self.turn = "Red"
        self.game_over = False

        self.red_time = 300
        self.yellow_time = 300
        self.timer_running = True

        top_frame = tk.Frame(root, bg="#2c3e50")
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(
            top_frame,
            text="📖 How to Play",
            bg="#f39c12",
            fg="white",
            font=("Arial", 9, "bold"),
            command=self.show_rules,
        ).pack(side=tk.LEFT)

        self.timer_label = tk.Label(
            top_frame,
            text=f"{self.player_name}: 05:00 | King: 05:00",
            font=("Arial", 11, "bold"),
            bg="#2c3e50",
            fg="white",
        )
        self.timer_label.pack(side=tk.RIGHT)

        self.status_label = tk.Label(
            root,
            text=f"Turn: {self.player_name} Player",
            font=("Arial", 13, "bold"),
            bg="#2c3e50",
            fg="#e74c3c",
        )
        self.status_label.pack(pady=5)

        # Column drop buttons at the top
        drop_frame = tk.Frame(root, bg="#2c3e50")
        drop_frame.pack(pady=5)
        for c in range(7):
            btn = tk.Button(
                drop_frame,
                text=f"▼ {c+1}",
                font=("Arial", 10, "bold"),
                width=5,
                bg="#485460",
                fg="white",
                command=lambda col=c: self.drop_piece(col),
            )
            btn.grid(row=0, column=c, padx=3)

        # Board Container
        board_frame = tk.Frame(root, bg="#2980b9", bd=5, relief="solid")
        board_frame.pack(pady=10)

        self.buttons = {}
        for r in range(6):
            for c in range(7):
                cell = tk.Button(
                    board_frame,
                    text="",
                    width=5,
                    height=2,
                    bg="#34495e",
                    state=tk.DISABLED,
                    relief="flat",
                )
                cell.grid(row=r, column=c, padx=2, pady=2)
                self.buttons[(r, c)] = cell

        self.update_timer()

    def show_rules(self):
        rules = (
            "CONNECT 4 (STORY MODE):\n\n"
            "• Click the '▼' buttons at the top of each column to drop your piece.\n"
            "• You go first against Gridmaster First Strike (Yellow).\n"
            "• First to connect 4 matching colored pieces horizontally, vertically, or diagonally wins the campaign battle!"
        )
        messagebox.showinfo("How to Play - Connect 4", rules)

    def drop_piece(self, col):
        if self.game_over:
            return

        target_row = -1
        for r in reversed(range(6)):
            if self.board[r][col] == "":
                target_row = r
                break

        if target_row != -1:
            self.board[target_row][col] = self.turn
            color_code = "#e74c3c" if self.turn == "Red" else "#f1c40f"
            self.buttons[(target_row, col)].config(bg=color_code)

            if self.check_win(target_row, col):
                self.game_over = True
                self.timer_running = False
                if self.turn == "Red":
                    if self.story_frame:
                        self.story_frame.kings_defeated_this_run += 1
                    messagebox.showinfo("King Defeated!", f"🏆 {self.player_name} connected 4 and defeated Gridmaster First Strike!")
                    self.root.destroy()
                else:
                    if self.story_frame:
                        self.story_frame.end_run(was_victory=False)
                    messagebox.showinfo("Defeat", "Gridmaster First Strike defeated you!")
                    self.root.destroy()
                return
            elif all(self.board[0][c] != "" for c in range(7)):
                self.game_over = True
                self.timer_running = False
                if self.story_frame:
                    self.story_frame.end_run(was_victory=False)
                messagebox.showinfo("Game Over", "It's a Draw! Run ended.")
                self.root.destroy()
                return
            else:
                self.turn = "Yellow" if self.turn == "Red" else "Red"
                display_name = self.player_name if self.turn == "Red" else "Gridmaster First Strike"
                next_color = "#e74c3c" if self.turn == "Red" else "#f1c40f"
                self.status_label.config(
                    text=f"Turn: {display_name}", fg=next_color
                )

                if self.turn == "Yellow" and not self.game_over:
                    self.root.after(500, self.ai_move)

    def ai_move(self):
        import random

        valid_cols = [c for c in range(7) if self.board[0][c] == ""]
        if valid_cols:
            ai_col = random.choice(valid_cols)
            self.drop_piece(ai_col)

    def check_win(self, r, c):
        p = self.board[r][c]
        dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in dirs:
            cnt = 1
            for step in (1, -1):
                nr, nc = r + dr * step, c + dc * step
                while 0 <= nr < 6 and 0 <= nc < 7 and self.board[nr][nc] == p:
                    cnt += 1
                    nr += dr * step
                    nc += dc * step
            if cnt >= 4:
                return True
        return False

    def update_timer(self):
        if self.timer_running and not self.game_over:
            if self.turn == "Red":
                if self.red_time > 0:
                    self.red_time -= 1
            else:
                if self.yellow_time > 0:
                    self.yellow_time -= 1

            r_min, r_sec = divmod(self.red_time, 60)
            y_min, y_sec = divmod(self.yellow_time, 60)
            self.timer_label.config(
                text=f"{self.player_name}: {r_min:02d}:{r_sec:02d} | King: {y_min:02d}:{y_sec:02d}"
            )

            if self.red_time == 0 or self.yellow_time == 0:
                self.game_over = True
                self.timer_running = False
                if self.red_time == 0:
                    if self.story_frame:
                        self.story_frame.end_run(was_victory=False)
                    messagebox.showinfo("Time Out!", f"{self.player_name} ran out of time! Gridmaster First Strike wins!")
                else:
                    if self.story_frame:
                        self.story_frame.kings_defeated_this_run += 1
                    messagebox.showinfo("Time Out!", "Gridmaster First Strike ran out of time! You win!")
                self.root.destroy()
                return

        self.root.after(1000, self.update_timer)

def run_mode(parent, player_name="Player", story_frame=None):
    app = Connect4App(parent, player_name=player_name, story_frame=story_frame)
    return app
