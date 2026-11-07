import random
import sys
import tkinter as tk
from tkinter import messagebox


class OtrioApp:

  def __init__(self, root, mode="PvP"):
    self.root = root
    self.root.title(f"Otrio - Mode: {mode}")
    self.root.geometry("680x820")
    self.root.config(bg="#2c3e50")

    self.mode = mode
    self.turn = "Red"  # Red vs Blue
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
        text="Red: 05:00 | Blue: 05:00",
        font=("Arial", 11, "bold"),
        bg="#2c3e50",
        fg="white",
    )
    self.timer_label.pack(side=tk.RIGHT)

    self.status_label = tk.Label(
        root,
        text="Turn: Red Player (Select ring size & place)",
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
        bg="#f1c40f",
        fg="#2c3e50",
        command=lambda: self.set_ring_size("L"),
    )
    self.btn_large.pack(side=tk.LEFT, padx=3)

    self.btn_medium = tk.Button(
        size_frame,
        text="🟢 Medium",
        font=("Arial", 10, "bold"),
        bg="#bdc3c7",
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
            text="[  ]",
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
        "OTRIO RULES & WIN CONDITIONS:\n\n"
        "1. Select a ring size (Large, Medium, or Small) and click an open space on the 3x3 grid.\n"
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
        f"Red Inventory: L={red_inv['L']} M={red_inv['M']} S={red_inv['S']} | "
        f"Blue Inventory: L={blue_inv['L']} M={blue_inv['M']} S={blue_inv['S']}"
    )
    self.inventory_label.config(text=txt)

  def square_clicked(self, r, c):
    if self.game_over:
      return

    size = self.selected_size
    player = self.turn

    # Check if player has this size remaining
    if self.inventory[player][size] <= 0:
      messagebox.showwarning(
          "No Rings Left", f"You have no remaining {size} rings left!"
      )
      return

    # Check if slot in cell is empty
    if self.board[r][c][size] is not None:
      messagebox.showwarning(
          "Slot Occupied", f"There is already a {size} ring in this square!"
      )
      return

    # Place piece
    self.board[r][c][size] = player
    self.inventory[player][size] -= 1
    self.update_board_ui()
    self.update_inventory_ui()

    if self.check_win(player):
      self.game_over = True
      self.timer_running = False
      messagebox.showinfo("🏆 Game Over!", f"{player} Player Wins Otrio!")
      self.status_label.config(text=f"Winner: {player} Player!", fg="#f1c40f")
      return

    # Check for Draw (no inventory left for current player)
    if all(count == 0 for count in self.inventory[player].values()):
      self.game_over = True
      self.timer_running = False
      messagebox.showinfo("Game Over", "Out of moves! It's a draw!")
      return

    self.finish_turn()

  def finish_turn(self):
    self.turn = "Blue" if self.turn == "Red" else "Red"
    color_code = "#e74c3c" if self.turn == "Red" else "#3498db"
    self.status_label.config(text=f"Turn: {self.turn} Player", fg=color_code)

    if self.mode == "PvAI" and self.turn == "Blue" and not self.game_over:
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
        messagebox.showinfo("Game Over", "Blue AI Wins Otrio!")
        self.status_label.config(text="Winner: Blue AI!", fg="#f1c40f")
        return

      self.finish_turn()

  def check_win(self, p):
    b = self.board

    # 1. Concentric single-cell win: L, M, and S of player 'p' in same cell
    for r in range(3):
      for c in range(3):
        if (
            b[r][c]["L"] == p
            and b[r][c]["M"] == p
            and b[r][c]["S"] == p
        ):
          return True

    lines = []
    # Rows and Columns
    for i in range(3):
      lines.append([(i, 0), (i, 1), (i, 2)])
      lines.append([(0, i), (1, i), (2, i)])
    # Diagonals
    lines.append([(0, 0), (1, 1), (2, 2)])
    lines.append([(0, 2), (1, 1), (2, 0)])

    for line in lines:
      # 2. Same size in a row win
      for sz in ["L", "M", "S"]:
        if all(b[r][c][sz] == p for r, c in line):
          return True

      # 3. Concentric ascending/descending size win
      p0, p1, p2 = line
      # S -> M -> L
      if (
          b[p0[0]][p0[1]]["S"] == p
          and b[p1[0]][p1[1]]["M"] == p
          and b[p2[0]][p2[1]]["L"] == p
      ):
        return True
      # L -> M -> S
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
          text=f"Red: {r_min:02d}:{r_sec:02d} | Blue: {b_min:02d}:{b_sec:02d}"
      )

      if self.red_time == 0 or self.blue_time == 0:
        self.game_over = True
        self.timer_running = False
        loser = "Red" if self.red_time == 0 else "Blue"
        winner = "Blue" if loser == "Red" else "Red"
        messagebox.showinfo("Time Out!", f"{loser} ran out of time! {winner} wins!")

    self.root.after(1000, self.update_timer)


if __name__ == "__main__":
  mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
  root = tk.Tk()
  app = OtrioApp(root, mode)
  root.mainloop()
