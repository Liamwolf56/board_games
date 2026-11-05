import random
import sys
import tkinter as tk
from tkinter import messagebox

KING_DATA = {
    "name": "Arch-Sentinel Otrio",
    "desc": "Otrio",
    "title": "Arch-Sentinel Otrio",
    "game": "Otrio",
    "intro": "You face the Arch-Sentinel of the concentric rings. Only true spatial mastery will breach my defenses!"
}

class OtrioApp:
    def __init__(self, root, player_name="Player", story_frame=None):
        self.root = root
        self.player_name = player_name
        self.story_frame = story_frame
        self.mode = "PvAI"

        self.root.title(f"Story Mode: {self.player_name} vs Arch-Sentinel Otrio")
        self.root.geometry("680x820")
        self.root.config(bg="#2c3e50")

        self.turn = "Red"  # Red (Player) vs Blue (Arch-Sentinel Otrio)
        self.game_over = False
        self.selected_size = "M"  # Default selected ring size: 'L', 'M', or 'S'

        # Board structure: 3x3 grid, where each cell is a dict {'L': None, 'M': None, 'S': None}
        self.board = [
            [{"L": None, "M": None, "S": None} for _ in range(3)] for _ in range(3)
        ]

        # Inventory per player: 3 Large, 3 Medium, 3 Small
        self.inventory = {
            "Red": {"L": 3, "M": 3, "S": 3},
            "Blue": {"L": 3, "M": 3, "S": 3},
        }

        # Match Timers (300 seconds / 5 mins)
        self.red_time = 300
        self.blue_time = 300
        self.timer_running = True

        # Top Control Bar
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
            text=f"Turn: {self.player_name} (Select ring size & place)",
            font=("Arial", 12, "bold"),
            bg="#2c3e50",
            fg="#e74c3c",
        )
        self.status_label.pack(pady=5)

        # Size Selection Controls
        size_frame = tk.Frame(root, bg="#2c3e50")
        size_frame.pack(pady=5)

        tk.Label(
            size_frame,
            text="Select Ring Size:",
            font=("Arial", 10, "bold"),
            bg="#2c3e50",
            fg="white",
        ).pack(side=tk.LEFT, padx=5)

        self.btn_large = tk.Button(
            size_frame,
            text="⭕ Large",
            font=("Arial", 10, "bold"),
            bg="#bdc3c7",
            fg="#2c3e50",
            command=lambda: self.set_ring_size("L"),
        )
        self.btn_large.pack(side=tk.LEFT, padx=3)

        self.btn_medium = tk.Button(
            size_frame,
            text="🟢 Medium",
            font=("Arial", 10, "bold"),
            bg="#f1c40f",
            fg="#2c3e50",
            command=lambda: self.set_ring_size("M"),
        )
        self.btn_medium.pack(side=tk.LEFT, padx=3)

        self.btn_small = tk.Button(
            size_frame,
            text="⚫ Small",
            font=("Arial", 10, "bold"),
            bg="#bdc3c7",
            fg="#2c3e50",
            command=lambda: self.set_ring_size("S"),
        )
        self.btn_small.pack(side=tk.LEFT, padx=3)

        self.inventory_label = tk.Label(
            root,
            text="",
            font=("Arial", 10, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1",
        )
        self.inventory_label.pack(pady=3)

        # 3x3 Board Grid
        board_frame = tk.Frame(root, bg="#34495e", bd=4, relief="solid")
        board_frame.pack(pady=10)

        self.buttons = {}
        for r in range(3):
            for c in range(3):
                btn = tk.Button(
                    board_frame,
                    text="[   ]",
                    font=("Courier", 16, "bold"),
                    width=8,
                    height=3,
                    bg="#ecf0f1",
                    command=lambda row=r, col=c: self.square_clicked(row, col),
                )
                btn.grid(row=r, column=c, padx=3, pady=3)
                self.buttons[(r, c)] = btn

        self.update_inventory_ui()
        self.update_timer()

    def show_rules(self):
        rules = (
            "OTRIO (STORY MODE):\n\n"
            "1. Select a ring size (Large, Medium, or Small) and click an open space on the 3x3 grid against Arch-Sentinel Otrio.\n"
            "2. Win Conditions:\n"
            "   • 3 rings of the SAME size in a row (Horizontal, Vertical, Diagonal).\n"
            "   • 3 rings in INCR/DECR size order (Small -> Medium -> Large) in a row.\n"
            "   • Concentric Stack: All 3 ring sizes (S, M, L) in a SINGLE square!"
        )
        messagebox.showinfo("How to Play - Otrio", rules)

    def set_ring_size(self, size):
        self.selected_size = size
        self.btn_large.config(bg="#f1c40f" if size == "L" else "#bdc3c7")
        self.btn_medium.config(bg="#f1c40f" if size == "M" else "#bdc3c7")
        self.btn_small.config(bg="#f1c40f" if size == "S" else "#bdc3c7")

    def update_inventory_ui(self):
        red_inv = self.inventory["Red"]
        blue_inv = self.inventory["Blue"]
        txt = (
            f"{self.player_name} Inventory: L={red_inv['L']} M={red_inv['M']} S={red_inv['S']} | "
            f"Arch-Sentinel: L={blue_inv['L']} M={blue_inv['M']} S={blue_inv['S']}"
        )
        self.inventory_label.config(text=txt)

    def square_clicked(self, r, c):
        if self.game_over or self.turn != "Red":
            return

        size = self.selected_size
        player = self.turn

        if self.inventory[player][size] <= 0:
            messagebox.showwarning(
                "No Rings Left", f"You have no remaining {size} rings left!"
            )
            return

        if self.board[r][c][size] is not None:
            messagebox.showwarning(
                "Slot Occupied", f"There is already a {size} ring in this square!"
            )
            return

        self.board[r][c][size] = player
        self.inventory[player][size] -= 1
        self.update_board_ui()
        self.update_inventory_ui()

        if self.check_win(player):
            self.game_over = True
            self.timer_running = False
            if self.story_frame:
                self.story_frame.kings_defeated_this_run += 1
            messagebox.showinfo("King Defeated!", f"🏆 {self.player_name} defeated Arch-Sentinel Otrio!")
            self.root.destroy()
            return

        if all(count == 0 for count in self.inventory[player].values()):
            self.game_over = True
            self.timer_running = False
            if self.story_frame:
                self.story_frame.end_run(was_victory=False)
            messagebox.showinfo("Game Out", "Out of moves! It's a draw.")
            self.root.destroy()
            return

        self.finish_turn()

    def finish_turn(self):
        self.turn = "Blue" if self.turn == "Red" else "Red"
        display_name = self.player_name if self.turn == "Red" else "Arch-Sentinel Otrio"
        color_code = "#e74c3c" if self.turn == "Red" else "#3498db"
        self.status_label.config(text=f"Turn: {display_name}", fg=color_code)

        if self.turn == "Blue" and not self.game_over:
            self.root.after(500, self.ai_move)

    def ai_move(self):
        if self.game_over:
            return

        valid_moves = []
        for size in ["L", "M", "S"]:
            if self.inventory["Blue"][size] > 0:
                for r in range(3):
                    for c in range(3):
                        if self.board[r][c][size] is None:
                            valid_moves.append((r, c, size))

        if valid_moves:
            r, c, size = random.choice(valid_moves)
            self.board[r][c][size] = "Blue"
            self.inventory["Blue"][size] -= 1
            self.update_board_ui()
            self.update_inventory_ui()

            if self.check_win("Blue"):
                self.game_over = True
                self.timer_running = False
                if self.story_frame:
                    self.story_frame.end_run(was_victory=False)
                messagebox.showinfo("Defeat", "Arch-Sentinel Otrio defeated you!")
                self.root.destroy()
                return

            self.finish_turn()

    def check_win(self, p):
        b = self.board

        for r in range(3):
            for c in range(3):
                if (
                    b[r][c]["L"] == p
                    and b[r][c]["M"] == p
                    and b[r][c]["S"] == p
                ):
                    return True

        lines = []
        for i in range(3):
            lines.append([(i, 0), (i, 1), (i, 2)])
            lines.append([(0, i), (1, i), (2, i)])
        lines.append([(0, 0), (1, 1), (2, 2)])
        lines.append([(0, 2), (1, 1), (2, 0)])

        for line in lines:
            for sz in ["L", "M", "S"]:
                if all(b[r][c][sz] == p for r, c in line):
                    return True

            p0, p1, p2 = line
            if (
                b[p0[0]][p0[1]]["S"] == p
                and b[p1[0]][p1[1]]["M"] == p
                and b[p2[0]][p2[1]]["L"] == p
            ):
                return True
            if (
                b[p0[0]][p0[1]]["L"] == p
                and b[p1[0]][p1[1]]["M"] == p
                and b[p2[0]][p2[1]]["S"] == p
            ):
                return True

        return False

    def update_board_ui(self):
        for r in range(3):
            for c in range(3):
                cell = self.board[r][c]
                l_str = "R" if cell["L"] == "Red" else ("B" if cell["L"] == "Blue" else ".")
                m_str = "R" if cell["M"] == "Red" else ("B" if cell["M"] == "Blue" else ".")
                s_str = "R" if cell["S"] == "Red" else ("B" if cell["S"] == "Blue" else ".")

                txt = f"[{l_str}{m_str}{s_str}]"
                self.buttons[(r, c)].config(text=txt)

    def update_timer(self):
        if self.timer_running and not self.game_over:
            if self.turn == "Red":
                if self.red_time > 0:
                    self.red_time -= 1
            else:
                if self.blue_time > 0:
                    self.blue_time -= 1

            r_min, r_sec = divmod(self.red_time, 60)
            b_min, b_sec = divmod(self.blue_time, 60)
            self.timer_label.config(
                text=f"{self.player_name}: {r_min:02d}:{r_sec:02d} | King: {b_min:02d}:{b_sec:02d}"
            )

            if self.red_time == 0 or self.blue_time == 0:
                self.game_over = True
                self.timer_running = False
                if self.red_time == 0:
                    if self.story_frame:
                        self.story_frame.end_run(was_victory=False)
                    messagebox.showinfo("Time Out!", f"{self.player_name} ran out of time! Arch-Sentinel Otrio wins!")
                else:
                    if self.story_frame:
                        self.story_frame.kings_defeated_this_run += 1
                    messagebox.showinfo("Time Out!", "Arch-Sentinel Otrio ran out of time! You win!")
                self.root.destroy()
                return

        self.root.after(1000, self.update_timer)

def run_mode(parent, player_name="Player", story_frame=None):
    app = OtrioApp(parent, player_name=player_name, story_frame=story_frame)
    return app
