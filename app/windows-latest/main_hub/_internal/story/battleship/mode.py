import random
import sys
import tkinter as tk
from tkinter import messagebox

KING_DATA = {
    "name": "Admiral Deep-Water Fleet",
    "desc": "Battleship"
}

class BattleshipApp:
    def __init__(self, root, player_name="Player", story_frame=None):
        self.root = root
        self.player_name = player_name
        self.story_frame = story_frame
        self.mode = "PvAI"
        
        self.root.title(f"Story Mode: {self.player_name} vs Admiral Deep-Water Fleet")
        self.root.geometry("860x780")
        self.root.config(bg="#1e272e")

        self.phase = "PLACEMENT"  # 'PLACEMENT' or 'BATTLE'
        self.active_placing_player = "Player 1"
        self.turn = "Player 1"
        self.game_over = False

        # Ships to place: (Name, Length)
        self.ships_to_place = [
            ("Carrier", 4),
            ("Battleship", 3),
            ("Cruiser", 2),
            ("Submarine", 2),
        ]
        self.current_ship_idx = 0
        self.placement_orientation = "H"  # 'H' or 'V'

        # Timers (300 seconds / 5 mins per player)
        self.p1_time = 300
        self.p2_time = 300
        self.timer_running = True

        # Grids: empty=".", ship="S", hit="H", miss="M"
        self.p1_ships = [["." for _ in range(8)] for _ in range(8)]
        self.p1_shots = [["." for _ in range(8)] for _ in range(8)]

        self.p2_ships = [["." for _ in range(8)] for _ in range(8)]
        self.p2_shots = [["." for _ in range(8)] for _ in range(8)]

        # Generate AI fleet immediately
        self.place_random_fleet(self.p2_ships)

        top_frame = tk.Frame(root, bg="#1e272e")
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
            bg="#1e272e",
            fg="white",
        )
        self.timer_label.pack(side=tk.RIGHT)

        self.status_label = tk.Label(
            root,
            text="",
            font=("Arial", 12, "bold"),
            bg="#1e272e",
            fg="#00d8d6",
        )
        self.status_label.pack(pady=5)

        # Control Frame for Placement
        self.control_frame = tk.Frame(root, bg="#1e272e")
        self.control_frame.pack(pady=5)

        self.rotate_btn = tk.Button(
            self.control_frame,
            text="🔄 Orientation: Horizontal",
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.toggle_orientation,
        )
        self.rotate_btn.pack(side=tk.LEFT, padx=5)

        self.start_battle_btn = tk.Button(
            self.control_frame,
            text="🚀 Ready for Battle!",
            bg="#2ecc71",
            fg="white",
            font=("Arial", 10, "bold"),
            state=tk.DISABLED,
            command=self.finish_placement,
        )
        self.start_battle_btn.pack(side=tk.LEFT, padx=5)

        # Main Boards Container
        boards_frame = tk.Frame(root, bg="#1e272e")
        boards_frame.pack(pady=10)

        # Left: Target Grid
        left_container = tk.Frame(boards_frame, bg="#1e272e")
        left_container.pack(side=tk.LEFT, padx=15)
        self.target_title = tk.Label(
            left_container,
            text="🎯 Target Grid (Enemy Waters)",
            font=("Arial", 11, "bold"),
            bg="#1e272e",
            fg="#ffdd59",
        )
        self.target_title.pack()

        self.target_frame = tk.Frame(
            left_container, bg="#485460", bd=3, relief="solid"
        )
        self.target_frame.pack(pady=5)

        # Right: Fleet Grid
        right_container = tk.Frame(boards_frame, bg="#1e272e")
        right_container.pack(side=tk.RIGHT, padx=15)
        self.fleet_title = tk.Label(
            right_container,
            text="🛡️ Your Fleet Grid",
            font=("Arial", 11, "bold"),
            bg="#1e272e",
            fg="#02c39a",
        )
        self.fleet_title.pack()

        self.fleet_frame = tk.Frame(
            right_container, bg="#485460", bd=3, relief="solid"
        )
        self.fleet_frame.pack(pady=5)

        self.target_buttons = {}
        self.fleet_buttons = {}

        self.create_grids_ui()
        self.update_placement_status()
        self.update_timer()

    def show_rules(self):
        rules = (
            "BATTLESHIP (STORY MODE):\n\n"
            "1. PLACEMENT PHASE: Place your secret ships on your Fleet Grid.\n"
            "   Use the 'Orientation' button to switch between Horizontal and Vertical.\n"
            "2. BATTLE PHASE: Take turns firing missiles at the Target Grid against Admiral Deep-Water Fleet.\n"
            "   💥 RED = HIT | 🌊 WHITE = MISS\n"
            "3. Destroy all enemy ships to defeat the King!"
        )
        messagebox.showinfo("How to Play - Battleship", rules)

    def toggle_orientation(self):
        if self.placement_orientation == "H":
            self.placement_orientation = "V"
            self.rotate_btn.config(text="🔄 Orientation: Vertical")
        else:
            self.placement_orientation = "H"
            self.rotate_btn.config(text="🔄 Orientation: Horizontal")

    def update_placement_status(self):
        if self.current_ship_idx < len(self.ships_to_place):
            name, length = self.ships_to_place[self.current_ship_idx]
            self.status_label.config(
                text=f"{self.player_name}: Place your {name} (Length: {length})",
                fg="#00d8d6",
            )
        else:
            self.status_label.config(
                text=f"{self.player_name}: All ships placed! Click 'Ready for Battle!'",
                fg="#2ecc71",
            )
            self.start_battle_btn.config(state=tk.NORMAL)

    def place_random_fleet(self, grid):
        ship_sizes = [4, 3, 2, 2]
        for size in ship_sizes:
            placed = False
            while not placed:
                orientation = random.choice(["H", "V"])
                if orientation == "H":
                    r = random.randint(0, 7)
                    c = random.randint(0, 8 - size)
                    if all(grid[r][c + i] == "." for i in range(size)):
                        for i in range(size):
                            grid[r][c + i] = "S"
                        placed = True
                else:
                    r = random.randint(0, 8 - size)
                    c = random.randint(0, 7)
                    if all(grid[r + i][c] == "." for i in range(size)):
                        for i in range(size):
                            grid[r + i][c] = "S"
                        placed = True

    def create_grids_ui(self):
        # Target Grid Buttons
        for r in range(8):
            for c in range(8):
                btn = tk.Button(
                    self.target_frame,
                    text="~",
                    font=("Arial", 12, "bold"),
                    width=3,
                    height=1,
                    bg="#0abde3",
                    fg="white",
                    command=lambda row=r, col=c: self.fire_shot(row, col),
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.target_buttons[(r, c)] = btn

        # Fleet Grid Buttons
        for r in range(8):
            for c in range(8):
                btn = tk.Button(
                    self.fleet_frame,
                    text="~",
                    font=("Arial", 12, "bold"),
                    width=3,
                    height=1,
                    bg="#0abde3",
                    fg="white",
                    command=lambda row=r, col=c: self.handle_fleet_click(row, col),
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.fleet_buttons[(r, c)] = btn

        self.update_fleet_ui()

    def handle_fleet_click(self, r, c):
        if self.phase != "PLACEMENT" or self.current_ship_idx >= len(self.ships_to_place):
            return

        name, length = self.ships_to_place[self.current_ship_idx]
        grid = self.p1_ships

        can_place = True
        coords = []
        if self.placement_orientation == "H":
            if c + length > 8:
                can_place = False
            else:
                for i in range(length):
                    if grid[r][c + i] != ".":
                        can_place = False
                    coords.append((r, c + i))
        else:
            if r + length > 8:
                can_place = False
            else:
                for i in range(length):
                    if grid[r + i][c] != ".":
                        can_place = False
                    coords.append((r + i, c))

        if can_place:
            for cr, cc in coords:
                grid[cr][cc] = "S"
            self.current_ship_idx += 1
            self.update_fleet_ui()
            self.update_placement_status()
        else:
            messagebox.showwarning(
                "Invalid Placement", "Ship cannot overlap or go off the board!"
            )

    def finish_placement(self):
        self.phase = "BATTLE"
        self.control_frame.pack_forget()
        messagebox.showinfo(
            "Battle Commences! 💥", "Fleet placed! {0} starts the attack against Admiral Deep-Water Fleet.".format(self.player_name)
        )
        self.turn = "Player 1"
        self.status_label.config(
            text=f"Turn: {self.player_name} - Fire a shot on the Target Grid!",
            fg="#00d8d6",
        )
        self.update_fleet_ui()

    def fire_shot(self, r, c):
        if self.phase != "BATTLE" or self.game_over:
            return

        shots_grid = self.p1_shots
        target_ships = self.p2_ships

        if shots_grid[r][c] != ".":
            return

        if target_ships[r][c] == "S":
            shots_grid[r][c] = "H"
            target_ships[r][c] = "H"
            self.target_buttons[(r, c)].config(
                text="💥", bg="#ee5253", state=tk.DISABLED
            )
            self.status_label.config(
                text=f"{self.player_name}: DIRECT HIT! 💥 Fire again!", fg="#ff4757"
            )
        else:
            shots_grid[r][c] = "M"
            self.target_buttons[(r, c)].config(
                text="🌊", bg="#c8d6e5", fg="#222f3e", state=tk.DISABLED
            )
            self.status_label.config(
                text=f"{self.player_name}: Splash! MISSED 🌊", fg="#fca510"
            )

        # Check Win Condition
        if not any("S" in row for row in target_ships):
            self.game_over = True
            self.timer_running = False
            if self.story_frame:
                self.story_frame.kings_defeated_this_run += 1
            messagebox.showinfo(
                "King Defeated!", f"🏆 {self.player_name} destroyed Admiral Deep-Water Fleet's entire fleet!"
            )
            self.status_label.config(text=f"{self.player_name} WINS!", fg="#f1c40f")
            self.root.destroy()
            return

        if not self.game_over:
            self.root.after(600, self.ai_fire)

    def ai_fire(self):
        if self.game_over:
            return

        unshot = [
            (r, c)
            for r in range(8)
            for c in range(8)
            if self.p2_shots[r][c] == "."
        ]
        if unshot:
            r, c = random.choice(unshot)
            if self.p1_ships[r][c] == "S":
                self.p2_shots[r][c] = "H"
                self.p1_ships[r][c] = "H"
            else:
                self.p2_shots[r][c] = "M"

            self.update_fleet_ui()

            if not any("S" in row for row in self.p1_ships):
                self.game_over = True
                self.timer_running = False
                if self.story_frame:
                    self.story_frame.end_run(was_victory=False)
                messagebox.showinfo("Defeat", "Admiral Deep-Water Fleet destroyed your fleet!")
                self.status_label.config(text="Admiral Deep-Water Fleet Wins!", fg="#ee5253")
                self.root.destroy()

    def update_fleet_ui(self):
        if self.phase == "PLACEMENT":
            grid = self.p1_ships
        else:
            grid = self.p1_ships

        for r in range(8):
            for c in range(8):
                val = grid[r][c]
                if val == "S":
                    self.fleet_buttons[(r, c)].config(text="🚢", bg="#576574", fg="white")
                elif val == "H":
                    self.fleet_buttons[(r, c)].config(text="💥", bg="#ee5253", fg="white")
                elif val == "M":
                    self.fleet_buttons[(r, c)].config(
                        text="🌊", bg="#c8d6e5", fg="#222f3e"
                    )
                else:
                    self.fleet_buttons[(r, c)].config(
                        text="~", bg="#0abde3", fg="white"
                    )

    def update_timer(self):
        if self.timer_running and not self.game_over and self.phase == "BATTLE":
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
                    messagebox.showinfo("Time Out!", f"{self.player_name} ran out of time! Admiral Deep-Water Fleet wins!")
                else:
                    if self.story_frame:
                        self.story_frame.kings_defeated_this_run += 1
                    messagebox.showinfo("Time Out!", "Admiral Deep-Water Fleet ran out of time! You win!")
                self.root.destroy()
                return

        self.root.after(1000, self.update_timer)

def run_mode(parent, player_name="Player", story_frame=None):
    app = BattleshipApp(parent, player_name=player_name, story_frame=story_frame)
    return app
