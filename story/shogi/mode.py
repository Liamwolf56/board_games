import sys
import tkinter as tk
from tkinter import messagebox

KING_DATA = {
    "name": "Shogun General Shogi",
    "desc": "Shogi (Japanese Chess)"
}

class ShogiApp:
    def __init__(self, root, player_name="Player", story_frame=None):
        self.root = root
        self.player_name = player_name
        self.story_frame = story_frame
        self.mode = "PvAI"

        self.root.title(f"Story Mode: {self.player_name} vs Shogun General Shogi")
        self.root.geometry("750x850")
        self.root.config(bg="#d2b48c")

        self.board = [[None for _ in range(9)] for _ in range(9)]
        self.turn = 1
        self.selected_piece = None

        self.time_p1 = 600
        self.time_p2 = 600
        self.timer_running = True

        # Reliable Monochrome Unicode Symbols for Shogi
        self.symbols = {
            "KING": "♔",
            "ROOK": "♖",
            "BISHOP": "♗",
            "GOLD": "★",
            "SILVER": "◆",
            "KNIGHT": "♘",
            "LANCE": "▲",
            "PAWN": "●",
        }

        self.hands = {1: [], 2: []}
        self.setup_board()

        top_frame = tk.Frame(root, bg="#d2b48c")
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(
            top_frame,
            text="New Game",
            bg="#8b4513",
            fg="white",
            font=("Arial", 9, "bold"),
            command=self.new_game,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            top_frame,
            text="How to Play",
            bg="#34495e",
            fg="white",
            font=("Arial", 9, "bold"),
            command=self.show_instructions,
        ).pack(side=tk.LEFT, padx=5)

        self.timer_label = tk.Label(
            top_frame,
            text=f"{self.player_name}: 10:00 | King: 10:00",
            font=("Arial", 10, "bold"),
            bg="#d2b48c",
            fg="#2c3e50",
        )
        self.timer_label.pack(side=tk.RIGHT, padx=5)

        self.status_label = tk.Label(
            top_frame,
            text=f"{self.player_name}'s Turn",
            font=("Arial", 11, "bold"),
            bg="#d2b48c",
            fg="#2c3e50",
        )
        self.status_label.pack(side=tk.RIGHT, padx=10)

        main_frame = tk.Frame(root, bg="#d2b48c")
        main_frame.pack(pady=5)

        self.p2_hand_frame = tk.Frame(main_frame, bg="#deb887", bd=2, relief="solid")
        self.p2_hand_frame.pack(fill=tk.X, pady=3)
        tk.Label(
            self.p2_hand_frame,
            text="Shogun Hand:",
            bg="#deb887",
            font=("Arial", 9, "bold"),
        ).pack(side=tk.LEFT, padx=5)
        self.p2_hand_container = tk.Frame(self.p2_hand_frame, bg="#deb887")
        self.p2_hand_container.pack(side=tk.LEFT)

        board_frame = tk.Frame(main_frame, bg="#8b4513", bd=4, relief="solid")
        board_frame.pack(pady=3)

        self.squares = {}
        for r in range(9):
            for c in range(9):
                btn = tk.Button(
                    board_frame,
                    text="",
                    font=("Arial", 16, "bold"),
                    width=3,
                    height=1,
                    bg="#f5deb3",
                    fg="#2c3e50",
                    command=lambda row=r, col=c: self.on_square_click(row, col),
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.squares[(r, c)] = btn

        self.p1_hand_frame = tk.Frame(main_frame, bg="#deb887", bd=2, relief="solid")
        self.p1_hand_frame.pack(fill=tk.X, pady=3)
        tk.Label(
            self.p1_hand_frame,
            text=f"{self.player_name} Hand:",
            bg="#deb887",
            font=("Arial", 9, "bold"),
        ).pack(side=tk.LEFT, padx=5)
        self.p1_hand_container = tk.Frame(self.p1_hand_frame, bg="#deb887")
        self.p1_hand_container.pack(side=tk.LEFT)

        self.update_ui()
        self.run_timer()

    def setup_board(self):
        self.board = [[None for _ in range(9)] for _ in range(9)]
        self.hands = {1: [], 2: []}
        self.turn = 1
        self.time_p1 = 600
        self.time_p2 = 600

        p2_back = [
            "LANCE",
            "KNIGHT",
            "SILVER",
            "GOLD",
            "KING",
            "GOLD",
            "SILVER",
            "KNIGHT",
            "LANCE",
        ]
        for c, p in enumerate(p2_back):
            self.board[0][c] = {"type": p, "player": 2}

        self.board[1][1] = {"type": "ROOK", "player": 2}
        self.board[1][7] = {"type": "BISHOP", "player": 2}
        for c in range(9):
            self.board[2][c] = {"type": "PAWN", "player": 2}

        for c in range(9):
            self.board[6][c] = {"type": "PAWN", "player": 1}
        self.board[7][1] = {"type": "BISHOP", "player": 1}
        self.board[7][7] = {"type": "ROOK", "player": 1}

        p1_back = [
            "LANCE",
            "KNIGHT",
            "SILVER",
            "GOLD",
            "KING",
            "GOLD",
            "SILVER",
            "KNIGHT",
            "LANCE",
        ]
        for c, p in enumerate(p1_back):
            self.board[8][c] = {"type": p, "player": 1}

    def new_game(self):
        self.setup_board()
        self.selected_piece = None
        self.update_ui()

    def show_instructions(self):
        messagebox.showinfo(
            "How to Play Shogi",
            f"• Shogi is Japanese chess played on a 9x9 board against Shogun General Shogi.\n• Captured pieces can be 'dropped' back onto the board as your own!\n• Goal: Capture the Shogun's King (♔) to win the campaign battle!",
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
                    messagebox.showinfo("Time Out", f"{self.player_name} ran out of time! Shogun General Shogi wins!")
                else:
                    if self.story_frame:
                        self.story_frame.kings_defeated_this_run += 1
                    messagebox.showinfo("Time Out", f"Shogun General Shogi ran out of time! {self.player_name} wins!")
                self.root.destroy()
                return

            self.root.after(1000, self.run_timer)

    def on_square_click(self, r, c):
        if self.turn != 1:
            return
        piece = self.board[r][c]

        if isinstance(self.selected_piece, tuple) and self.selected_piece[0] == "hand":
            _, player, p_type, idx = self.selected_piece
            if piece is None:
                self.board[r][c] = {"type": p_type, "player": player}
                self.hands[player].pop(idx)
                self.selected_piece = None
                self.turn = 2
                self.update_ui()
                if not self.check_game_over():
                    self.root.after(400, self.ai_move)
            else:
                messagebox.showerror("Invalid Drop", "Cannot drop on an occupied square!")
            return

        if self.selected_piece is None:
            if piece and piece["player"] == 1:
                self.selected_piece = (r, c)
                self.highlight_squares(r, c)
        else:
            sr, sc = self.selected_piece
            if (sr, sc) == (r, c):
                self.selected_piece = None
                self.update_ui()
                return

            target = self.board[r][c]
            if target is None or target["player"] != 1:
                if target is not None:
                    self.hands[1].append(target["type"])

                self.board[r][c] = self.board[sr][sc]
                self.board[sr][sc] = None
                self.selected_piece = None
                self.turn = 2
                self.update_ui()

                if not self.check_game_over():
                    self.root.after(400, self.ai_move)
            else:
                self.selected_piece = (r, c)
                self.highlight_squares(r, c)

    def select_hand_piece(self, player, p_type, idx):
        if self.turn != player or player != 1:
            return
        self.selected_piece = ("hand", player, p_type, idx)
        messagebox.showinfo(
            "Shogi Drop", f"Selected {p_type} from hand. Click an empty square to drop!"
        )

    def highlight_squares(self, r, c):
        self.update_ui()
        self.squares[(r, c)].config(bg="#7b68ee")
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < 9 and 0 <= nc < 9:
                    self.squares[(nr, nc)].config(bg="#85bb65")

    def ai_move(self):
        if self.check_game_over():
            return
        import random

        moves = []
        for r in range(9):
            for c in range(9):
                p = self.board[r][c]
                if p and p["player"] == 2:
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < 9 and 0 <= nc < 9:
                                target = self.board[nr][nc]
                                if target is None or target["player"] != 2:
                                    moves.append(((r, c), (nr, nc)))

        if moves:
            (sr, sc), (tr, tc) = random.choice(moves)
            target = self.board[tr][tc]
            if target:
                self.hands[2].append(target["type"])
            self.board[tr][tc] = self.board[sr][sc]
            self.board[sr][sc] = None

        self.turn = 1
        self.update_ui()
        self.check_game_over()

    def check_game_over(self):
        p1_king, p2_king = False, False
        for r in range(9):
            for c in range(9):
                p = self.board[r][c]
                if p and p["type"] == "KING":
                    if p["player"] == 1:
                        p1_king = True
                    elif p["player"] == 2:
                        p2_king = True

        if not p1_king:
            self.timer_running = False
            if self.story_frame:
                self.story_frame.end_run(was_victory=False)
            messagebox.showinfo("Defeat", "Shogun General Shogi has overthrown your King!")
            self.root.destroy()
            return True
        if not p2_king:
            self.timer_running = False
            if self.story_frame:
                self.story_frame.kings_defeated_this_run += 1
            messagebox.showinfo("King Defeated!", f"🏆 {self.player_name} has overthrown Shogun General Shogi!")
            self.root.destroy()
            return True
        return False

    def update_ui(self):
        for r in range(9):
            for c in range(9):
                btn = self.squares[(r, c)]
                btn.config(bg="#f5deb3")
                p = self.board[r][c]
                if p:
                    sym = self.symbols[p["type"]]
                    fg_col = "#000000" if p["player"] == 1 else "#a00000"
                    btn.config(text=sym, fg=fg_col)
                else:
                    btn.config(text="")

        for widget in self.p1_hand_container.winfo_children():
            widget.destroy()
        for idx, p_type in enumerate(self.hands[1]):
            b = tk.Button(
                self.p1_hand_container,
                text=self.symbols[p_type],
                font=("Arial", 9, "bold"),
                width=3,
                bg="#deb887",
                command=lambda pt=p_type, i=idx: self.select_hand_piece(1, pt, i),
            )
            b.pack(side=tk.LEFT, padx=2)

        for widget in self.p2_hand_container.winfo_children():
            widget.destroy()
        for idx, p_type in enumerate(self.hands[2]):
            b = tk.Button(
                self.p2_hand_container,
                text=self.symbols[p_type],
                font=("Arial", 9, "bold"),
                width=3,
                bg="#deb887",
                state=tk.DISABLED,
            )
            b.pack(side=tk.LEFT, padx=2)

        turn_str = f"{self.player_name}'s Turn" if self.turn == 1 else "Shogun General Shogi's Turn"
        self.status_label.config(text=turn_str)

def run_mode(parent, player_name="Player", story_frame=None):
    app = ShogiApp(parent, player_name=player_name, story_frame=story_frame)
    return app
