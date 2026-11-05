import random
import sys
import tkinter as tk
from tkinter import messagebox

KING_DATA = {
    "name": "Speed King Monza",
    "desc": "Monza Racing"
}

class MonzaApp:
    def __init__(self, root, player_name="Player", story_frame=None):
        self.root = root
        self.player_name = player_name
        self.story_frame = story_frame
        self.mode = "PvAI"

        self.root.title(f"Story Mode: {self.player_name} vs Speed King Monza")
        self.root.geometry("880x720")
        self.root.config(bg="#1e272e")

        self.turn = "Car 1"  # Car 1 (Player) vs Car 2 (Speed King Monza)
        self.game_over = False

        # Track sequence (Tiles 1 to 12)
        self.track_colors = [
            "#e74c3c",
            "#3498db",
            "#2ecc71",
            "#f1c40f",
            "#9b59b6",
            "#ecf0f1",
            "#e74c3c",
            "#2ecc71",
            "#f1c40f",
            "#3498db",
            "#9b59b6",
            "#ecf0f1",
        ]
        self.track_color_names = [
            "RED",
            "BLUE",
            "GREEN",
            "YELLOW",
            "PURPLE",
            "WHITE",
            "RED",
            "GREEN",
            "YELLOW",
            "BLUE",
            "PURPLE",
            "WHITE",
        ]

        # Car positions (0 = Off track / Start line; Tile 1 is index 0)
        self.car1_pos = 0
        self.car2_pos = 0

        # Dice roll state (6 dice)
        self.dice_colors = ["RED", "BLUE", "GREEN", "YELLOW", "WHITE", "PURPLE"]
        self.current_dice = []
        self.used_dice_indices = set()
        self.die_rolled = False

        # Match Timers (300 seconds / 5 mins)
        self.p1_time = 300
        self.p2_time = 300
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

        self.status_label = tk.Label(
            root,
            text=f"Turn: {self.player_name} - Click 'Roll 6 Dice' to start!",
            font=("Arial", 11, "bold"),
            bg="#1e272e",
            fg="#e74c3c",
        )
        self.status_label.pack(pady=5)

        # Track Visualiser Frame
        track_container = tk.Frame(root, bg="#2c3e50", bd=3, relief="solid")
        track_container.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(
            track_container,
            text="MONZA GRAND PRIX RACETRACK",
            font=("Arial", 11, "bold"),
            bg="#2c3e50",
            fg="#f1c40f",
        ).pack(pady=5)

        self.track_frame = tk.Frame(track_container, bg="#2c3e50")
        self.track_frame.pack(pady=5)

        self.track_cells = []
        self.create_track_ui()

        # Dice Controls Container
        dice_container = tk.Frame(root, bg="#1e272e")
        dice_container.pack(pady=15)

        self.roll_btn = tk.Button(
            dice_container,
            text="Roll 6 Dice",
            font=("Arial", 11, "bold"),
            bg="#2ecc71",
            fg="white",
            command=self.roll_dice,
        )
        self.roll_btn.pack(side=tk.LEFT, padx=10)

        self.dice_buttons_frame = tk.Frame(dice_container, bg="#1e272e")
        self.dice_buttons_frame.pack(side=tk.LEFT, padx=10)

        self.end_turn_btn = tk.Button(
            dice_container,
            text="End Turn",
            font=("Arial", 10, "bold"),
            bg="#e67e22",
            fg="white",
            state=tk.DISABLED,
            command=self.finish_turn,
        )
        self.end_turn_btn.pack(side=tk.LEFT, padx=10)

        self.update_track_ui()
        self.update_timer()

    def show_rules(self):
        rules = (
            "MONZA RACING (STORY MODE):\n\n"
            "1. Both cars start behind Tile 1.\n"
            "2. Click 'Roll 6 Dice' to throw all 6 color dice.\n"
            "3. Click a die that matches the EXACT color of the next tile you need to land on!\n"
            "   • To move onto Tile 1, click RED.\n"
            "   • To move onto Tile 2, click BLUE, and so on.\n"
            "4. Chain multiple matching dice in one turn to zip down the track against Speed King Monza!\n"
            "5. First car to reach Tile 12 wins the campaign battle!"
        )
        messagebox.showinfo("How to Play - Monza", rules)

    def create_track_ui(self):
        for idx in range(12):
            hex_bg = self.track_colors[idx]
            fg_txt = "#2c3e50" if hex_bg == "#ecf0f1" else "#ffffff"

            lbl = tk.Label(
                self.track_frame,
                text=f"Tile {idx+1}\n\n",
                font=("Arial", 9, "bold"),
                width=7,
                height=4,
                bg=hex_bg,
                fg=fg_txt,
                relief="solid",
                bd=2,
            )
            lbl.grid(row=0, column=idx, padx=1)
            self.track_cells.append(lbl)

    def roll_dice(self):
        if self.game_over or self.die_rolled:
            return

        self.current_dice = [
            random.choice(self.dice_colors) for _ in range(6)
        ]
        self.used_dice_indices = set()
        self.die_rolled = True
        self.roll_btn.config(state=tk.DISABLED)
        self.end_turn_btn.config(state=tk.NORMAL)

        pos = self.car1_pos if self.turn == "Car 1" else self.car2_pos
        display_name = self.player_name if self.turn == "Car 1" else "Speed King Monza"
        next_tile_color = self.track_color_names[pos] if pos < 12 else "FINISH"

        self.update_dice_ui()
        self.status_label.config(
            text=f"Turn: {display_name} - Next Tile Needed: [{next_tile_color}]",
            fg="#f1c40f",
        )

    def use_die(self, idx):
        if self.game_over or not self.die_rolled or idx in self.used_dice_indices:
            return

        die_color = self.current_dice[idx]
        current_pos = self.car1_pos if self.turn == "Car 1" else self.car2_pos

        if current_pos >= 12:
            return

        required_color = self.track_color_names[current_pos]

        if die_color == required_color:
            self.used_dice_indices.add(idx)
            if self.turn == "Car 1":
                self.car1_pos += 1
            else:
                self.car2_pos += 1

            self.update_track_ui()
            self.update_dice_ui()

            pos = self.car1_pos if self.turn == "Car 1" else self.car2_pos
            if pos >= 12:
                self.game_over = True
                self.timer_running = False
                if self.turn == "Car 1":
                    if self.story_frame:
                        self.story_frame.kings_defeated_this_run += 1
                    messagebox.showinfo(
                        "King Defeated!", f"🏆 {self.player_name} crossed the finish line and defeated Speed King Monza!"
                    )
                else:
                    if self.story_frame:
                        self.story_frame.end_run(was_victory=False)
                    messagebox.showinfo("Defeat", "Speed King Monza crossed the finish line first!")
                self.root.destroy()
                return
            else:
                next_needed = self.track_color_names[pos]
                display_name = self.player_name if self.turn == "Car 1" else "Speed King Monza"
                self.status_label.config(
                    text=f"Turn: {display_name} - Next Tile Needed: [{next_needed}]",
                    fg="#f1c40f",
                )
        else:
            if self.turn == "Car 1":
                messagebox.showwarning(
                    "Mismatch",
                    f"You clicked {die_color}, but the next tile needs {required_color}!",
                )

    def finish_turn(self):
        self.die_rolled = False
        self.current_dice = []
        self.used_dice_indices = set()
        self.roll_btn.config(state=tk.NORMAL)
        self.end_turn_btn.config(state=tk.DISABLED)

        for widget in self.dice_buttons_frame.winfo_children():
            widget.destroy()

        self.turn = "Car 2" if self.turn == "Car 1" else "Car 1"
        display_name = self.player_name if self.turn == "Car 1" else "Speed King Monza"
        color_code = "#e74c3c" if self.turn == "Car 1" else "#3498db"
        self.status_label.config(
            text=f"Turn: {display_name} - Click 'Roll 6 Dice' to start!",
            fg=color_code,
        )

        if self.turn == "Car 2" and not self.game_over:
            self.root.after(600, self.ai_turn)

    def ai_turn(self):
        if self.game_over:
            return

        self.roll_dice()

        moved = True
        while moved and not self.game_over:
            moved = False
            if self.car2_pos < 12:
                req_color = self.track_color_names[self.car2_pos]
                for idx, d_color in enumerate(self.current_dice):
                    if idx not in self.used_dice_indices and d_color == req_color:
                        self.use_die(idx)
                        moved = True
                        break

        if not self.game_over:
            self.root.after(800, self.finish_turn)

    def update_dice_ui(self):
        for widget in self.dice_buttons_frame.winfo_children():
            widget.destroy()

        color_map = {
            "RED": "#e74c3c",
            "BLUE": "#3498db",
            "GREEN": "#2ecc71",
            "YELLOW": "#f1c40f",
            "PURPLE": "#9b59b6",
            "WHITE": "#ecf0f1",
        }

        for idx, c_name in enumerate(self.current_dice):
            hex_bg = color_map.get(c_name, "#bdc3c7")
            fg_txt = "#2c3e50" if c_name == "WHITE" else "#ffffff"

            btn = tk.Button(
                self.dice_buttons_frame,
                text=c_name,
                font=("Arial", 9, "bold"),
                bg=hex_bg,
                fg=fg_txt,
                width=6,
                command=lambda i=idx: self.use_die(i),
            )
            if idx in self.used_dice_indices:
                btn.config(state=tk.DISABLED, bg="#7f8c8d", text="USED")
            btn.pack(side=tk.LEFT, padx=2)

    def update_track_ui(self):
        for idx in range(12):
            hex_bg = self.track_colors[idx]
            fg_txt = "#2c3e50" if hex_bg == "#ecf0f1" else "#ffffff"

            cars_text = ""
            if self.car1_pos - 1 == idx:
                cars_text += "[P1] "
            if self.car2_pos - 1 == idx:
                cars_text += "[King]"

            cell_str = f"Tile {idx+1}\n{self.track_color_names[idx]}\n{cars_text}"
            self.track_cells[idx].config(text=cell_str, bg=hex_bg, fg=fg_txt)

    def update_timer(self):
        if self.timer_running and not self.game_over:
            if self.turn == "Car 1":
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
                    messagebox.showinfo("Time Out!", f"{self.player_name} ran out of time! Speed King Monza wins!")
                else:
                    if self.story_frame:
                        self.story_frame.kings_defeated_this_run += 1
                    messagebox.showinfo("Time Out!", "Speed King Monza ran out of time! You win!")
                self.root.destroy()
                return

        self.root.after(1000, self.update_timer)

def run_mode(parent, player_name="Player", story_frame=None):
    app = MonzaApp(parent, player_name=player_name, story_frame=story_frame)
    return app
