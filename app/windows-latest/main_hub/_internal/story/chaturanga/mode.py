import sys
import tkinter as tk
from tkinter import messagebox

KING_DATA = {
    "name": "Raja Four-Fold War",
    "desc": "Chaturanga"
}

class ChaturangaApp:
    def __init__(self, root, player_name="Player", story_frame=None):
        self.root = root
        self.player_name = player_name
        self.story_frame = story_frame
        self.mode = "PvAI"

        self.root.title(f"Story Mode: {self.player_name} vs Raja Four-Fold War")
        self.root.geometry("640x740")
        self.root.config(bg="#34495e")

        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.turn = 1
        self.selected_square = None

        self.time_p1 = 600
        self.time_p2 = 600
        self.timer_running = True

        self.symbols = {
            1: {
                "KING": "♔",
                "COUNSELOR": "♕",
                "ELEPHANT": "♗",
                "HORSE": "♘",
                "CHARIOT": "♖",
                "PAWN": "♙",
            },
            2: {
                "KING": "♚",
                "COUNSELOR": "♛",
                "ELEPHANT": "♝",
                "HORSE": "♞",
                "CHARIOT": "♜",
                "PAWN": "♟",
            },
        }

        top_frame = tk.Frame(root, bg="#34495e")
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(
            top_frame,
            text="New Game",
            bg="#e67e22",
            fg="white",
            font=("Arial", 9, "bold"),
            command=self.new_game,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            top_frame,
            text="How to Play",
            bg="#2980b9",
            fg="white",
            font=("Arial", 9, "bold"),
            command=self.show_instructions,
        ).pack(side=tk.LEFT, padx=5)

        self.timer_label = tk.Label(
            top_frame,
            text=f"{self.player_name}: 10:00 | King: 10:00",
            font=("Arial", 10, "bold"),
            bg="#34495e",
            fg="#00d8d6",
        )
        self.timer_label.pack(side=tk.RIGHT, padx=5)

        self.status_label = tk.Label(
            top_frame,
            text=f"{self.player_name}'s Turn",
            font=("Arial", 11, "bold"),
            bg="#34495e",
            fg="#00d8d6",
        )
        self.status_label.pack(side=tk.RIGHT, padx=10)

        board_frame = tk.Frame(root, bg="#2c3e50", bd=4, relief="solid")
        board_frame.pack(pady=10)

        self.squares = {}
        for r in range(8):
            for c in range(8):
                bg_col = "#ecf0f1" if (r + c) % 2 == 0 else "#bdc3c7"
                btn = tk.Button(
                    board_frame,
                    text="",
                    font=("Arial", 22, "bold"),
                    width=2,
                    height=1,
                    bg=bg_col,
                    command=lambda row=r, col=c: self.on_square_click(row, col),
                )
                btn.grid(row=r, column=c)
                self.squares[(r, c)] = btn

        self.setup_board()
        self.update_ui()
        self.run_timer()

    def setup_board(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.turn = 1
        self.time_p1 = 600
        self.time_p2 = 600

        back = [
            "CHARIOT",
            "HORSE",
            "ELEPHANT",
            "COUNSELOR",
            "KING",
            "ELEPHANT",
            "HORSE",
            "CHARIOT",
        ]
        for c, p in enumerate(back):
            self.board[0][c] = {"type": p, "player": 2}
        for c in range(8):
            self.board[1][c] = {"type": "PAWN", "player": 2}

        for c in range(8):
            self.board[6][c] = {"type": "PAWN", "player": 1}
        for c, p in enumerate(back):
            self.board[7][c] = {"type": p, "player": 1}

    def new_game(self):
        self.setup_board()
        self.selected_square = None
        self.update_ui()

    def show_instructions(self):
        messagebox.showinfo(
            "How to Play Chaturanga",
            f"• Chaturanga is the 6th-century Indian ancestor of chess.\n• Goal: Capture Raja Four-Fold War's King (♚) to win the campaign battle!",
        )

    def run_timer(self):
        if self.timer_running:
            if self.turn == 1:
                self.time_p1 = max(0, self.time_p1 - 1)
            else:
                self.time_p2 = max(0, self.time_p2 - 1)

            m1, s1 = divmod(self.time_p1, 60)
            m2, s2 = divmod(self.time_p2, 60)
            self.timer_label.config(
                text=f"{self.player_name}: {m1:02d}:{s1:02d} | King: {m2:02d}:{s2:02d}"
            )

            if self.time_p1 == 0 or self.time_p2 == 0:
                if self.time_p1 == 0:
                    if self.story_frame:
                        self.story_frame.end_run(was_victory=False)
                    messagebox.showinfo("Time Out", f"{self.player_name} ran out of time! Raja Four-Fold War wins!")
                else:
                    if self.story_frame:
                        self.story_frame.kings_defeated_this_run += 1
                    messagebox.showinfo("Time Out", f"Raja Four-Fold War ran out of time! {self.player_name} wins!")
                self.root.destroy()
                return

            self.root.after(1000, self.run_timer)

    def on_square_click(self, r, c):
        if self.turn != 1:
            return
        piece = self.board[r][c]

        if self.selected_square is None:
            if piece and piece["player"] == 1:
                self.selected_square = (r, c)
                self.highlight_squares(r, c)
        else:
            sr, sc = self.selected_square
            if (sr, sc) == (r, c):
                self.selected_square = None
                self.update_ui()
                return

            target = self.board[r][c]
            if target is None or target["player"] != 1:
                self.board[r][c] = self.board[sr][sc]
                self.board[sr][sc] = None
                self.selected_square = None
                self.turn = 2
                self.update_ui()

                if not self.check_game_over():
                    self.root.after(400, self.ai_move)
            else:
                self.selected_square = (r, c)
                self.highlight_squares(r, c)

    def highlight_squares(self, r, c):
        self.update_ui()
        self.squares[(r, c)].config(bg="#f1c40f")
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                bg_col = "#e67e22" if (nr + nc) % 2 == 0 else "#d35400"
                self.squares[(nr, nc)].config(bg=bg_col)

    def ai_move(self):
        if self.check_game_over():
            return
        import random

        moves = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p["player"] == 2:
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < 8 and 0 <= nc < 8:
                            t = self.board[nr][nc]
                            if t is None or t["player"] != 2:
                                moves.append(((r, c), (nr, nc)))

        if moves:
            (sr, sc), (tr, tc) = random.choice(moves)
            self.board[tr][tc] = self.board[sr][sc]
            self.board[sr][sc] = None

        self.turn = 1
        self.update_ui()
        self.check_game_over()

    def check_game_over(self):
        p1_k, p2_k = False, False
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p["type"] == "KING":
                    if p["player"] == 1:
                        p1_k = True
                    elif p["player"] == 2:
                        p2_k = True

        if not p1_k:
            self.timer_running = False
            if self.story_frame:
                self.story_frame.end_run(was_victory=False)
            messagebox.showinfo("Defeat", "Raja Four-Fold War has overthrown your King!")
            self.root.destroy()
            return True
        if not p2_k:
            self.timer_running = False
            if self.story_frame:
                self.story_frame.kings_defeated_this_run += 1
            messagebox.showinfo("King Defeated!", f"🏆 {self.player_name} has overthrown Raja Four-Fold War!")
            self.root.destroy()
            return True
        return False

    def update_ui(self):
        for r in range(8):
            for c in range(8):
                bg_col = "#ecf0f1" if (r + c) % 2 == 0 else "#bdc3c7"
                btn = self.squares[(r, c)]
                btn.config(bg=bg_col)
                p = self.board[r][c]
                if p:
                    sym = self.symbols[p["player"]][p["type"]]
                    fg_col = "#2c3e50" if p["player"] == 1 else "#000000"
                    btn.config(text=sym, fg=fg_col)
                else:
                    btn.config(text="")

        turn_str = f"{self.player_name}'s Turn" if self.turn == 1 else "Raja Four-Fold War's Turn"
        self.status_label.config(text=turn_str)

def run_mode(parent, player_name="Player", story_frame=None):
    app = ChaturangaApp(parent, player_name=player_name, story_frame=story_frame)
    return app
