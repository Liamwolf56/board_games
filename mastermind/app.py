import random
import sys
import tkinter as tk
from tkinter import messagebox


class MastermindApp:

  def __init__(self, root, mode="PvP"):
    self.root = root
    self.root.title(f"Mastermind - Mode: {mode}")
    self.root.geometry("640x820")
    self.root.config(bg="#1e272e")

    self.mode = mode
    self.game_over = False
    self.current_attempt = 0
    self.max_attempts = 10

    # Available colors
    self.colors = ["RED", "BLUE", "GREEN", "YELLOW", "PURPLE", "WHITE"]
    self.color_map = {
        "RED": "#e74c3c",
        "BLUE": "#3498db",
        "GREEN": "#2ecc71",
        "YELLOW": "#f1c40f",
        "PURPLE": "#9b59b6",
        "WHITE": "#ecf0f1",
    }

    # Secret Code (4 colors)
    self.secret_code = [random.choice(self.colors) for _ in range(4)]
    self.current_guess = ["", "", "", ""]
    self.active_peg_slot = 0

    # Match Timers (300 seconds / 5 mins)
    self.time_left = 300
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
        text="Time: 05:00",
        font=("Arial", 11, "bold"),
        bg="#1e272e",
        fg="white",
    )
    self.timer_label.pack(side=tk.RIGHT)

    self.status_label = tk.Label(
        root,
        text="Attempt 1/10: Select 4 colors to build your guess",
        font=("Arial", 11, "bold"),
        bg="#1e272e",
        fg="#00d8d6",
    )
    self.status_label.pack(pady=5)

    # Color Palette Selection Frame
    palette_frame = tk.Frame(root, bg="#2c3e50", bd=2, relief="solid")
    palette_frame.pack(pady=5, padx=10)

    tk.Label(
        palette_frame,
        text="COLOR PALETTE:",
        font=("Arial", 9, "bold"),
        bg="#2c3e50",
        fg="white",
    ).pack(side=tk.LEFT, padx=5)

    for c_name in self.colors:
      hex_c = self.color_map[c_name]
      fg_t = "#2c3e50" if c_name == "WHITE" else "#ffffff"
      btn = tk.Button(
          palette_frame,
          text=c_name,
          font=("Arial", 8, "bold"),
          bg=hex_c,
          fg=fg_t,
          width=7,
          command=lambda c=c_name: self.select_color(c),
      )
      btn.pack(side=tk.LEFT, padx=2, pady=5)

    # Guessing Board Grid (10 Rows)
    board_frame = tk.Frame(root, bg="#2c3e50", bd=3, relief="solid")
    board_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    self.rows_ui = []
    for r in range(self.max_attempts):
      row_f = tk.Frame(board_frame, bg="#2c3e50")
      row_f.pack(pady=2)

      lbl = tk.Label(
          row_f,
          text=f"#{10-r:02d}",
          font=("Arial", 9, "bold"),
          bg="#2c3e50",
          fg="#7f8c8d",
          width=3,
      )
      lbl.pack(side=tk.LEFT, padx=2)

      peg_btns = []
      for c in range(4):
        p_btn = tk.Button(
            row_f,
            text="",
            font=("Arial", 8, "bold"),
            width=6,
            bg="#34495e",
            state=tk.DISABLED,
        )
        p_btn.pack(side=tk.LEFT, padx=2)
        peg_btns.append(p_btn)

      fb_lbl = tk.Label(
          row_f,
          text="",
          font=("Arial", 10, "bold"),
          bg="#2c3e50",
          fg="#f1c40f",
          width=12,
          anchor="w",
      )
      fb_lbl.pack(side=tk.LEFT, padx=10)

      self.rows_ui.append(
          {"pegs": peg_btns, "feedback": fb_lbl, "label": lbl}
      )

    # Submit Button
    self.submit_btn = tk.Button(
        root,
        text="Submit Guess",
        font=("Arial", 11, "bold"),
        bg="#2ecc71",
        fg="white",
        state=tk.DISABLED,
        command=self.submit_guess,
    )
    self.submit_btn.pack(pady=10)

    self.update_active_row_ui()
    self.update_timer()

  def show_rules(self):
    rules = (
        "MASTERMIND RULES:\n\n"
        "1. Crack the secret 4-color code in 10 attempts or less!\n"
        "2. Click colors from the palette to fill your 4 guess slots.\n"
        "3. Feedback:\n"
        "   • Black Peg (●): Correct color in the EXACT position.\n"
        "   • White Peg (○): Correct color in the WRONG position."
    )
    messagebox.showinfo("How to Play - Mastermind", rules)

  def select_color(self, color_name):
    if self.game_over or self.active_peg_slot >= 4:
      return

    self.current_guess[self.active_peg_slot] = color_name

    # Display on current row
    row_idx = self.max_attempts - 1 - self.current_attempt
    btn = self.rows_ui[row_idx]["pegs"][self.active_peg_slot]
    hex_c = self.color_map[color_name]
    fg_t = "#2c3e50" if color_name == "WHITE" else "#ffffff"
    btn.config(text=color_name, bg=hex_c, fg=fg_t)

    self.active_peg_slot += 1

    if self.active_peg_slot == 4:
      self.submit_btn.config(state=tk.NORMAL)

  def submit_guess(self):
    if self.game_over or self.active_peg_slot < 4:
      return

    # Calculate Feedback Pegs
    black_pegs = 0
    white_pegs = 0

    secret_copy = list(self.secret_code)
    guess_copy = list(self.current_guess)

    # First pass: Exact matches (Black Pegs)
    for i in range(4):
      if guess_copy[i] == secret_copy[i]:
        black_pegs += 1
        secret_copy[i] = None
        guess_copy[i] = None

    # Second pass: Wrong position matches (White Pegs)
    for i in range(4):
      if guess_copy[i] is not None and guess_copy[i] in secret_copy:
        white_pegs += 1
        secret_copy[secret_copy.index(guess_copy[i])] = None

    # Update feedback text
    row_idx = self.max_attempts - 1 - self.current_attempt
    fb_text = f"● x{black_pegs} | ○ x{white_pegs}"
    self.rows_ui[row_idx]["feedback"].config(text=fb_text)

    # Check Win Condition
    if black_pegs == 4:
      self.game_over = True
      self.timer_running = False
      messagebox.showinfo(
          "🏆 Code Broken!",
          f"You cracked the secret code in {self.current_attempt + 1} attempts!",
      )
      self.status_label.config(text="WINNER! Code Cracked! 🏆", fg="#f1c40f")
      return

    self.current_attempt += 1

    # Check Defeat
    if self.current_attempt >= self.max_attempts:
      self.game_over = True
      self.timer_running = False
      code_str = " - ".join(self.secret_code)
      messagebox.showinfo(
          "Game Over", f"Out of attempts! Secret code was:\n{code_str}"
      )
      self.status_label.config(
          text=f"Game Over! Code was: {code_str}", fg="#e74c3c"
      )
      return

    # Reset for next row
    self.current_guess = ["", "", "", ""]
    self.active_peg_slot = 0
    self.submit_btn.config(state=tk.DISABLED)
    self.status_label.config(
        text=f"Attempt {self.current_attempt + 1}/10: Select 4 colors for your guess"
    )
    self.update_active_row_ui()

  def update_active_row_ui(self):
    for r in range(self.max_attempts):
      row_idx = self.max_attempts - 1 - r
      if r == self.current_attempt:
        self.rows_ui[row_idx]["label"].config(fg="#f1c40f")
      else:
        self.rows_ui[row_idx]["label"].config(fg="#7f8c8d")

  def update_timer(self):
    if self.timer_running and not self.game_over:
      if self.time_left > 0:
        self.time_left -= 1

      mins, secs = divmod(self.time_left, 60)
      self.timer_label.config(text=f"Time: {mins:02d}:{secs:02d}")

      if self.time_left == 0:
        self.game_over = True
        self.timer_running = False
        code_str = " - ".join(self.secret_code)
        messagebox.showinfo(
            "Time Out!", f"Time ran out! Secret code was:\n{code_str}"
        )

    self.root.after(1000, self.update_timer)


if __name__ == "__main__":
  mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
  root = tk.Tk()
  app = MastermindApp(root, mode)
  root.mainloop()
