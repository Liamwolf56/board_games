import random
import sys
import tkinter as tk
from tkinter import messagebox

KING_DATA = {
    "name": "Grandmaster Wild Card",
    "desc": "Sequence for Kids"
}

class SequenceForKidsApp:
    def __init__(self, root, player_name="Player", story_frame=None):
        self.root = root
        self.player_name = player_name
        self.story_frame = story_frame
        self.mode = "PvAI"

        self.root.title(f"Story Mode: {self.player_name} vs Grandmaster Wild Card")
        self.root.geometry("750x750")
        self.root.config(bg="#2c3e50")

        self.turn = "Player 1"  # Player 1 (Blue) vs Player 2 (Grandmaster Wild Card)
        self.game_over = False

        # Animal deck/cards
        self.animals = ["Lion", "Elephant", "Monkey", "Giraffe", "Zebra", "Tiger"]

        # 5x5 Board grid with animals
        self.board_animals = [
            ["Lion", "Elephant", "Monkey", "Giraffe", "Zebra"],
            ["Zebra", "Tiger", "Lion", "Elephant", "Monkey"],
            ["Monkey", "Giraffe", "Tiger", "Zebra", "Lion"],
            ["Elephant", "Monkey", "Zebra", "Lion", "Giraffe"],
            ["Giraffe", "Zebra", "Elephant", "Monkey", "Tiger"],
        ]

        # Board chips: empty="", "Player 1", or "Player 2"
        self.board_chips = [["" for _ in range(5)] for _ in range(5)]

        # Hands (3 cards each)
        self.p1_hand = [random.choice(self.animals) for _ in range(3)]
        self.p2_hand = [random.choice(self.animals) for _ in range(3)]
        self.selected_card_idx = None

        # Timers (300 seconds / 5 mins)
        self.p1_time = 300
        self.p2_time = 300
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
            text=f"Turn: {self.player_name} (Select a card from your hand, then click matching animal)",
            font=("Arial", 11, "bold"),
            bg="#2c3e50",
            fg="#3498db",
        )
        self.status_label.pack(pady=5)

        # Board Grid Container
        board_frame = tk.Frame(root, bg="#34495e", bd=4, relief="solid")
        board_frame.pack(pady=10)

        self.board_buttons = {}
        for r in range(5):
            for c in range(5):
                animal_name = self.board_animals[r][c]
                btn = tk.Button(
                    board_frame,
                    text=f"{animal_name}\n[    ]",
                    font=("Arial", 9, "bold"),
                    width=10,
                    height=4,
                    bg="#ecf0f1",
                    command=lambda row=r, col=c: self.board_clicked(row, col),
                )
                btn.grid(row=r, column=c, padx=3, pady=3)
                self.board_buttons[(r, c)] = btn

        # Hand Container Frame
        hand_frame = tk.Frame(root, bg="#1e272e", bd=3, relief="solid")
        hand_frame.pack(pady=10, padx=10, fill=tk.X)

        self.hand_title_label = tk.Label(
            hand_frame,
            text=f"{self.player_name}'s Hand (Click to select card):",
            font=("Arial", 10, "bold"),
            bg="#1e272e",
            fg="#3498db",
        )
        self.hand_title_label.pack(pady=3)

        self.card_buttons_frame = tk.Frame(hand_frame, bg="#1e272e")
        self.card_buttons_frame.pack(pady=5)

        self.card_buttons = []
        for i in range(3):
            c_btn = tk.Button(
                self.card_buttons_frame,
                text="",
                font=("Arial", 11, "bold"),
                width=12,
                height=2,
                bg="#bdc3c7",
                command=lambda idx=i: self.select_card(idx),
            )
            c_btn.pack(side=tk.LEFT, padx=5)
            self.card_buttons.append(c_btn)

        self.update_hand_ui()
        self.update_board_ui()
        self.update_timer()

    def show_rules(self):
        rules = (
            "SEQUENCE FOR KIDS (STORY MODE):\n\n"
            "1. Click a card in your hand to select it.\n"
            "2. Click an empty square on the board containing that animal to place your chip.\n"
            "3. First player to connect 4 chips in a row (horizontal, vertical, or diagonal) defeats Grandmaster Wild Card!"
        )
        messagebox.showinfo("How to Play - Sequence for Kids", rules)

    def select_card(self, idx):
        if self.game_over or self.turn != "Player 1":
            return
        self.selected_card_idx = idx
        hand = self.p1_hand
        selected_card = hand[idx]
        self.status_label.config(
            text=(
                f"Turn: {self.player_name} | Selected Card: [{selected_card}] -> Now click matching animal on board"
            ),
            fg="#f1c40f",
        )

        for i, btn in enumerate(self.card_buttons):
            btn.config(bg="#f1c40f" if i == idx else "#bdc3c7")

    def board_clicked(self, r, c):
        if self.game_over or self.turn != "Player 1":
            return

        if self.selected_card_idx is None:
            messagebox.showwarning(
                "Select Card First", "Please select a card from your hand first!"
            )
            return

        hand = self.p1_hand
        card_animal = hand[self.selected_card_idx]
        board_animal = self.board_animals[r][c]

        if board_animal != card_animal:
            messagebox.showwarning(
                "Mismatch",
                f"This square is a {board_animal}, but your card is {card_animal}!",
            )
            return

        if self.board_chips[r][c] != "":
            messagebox.showwarning("Occupied", "This square already has a chip on it!")
            return

        self.board_chips[r][c] = "Player 1"
        hand[self.selected_card_idx] = random.choice(self.animals)
        self.selected_card_idx = None

        self.update_board_ui()
        self.update_hand_ui()

        if self.check_win("Player 1"):
            self.game_over = True
            self.timer_running = False
            if self.story_frame:
                self.story_frame.kings_defeated_this_run += 1
            messagebox.showinfo("King Defeated!", f"🏆 {self.player_name} defeated Grandmaster Wild Card!")
            self.root.destroy()
            return

        self.finish_turn()

    def finish_turn(self):
        self.turn = "Player 2" if self.turn == "Player 1" else "Player 1"
        color_code = "#3498db" if self.turn == "Player 1" else "#e74c3c"
        title_text = (
            f"{self.player_name}'s Hand (Click to select card):"
            if self.turn == "Player 1"
            else "Grandmaster Wild Card's Hand:"
        )
        self.hand_title_label.config(text=title_text)
        display_name = self.player_name if self.turn == "Player 1" else "Grandmaster Wild Card"
        self.status_label.config(
            text=f"Turn: {display_name}", fg=color_code
        )
        self.update_hand_ui()

        if self.mode == "PvAI" and self.turn == "Player 2" and not self.game_over:
            self.root.after(600, self.ai_move)

    def ai_move(self):
        if self.game_over:
            return

        valid_move = None
        for idx, card in enumerate(self.p2_hand):
            for r in range(5):
                for c in range(5):
                    if self.board_animals[r][c] == card and self.board_chips[r][c] == "":
                        valid_move = (idx, r, c)
                        break
                if valid_move:
                    break
            if valid_move:
                break

        if valid_move:
            idx, r, c = valid_move
            self.board_chips[r][c] = "Player 2"
            self.p2_hand[idx] = random.choice(self.animals)
            self.update_board_ui()
            self.update_hand_ui()

            if self.check_win("Player 2"):
                self.game_over = True
                self.timer_running = False
                if self.story_frame:
                    self.story_frame.end_run(was_victory=False)
                messagebox.showinfo("Defeat", "Grandmaster Wild Card defeated you!")
                self.root.destroy()
                return

        self.finish_turn()

    def check_win(self, p):
        b = self.board_chips
        lines = []
        for i in range(5):
            lines.append([(i, 0), (i, 1), (i, 2), (i, 3)])
            lines.append([(i, 1), (i, 2), (i, 3), (i, 4)])
            lines.append([(0, i), (1, i), (2, i), (3, i)])
            lines.append([(1, i), (2, i), (3, i), (4, i)])
        lines.append([(0, 0), (1, 1), (2, 2), (3, 3)])
        lines.append([(1, 1), (2, 2), (3, 3), (4, 4)])
        lines.append([(0, 1), (1, 2), (2, 3), (3, 4)])
        lines.append([(1, 0), (2, 1), (3, 2), (4, 3)])

        lines.append([(0, 4), (1, 3), (2, 2), (3, 1)])
        lines.append([(1, 4), (2, 3), (3, 2), (4, 1)])
        lines.append([(0, 3), (1, 2), (2, 1), (3, 0)])
        lines.append([(1, 3), (2, 2), (3, 1), (4, 0)])

        for line in lines:
            if all(b[r][c] == p for r, c in line):
                return True
        return False

    def update_board_ui(self):
        for r in range(5):
            for c in range(5):
                animal = self.board_animals[r][c]
                chip = self.board_chips[r][c]
                btn = self.board_buttons[(r, c)]

                if chip == "Player 1":
                    btn.config(text=f"{animal}\n🔵 P1", bg="#3498db", fg="white")
                elif chip == "Player 2":
                    btn.config(text=f"{animal}\n🔴 King", bg="#e74c3c", fg="white")
                else:
                    btn.config(text=f"{animal}\n[    ]", bg="#ecf0f1", fg="#2c3e50")

    def update_hand_ui(self):
        hand = self.p1_hand if self.turn == "Player 1" else self.p2_hand
        for i, card_name in enumerate(hand):
            self.card_buttons[i].config(text=card_name if self.turn == "Player 1" else "Hidden")

    def update_timer(self):
        if self.timer_running and not self.game_over:
            if self.turn == "Player 1":
                if self.p1_time > 0:
                    self.p1_time -= 1
            else:
                if self.p2_time > 0:
                    self.p2_time -= 1

            p1_min, p1_sec = divmod(self.p1_time, 60)
            p2_min, p2_sec = divmod(self.p2_time, 60)
            self.timer_label.config(
                text=f"{self.player_name}: {p1_min:02d}:{p1_sec:02d} | King: {p2_min:02d}:{p2_sec:02d}"
            )

            if self.p1_time == 0 or self.p2_time == 0:
                self.game_over = True
                self.timer_running = False
                if self.p1_time == 0:
                    if self.story_frame:
                        self.story_frame.end_run(was_victory=False)
                    messagebox.showinfo("Time Out!", f"{self.player_name} ran out of time! Grandmaster Wild Card wins!")
                else:
                    if self.story_frame:
                        self.story_frame.kings_defeated_this_run += 1
                    messagebox.showinfo("Time Out!", "Grandmaster Wild Card ran out of time! You win!")
                self.root.destroy()
                return

        self.root.after(1000, self.update_timer)

def run_mode(parent, player_name="Player", story_frame=None):
    app = SequenceForKidsApp(parent, player_name=player_name, story_frame=story_frame)
    return app
