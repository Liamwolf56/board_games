import random
import sys
import tkinter as tk
from tkinter import messagebox

KING_DATA = {
    "name": "Othello Overlord",
    "desc": "Reversi (Othello)"
}

class ReversiApp:
    def __init__(self, root, player_name="Player", story_frame=None):
        self.root = root
        self.player_name = player_name
        self.story_frame = story_frame
        self.mode = "PvAI"

        self.root.title(f"Story Mode: {self.player_name} vs Othello Overlord")
        self.root.geometry("680x780")
        self.root.config(bg="#1e272e")

        self.turn = "Black"  # Black (Player) vs White (Othello Overlord)
        self.game_over = False

        # 8x8 Board setup: "" = empty, "Black" = Black disc, "White" = White disc
        self.board = [["" for _ in range(8)] for _ in range(8)]
        self.init_board()

        # Timers (300 seconds / 5 mins)
        self.black_time = 300
        self.white_time = 300
        self.timer_running = True

        # Top Control Bar
        top_frame = tk.Frame(root, bg="#1e272e")
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(
            top_frame,
            text="How to Play",
            bg="#f39c12",
            fg="white",
            font=("Arial", 9, "bold"),
            command=self.show_rules,
        ).pack(side=tk.LEFT)

        self.timer_label = tk.Label(
            top_frame,
            text=f"{self.player_name}: 05:00 | King: 05:00",
            font=("Arial", 11, "bold"),
            bg="#1e272e",
            fg="white",
        )
        self.timer_label.pack(side=tk.RIGHT)

        self.score_label = tk.Label(
            root,
            text=f"{self.player_name}: 2 | King: 2",
            font=("Arial", 12, "bold"),
            bg="#1e272e",
            fg="#ffdd59",
        )
        self.score_label.pack(pady=3)

        self.status_label = tk.Label(
            root,
            text=f"Turn: {self.player_name} Player - Click a highlighted green tile to place disc",
            font=("Arial", 12, "bold"),
            bg="#1e272e",
            fg="#3498db",
        )
        self.status_label.pack(pady=5)

        # Board Grid Container
        board_frame = tk.Frame(root, bg="#2c3e50", bd=4, relief="solid")
        board_frame.pack(pady=10)

        self.buttons = {}
        for r in range(8):
            for c in range(8):
                btn = tk.Button(
                    board_frame,
                    text="",
                    font=("Arial", 10, "bold"),
                    width=6,
                    height=3,
                    bg="#27ae60",
                    command=lambda row=r, col=c: self.square_clicked(row, col),
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[(r, c)] = btn

        self.update_board_ui()
        self.update_timer()

    def init_board(self):
        self.board[3][3] = "White"
        self.board[3][4] = "Black"
        self.board[4][3] = "Black"
        self.board[4][4] = "White"

    def show_rules(self):
        rules = (
            "REVERSI (STORY MODE):\n\n"
            "1. Valid placement squares against Othello Overlord are highlighted in GREEN.\n"
            "2. Placing your disc traps opponent discs horizontally, vertically, or diagonally.\n"
            "3. Trapped opponent discs flip over to your color.\n"
            "4. If you have no valid moves, your turn is skipped.\n"
            "5. Finish with the most discs to defeat the King!"
        )
        messagebox.showinfo("How to Play - Reversi", rules)

    def get_flips(self, r, c, player):
        if self.board[r][c] != "":
            return []

        opponent = "White" if player == "Black" else "Black"
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]
        all_flips = []

        for dr, dc in directions:
            curr_r, curr_r_path = r + dr, []
            curr_c = c + dc

            while 0 <= curr_r < 8 and 0 <= curr_c < 8:
                target = self.board[curr_r][curr_c]
                if target == opponent:
                    curr_r_path.append((curr_r, curr_c))
                elif target == player:
                    if curr_r_path:
                        all_flips.extend(curr_r_path)
                    break
                else:
                    break
                curr_r += dr
                curr_c += dc

        return all_flips

    def get_valid_moves(self, player):
        valid = []
        for r in range(8):
            for c in range(8):
                if self.get_flips(r, c, player):
                    valid.append((r, c))
        return valid

    def square_clicked(self, r, c):
        if self.game_over or self.turn != "Black":
            return

        valid_moves = self.get_valid_moves(self.turn)
        if (r, c) not in valid_moves:
            messagebox.showwarning("Invalid Move", "You must place on a valid green square!")
            return

        flips = self.get_flips(r, c, self.turn)
        self.board[r][c] = self.turn
        for fr, fc in flips:
            self.board[fr][fc] = self.turn

        self.update_board_ui()
        self.check_game_state()

    def check_game_state(self):
        self.turn = "White" if self.turn == "Black" else "Black"

        valid_moves = self.get_valid_moves(self.turn)
        if not valid_moves:
            self.turn = "White" if self.turn == "Black" else "Black"
            valid_moves = self.get_valid_moves(self.turn)
            if not valid_moves:
                self.game_over = True
                self.timer_running = False
                black_score = sum(row.count("Black") for row in self.board)
                white_score = sum(row.count("White") for row in self.board)

                if black_score > white_score:
                    if self.story_frame:
                        self.story_frame.kings_defeated_this_run += 1
                    messagebox.showinfo("King Defeated!", f"🏆 {self.player_name} defeated Othello Overlord ({black_score} to {white_score})!")
                    self.root.destroy()
                elif white_score > black_score:
                    if self.story_frame:
                        self.story_frame.end_run(was_victory=False)
                    messagebox.showinfo("Defeat", f"Othello Overlord defeated you ({white_score} to {black_score})!")
                    self.root.destroy()
                else:
                    if self.story_frame:
                        self.story_frame.end_run(was_victory=False)
                    messagebox.showinfo("Game Over", f"It's a tie ({black_score} to {white_score}). Run ended.")
                    self.root.destroy()
                return
            else:
                messagebox.showinfo(
                    "Turn Passed",
                    f"No valid moves available! Turn passes back to {self.turn}.",
                )

        display_name = self.player_name if self.turn == "Black" else "Othello Overlord"
        color_code = "#3498db" if self.turn == "Black" else "#ecf0f1"
        self.status_label.config(
            text=f"Turn: {display_name} - Place your disc", fg=color_code
        )
        self.update_board_ui()

        if self.turn == "White" and not self.game_over:
            self.root.after(600, self.ai_move)

    def ai_move(self):
        if self.game_over:
            return

        valid_moves = self.get_valid_moves("White")
        if valid_moves:
            r, c = random.choice(valid_moves)
            flips = self.get_flips(r, c, "White")
            self.board[r][c] = "White"
            for fr, fc in flips:
                self.board[fr][fc] = "White"

            self.update_board_ui()
            self.check_game_state()

    def update_board_ui(self):
        black_score = sum(row.count("Black") for row in self.board)
        white_score = sum(row.count("White") for row in self.board)
        self.score_label.config(text=f"{self.player_name} Discs: {black_score} | King Discs: {white_score}")

        valid_moves = self.get_valid_moves(self.turn)

        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                btn = self.buttons[(r, c)]

                if piece == "Black":
                    btn.config(text="BLACK", bg="#2c3e50", fg="white")
                elif piece == "White":
                    btn.config(text="WHITE", bg="#ecf0f1", fg="#2c3e50")
                elif (r, c) in valid_moves and not (self.turn == "White"):
                    btn.config(text="•", bg="#2ecc71", fg="white")
                else:
                    btn.config(text="", bg="#27ae60")

    def update_timer(self):
        if self.timer_running and not self.game_over:
            if self.turn == "Black":
                if self.black_time > 0:
                    self.black_time -= 1
            else:
                if self.white_time > 0:
                    self.white_time -= 1

            b_min, b_sec = divmod(self.black_time, 60)
            w_min, w_sec = divmod(self.white_time, 60)
            self.timer_label.config(
                text=f"{self.player_name}: {b_min:02d}:{b_sec:02d} | King: {w_min:02d}:{w_sec:02d}"
            )

            if self.black_time == 0 or self.white_time == 0:
                self.game_over = True
                self.timer_running = False
                if self.black_time == 0:
                    if self.story_frame:
                        self.story_frame.end_run(was_victory=False)
                    messagebox.showinfo("Time Out!", f"{self.player_name} ran out of time! Othello Overlord wins!")
                else:
                    if self.story_frame:
                        self.story_frame.kings_defeated_this_run += 1
                    messagebox.showinfo("Time Out!", "Othello Overlord ran out of time! You win!")
                self.root.destroy()
                return

        self.root.after(1000, self.update_timer)

def run_mode(parent, player_name="Player", story_frame=None):
    app = ReversiApp(parent, player_name=player_name, story_frame=story_frame)
    return app
