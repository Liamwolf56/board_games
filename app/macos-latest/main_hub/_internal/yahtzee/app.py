import random
import sys
import tkinter as tk
from tkinter import messagebox


class YahtzeeApp:

  def __init__(self, root, mode="PvP"):
    self.root = root
    self.root.title(f"Yahtzee - Mode: {mode}")
    self.root.geometry("820x760")
    self.root.config(bg="#1e272e")

    self.mode = mode
    self.turn = "Player 1"
    self.rolls_left = 3
    self.game_over = False

    self.dice = [1, 1, 1, 1, 1]
    self.held = [False, False, False, False, False]
    self.dice_rolled_this_turn = False

    # Scorecards: dict mapping category name to score or None
    # Categories: Aces, Twos, Threes, Fours, Fives, Sixes, 3Kind, 4Kind, FullHouse, SmStraight, LgStraight, Yahtzee, Chance
    self.categories = [
        "Aces",
        "Twos",
        "Threes",
        "Fours",
        "Fives",
        "Sixes",
        "3 of a Kind",
        "4 of a Kind",
        "Full House",
        "Small Straight",
        "Large Straight",
        "Yahtzee",
        "Chance",
    ]

    self.p1_scores = {cat: None for cat in self.categories}
    self.p2_scores = {cat: None for cat in self.categories}

    # Timers (300 seconds / 5 mins)
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
        text="Player 1: 05:00 | Player 2: 05:00",
        font=("Arial", 11, "bold"),
        bg="#1e272e",
        fg="white",
    )
    self.timer_label.pack(side=tk.RIGHT)

    self.status_label = tk.Label(
        root,
        text="Turn: Player 1 - Click 'Roll Dice' to start your turn",
        font=("Arial", 12, "bold"),
        bg="#1e272e",
        fg="#00d8d6",
    )
    self.status_label.pack(pady=5)

    # Dice Container
    dice_frame = tk.Frame(root, bg="#2c3e50", bd=3, relief="solid")
    dice_frame.pack(pady=10, padx=10, fill=tk.X)

    tk.Label(
        dice_frame,
        text="Click dice to HOLD them between rolls",
        font=("Arial", 10, "bold"),
        bg="#2c3e50",
        fg="#ffdd59",
    ).pack(pady=3)

    self.dice_buttons_frame = tk.Frame(dice_frame, bg="#2c3e50")
    self.dice_buttons_frame.pack(pady=5)

    self.dice_buttons = []
    for i in range(5):
      btn = tk.Button(
          self.dice_buttons_frame,
          text="[ 1 ]",
          font=("Arial", 14, "bold"),
          width=8,
          height=2,
          bg="#ecf0f1",
          fg="#2c3e50",
          command=lambda idx=i: self.toggle_hold(idx),
      )
      btn.pack(side=tk.LEFT, padx=6)
      self.dice_buttons.append(btn)

    control_sub_frame = tk.Frame(dice_frame, bg="#2c3e50")
    control_sub_frame.pack(pady=5)

    self.roll_btn = tk.Button(
        control_sub_frame,
        text="🎲 Roll Dice (3 left)",
        font=("Arial", 11, "bold"),
        bg="#2ecc71",
        fg="white",
        command=self.roll_dice,
    )
    self.roll_btn.pack(side=tk.LEFT, padx=10)

    # Scorecard Container
    score_container = tk.Frame(root, bg="#2c3e50", bd=3, relief="solid")
    score_container.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

    tk.Label(
        score_container,
        text="YAHTZEE SCORECARD (Click a category to lock your score)",
        font=("Arial", 10, "bold"),
        bg="#2c3e50",
        fg="#3498db",
    ).pack(pady=3)

    self.score_buttons_frame = tk.Frame(score_container, bg="#2c3e50")
    self.score_buttons_frame.pack(pady=5, fill=tk.BOTH, expand=True)

    self.score_buttons = {}
    for cat in self.categories:
      row_f = tk.Frame(self.score_buttons_frame, bg="#2c3e50")
      row_f.pack(fill=tk.X, pady=1)

      lbl = tk.Label(
          row_f,
          text=cat,
          font=("Arial", 10, "bold"),
          width=16,
          anchor="w",
          bg="#2c3e50",
          fg="white",
      )
      lbl.pack(side=tk.LEFT, padx=5)

      p1_btn = tk.Button(
          row_f,
          text="-",
          font=("Arial", 9, "bold"),
          width=12,
          bg="#34495e",
          fg="white",
          command=lambda c=cat: self.score_category(c),
      )
      p1_btn.pack(side=tk.LEFT, padx=5)
      self.score_buttons[("Player 1", cat)] = p1_btn

      p2_btn = tk.Button(
          row_f,
          text="-",
          font=("Arial", 9, "bold"),
          width=12,
          bg="#34495e",
          fg="white",
          state=tk.DISABLED,
      )
      p2_btn.pack(side=tk.LEFT, padx=5)
      self.score_buttons[("Player 2", cat)] = p2_btn

    self.update_ui()
    self.update_timer()

  def show_rules(self):
    rules = (
        "YAHTZEE RULES:\n\n"
        "1. Roll the 5 dice up to 3 times per turn.\n"
        "2. Click dice to HOLD them between rolls.\n"
        "3. Select an open category on your scorecard to lock in your points for that turn.\n"
        "4. Fill all categories to achieve your final score!"
    )
    messagebox.showinfo("How to Play - Yahtzee", rules)

  def toggle_hold(self, idx):
    if not self.dice_rolled_this_turn or self.game_over:
      return
    self.held[idx] = not self.held[idx]
    self.update_ui()

  def roll_dice(self):
    if self.rolls_left <= 0 or self.game_over:
      return

    for i in range(5):
      if not self.held[i]:
        self.dice[i] = random.randint(1, 6)

    self.rolls_left -= 1
    self.dice_rolled_this_turn = True
    self.roll_btn.config(
        text=f"🎲 Roll Dice ({self.rolls_left} left)",
        bg="#e67e22" if self.rolls_left > 0 else "#7f8c8d",
    )
    self.update_ui()

  def calculate_potential_score(self, cat, dice_vals):
    counts = {n: dice_vals.count(n) for n in range(1, 7)}
    total = sum(dice_vals)

    if cat == "Aces":
      return counts[1] * 1
    elif cat == "Twos":
      return counts[2] * 2
    elif cat == "Threes":
      return counts[3] * 3
    elif cat == "Fours":
      return counts[4] * 4
    elif cat == "Fives":
      return counts[5] * 5
    elif cat == "Sixes":
      return counts[6] * 6
    elif cat == "3 of a Kind":
      return total if any(c >= 3 for c in counts.values()) else 0
    elif cat == "4 of a Kind":
      return total if any(c >= 4 for c in counts.values()) else 0
    elif cat == "Full House":
      has_3 = 3 in counts.values()
      has_2 = 2 in counts.values()
      has_5 = 5 in counts.values()
      return 25 if (has_3 and has_2) or has_5 else 0
    elif cat == "Small Straight":
      sorted_u = sorted(list(set(dice_vals)))
      straights = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]]
      for s in straights:
        if all(val in sorted_u for val in s):
          return 30
      return 0
    elif cat == "Large Straight":
      sorted_u = sorted(list(set(dice_vals)))
      if sorted_u == [1, 2, 3, 4, 5] or sorted_u == [2, 3, 4, 5, 6]:
        return 40
      return 0
    elif cat == "Yahtzee":
      return 50 if any(c == 5 for c in counts.values()) else 0
    elif cat == "Chance":
      return total
    return 0

  def score_category(self, cat):
    if not self.dice_rolled_this_turn or self.game_over:
      messagebox.showwarning(
          "Roll First", "Please roll the dice at least once before scoring!"
      )
      return

    scores_dict = self.p1_scores if self.turn == "Player 1" else self.p2_scores
    if scores_dict[cat] is not None:
      messagebox.showwarning(
          "Category Taken", "This category has already been scored!"
      )
      return

    score = self.calculate_potential_score(cat, self.dice)
    scores_dict[cat] = score

    self.finish_turn()

  def finish_turn(self):
    self.dice_rolled_this_turn = False
    self.rolls_left = 3
    self.held = [False, False, False, False, False]
    self.roll_btn.config(text="🎲 Roll Dice (3 left)", bg="#2ecc71")

    # Check if game is complete for both players
    p1_done = all(v is not None for v in self.p1_scores.values())
    p2_done = all(v is not None for v in self.p2_scores.values())

    if p1_done and p2_done:
      self.game_over = True
      self.timer_running = False
      p1_total = sum(v for v in self.p1_scores.values() if v is not None)
      p2_total = sum(v for v in self.p2_scores.values() if v is not None)

      if p1_total > p2_total:
        msg = f"Game Over! Player 1 Wins ({p1_total} to {p2_total})"
      elif p2_total > p1_total:
        msg = f"Game Over! Player 2 Wins ({p2_total} to {p1_total})"
      else:
        msg = f"Game Over! Tie Game ({p1_total} to {p2_total})"

      messagebox.showinfo("🏆 Final Scores", msg)
      self.status_label.config(text=msg, fg="#f1c40f")
      return

    self.turn = "Player 2" if self.turn == "Player 1" else "Player 1"
    color_code = "#00d8d6" if self.turn == "Player 1" else "#ff4757"
    self.status_label.config(
        text=f"Turn: {self.turn} - Click 'Roll Dice' to start", fg=color_code
    )
    self.update_ui()

    if self.mode == "PvAI" and self.turn == "Player 2" and not self.game_over:
      self.root.after(800, self.ai_turn)

  def ai_turn(self):
    if self.game_over:
      return

    # AI rolls once
    self.roll_dice()
    self.root.after(800, self.ai_score)

  def ai_score(self):
    if self.game_over:
      return

    # AI picks first available category
    for cat in self.categories:
      if self.p2_scores[cat] is None:
        self.p2_scores[cat] = self.calculate_potential_score(cat, self.dice)
        break

    self.finish_turn()

  def update_ui(self):
    # Update dice buttons
    for i, val in enumerate(self.dice):
      btn = self.dice_buttons[i]
      hld = self.held[i]
      bg_col = "#f1c40f" if hld else "#ecf0f1"
      txt = f"[{val}]" + ("\n(HOLD)" if hld else "")
      btn.config(text=txt, bg=bg_col)

    # Update scorecard buttons
    for cat in self.categories:
      p1_val = self.p1_scores[cat]
      p1_btn = self.score_buttons[("Player 1", cat)]
      if p1_val is not None:
        p1_btn.config(
            text=str(p1_val), state=tk.DISABLED, bg="#7f8c8d", fg="white"
        )
      else:
        if self.turn == "Player 1" and self.dice_rolled_this_turn:
          potential = self.calculate_potential_score(cat, self.dice)
          p1_btn.config(
              text=f"-> {potential}", state=tk.NORMAL, bg="#27ae60", fg="white"
          )
        else:
          p1_btn.config(text="-", state=tk.NORMAL, bg="#34495e", fg="white")

      p2_val = self.p2_scores[cat]
      p2_btn = self.score_buttons[("Player 2", cat)]
      if p2_val is not None:
        p2_btn.config(
            text=str(p2_val), state=tk.DISABLED, bg="#7f8c8d", fg="white"
        )
      else:
        if self.mode == "PvAI":
          p2_btn.config(text="-", state=tk.DISABLED, bg="#34495e", fg="white")
        else:
          if self.turn == "Player 2" and self.dice_rolled_this_turn:
            potential = self.calculate_potential_score(cat, self.dice)
            p2_btn.config(
                text=f"-> {potential}", state=tk.NORMAL, bg="#27ae60", fg="white"
            )
          else:
            p2_btn.config(text="-", state=tk.NORMAL, bg="#34495e", fg="white")

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
  app = YahtzeeApp(root, mode)
  root.mainloop()
