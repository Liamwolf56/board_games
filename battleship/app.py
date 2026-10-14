import random
import sys
import tkinter as tk
from tkinter import messagebox


class BattleshipApp:

  def __init__(self, root, mode="PvP"):
    self.root = root
    self.root.title(f"Battleship - Mode: {mode}")
    self.root.geometry("860x780")
    self.root.config(bg="#1e272e")

    self.mode = mode
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

    # If PvAI, generate AI fleet immediately
    if self.mode == "PvAI":
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
        text="Player 1: 05:00 | Player 2: 05:00",
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
        "BATTLESHIP RULES:\n\n"
        "1. PLACEMENT PHASE: Each player places their secret ships on their Fleet Grid.\n"
        "   Use the 'Orientation' button to switch between Horizontal and Vertical.\n"
        "2. BATTLE PHASE: Take turns firing missiles at the Target Grid.\n"
        "   💥 RED = HIT | 🌊 WHITE = MISS\n"
        "3. Destroy all enemy ships to win!"
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
          text=f"{self.active_placing_player}: Place your {name} (Length:"
          f" {length})",
          fg="#00d8d6",
      )
    else:
      self.status_label.config(
          text=f"{self.active_placing_player}: All ships placed! Click 'Ready"
          " for Battle!'",
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
    if self.phase != "PLACEMENT" or self.current_ship_idx >= len(
        self.ships_to_place
    ):
      return

    name, length = self.ships_to_place[self.current_ship_idx]
    grid = (
        self.p1_ships
        if self.active_placing_player == "Player 1"
        else self.p2_ships
    )

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
    if self.mode == "PvP" and self.active_placing_player == "Player 1":
      # Transition to Player 2 Placement
      self.active_placing_player = "Player 2"
      self.current_ship_idx = 0
      self.start_battle_btn.config(state=tk.DISABLED)
      messagebox.showinfo(
          "Pass Device",
          "Player 1 fleet locked in!\nPass the device to Player 2 to place"
          " their ships.",
      )
      self.update_fleet_ui()
      self.update_placement_status()
    else:
      # Both players placed ships -> Begin Battle Phase
      self.phase = "BATTLE"
      self.control_frame.pack_forget()
      messagebox.showinfo(
          "Battle Commences! 💥", "All fleets placed! Player 1 starts the attack."
      )
      self.turn = "Player 1"
      self.status_label.config(
          text="Turn: Player 1 - Fire a shot on the Target Grid!",
          fg="#00d8d6",
      )
      self.update_fleet_ui()

  def fire_shot(self, r, c):
    if self.phase != "BATTLE" or self.game_over:
      return

    # Determine targeting and defending player boards
    if self.turn == "Player 1":
      shots_grid = self.p1_shots
      target_ships = self.p2_ships
    else:
      shots_grid = self.p2_shots
      target_ships = self.p1_ships

    if shots_grid[r][c] != ".":
      return

    if target_ships[r][c] == "S":
      shots_grid[r][c] = "H"
      target_ships[r][c] = "H"
      self.target_buttons[(r, c)].config(
          text="💥", bg="#ee5253", state=tk.DISABLED
      )
      self.status_label.config(
          text=f"{self.turn}: DIRECT HIT! 💥 Fire again!", fg="#ff4757"
      )
    else:
      shots_grid[r][c] = "M"
      self.target_buttons[(r, c)].config(
          text="🌊", bg="#c8d6e5", fg="#222f3e", state=tk.DISABLED
      )
      self.status_label.config(
          text=f"{self.turn}: Splash! MISSED 🌊", fg="#fca510"
      )

    # Check Win Condition
    if not any("S" in row for row in target_ships):
      self.game_over = True
      self.timer_running = False
      messagebox.showinfo(
          "🏆 Victory!", f"{self.turn} destroyed the entire enemy fleet!"
      )
      self.status_label.config(text=f"{self.turn} WINS!", fg="#f1c40f")
      return

    # Turn / AI rotation
    if self.mode == "PvAI":
      if not self.game_over:
        self.root.after(600, self.ai_fire)
    else:
      # PvP Turn Switch
      self.turn = "Player 2" if self.turn == "Player 1" else "Player 1"
      messagebox.showinfo(
          "Pass Device", f"Turn ended. Pass device to {self.turn}."
      )
      self.status_label.config(
          text=f"Turn: {self.turn} - Fire a shot on the Target Grid!",
          fg="#00d8d6",
      )
      self.update_target_buttons_for_turn()
      self.update_fleet_ui()

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
        messagebox.showinfo("Game Over", "Enemy AI destroyed your fleet!")
        self.status_label.config(text="Enemy AI Wins!", fg="#ee5253")

  def update_target_buttons_for_turn(self):
    # Refresh targeting grid visual state based on current player's past shots
    shots_grid = self.p1_shots if self.turn == "Player 1" else self.p2_shots
    for r in range(8):
      for c in range(8):
        st = shots_grid[r][c]
        btn = self.target_buttons[(r, c)]
        if st == "H":
          btn.config(text="💥", bg="#ee5253", state=tk.DISABLED)
        elif st == "M":
          btn.config(text="🌊", bg="#c8d6e5", fg="#222f3e", state=tk.DISABLED)
        else:
          btn.config(text="~", bg="#0abde3", fg="white", state=tk.NORMAL)

  def update_fleet_ui(self):
    if self.phase == "PLACEMENT":
      grid = (
          self.p1_ships
          if self.active_placing_player == "Player 1"
          else self.p2_ships
      )
    else:
      grid = self.p1_ships if self.turn == "Player 1" else self.p2_ships

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
          text=f"Player 1: {p1_min:02d}:{p1_sec:02d} | Player 2:"
          f" {p2_min:02d}:{p2_sec:02d}"
      )

      if self.p1_time == 0 or self.p2_time == 0:
        self.game_over = True
        self.timer_running = False
        loser = "Player 1" if self.p1_time == 0 else "Player 2"
        winner = "Player 2" if loser == "Player 1" else "Player 1"
        messagebox.showinfo("Time Out!", f"{loser} ran out of time! {winner} wins!")

    self.root.after(1000, self.update_timer)


if __name__ == "__main__":
  mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
  root = tk.Tk()
  app = BattleshipApp(root, mode)
  root.mainloop()
