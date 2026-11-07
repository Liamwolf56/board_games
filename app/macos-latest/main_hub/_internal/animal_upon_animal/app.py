import random
import sys
import tkinter as tk
from tkinter import messagebox


class AnimalUponAnimalApp:

  def __init__(self, root, mode="PvP"):
    self.root = root
    self.root.title(f"Animal Upon Animal - Mode: {mode}")
    self.root.geometry("700x750")
    self.root.config(bg="#1e272e")

    self.mode = mode
    self.turn = "Player 1"  # Player 1 (Green) vs Player 2 (Orange)
    self.game_over = False
    self.die_rolled = False
    self.roll_result = None

    # Player Animal Inventories (7 animals each)
    self.p1_inventory = [
        "Snake",
        "Penguin",
        "Toucan",
        "Frilled Lizard",
        "Monkey",
        "Hedgehog",
        "Sheep",
    ]
    self.p2_inventory = [
        "Snake",
        "Penguin",
        "Toucan",
        "Frilled Lizard",
        "Monkey",
        "Hedgehog",
        "Sheep",
    ]

    # Stacking Pyramid state
    self.pyramid = ["Crocodile Base"]

    # Match Timers (300 seconds / 5 mins)
    self.p1_time = 300
    self.p2_time = 300
    self.timer_running = True

    # Top Bar
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
        text="Turn: Player 1 -> Click '🎲 Roll Die' to start your turn!",
        font=("Arial", 11, "bold"),
        bg="#1e272e",
        fg="#00d8d6",
    )
    self.status_label.pack(pady=5)

    # Die Roll Controls
    die_frame = tk.Frame(root, bg="#1e272e")
    die_frame.pack(pady=5)

    self.roll_btn = tk.Button(
        die_frame,
        text="🎲 Roll Die",
        font=("Arial", 12, "bold"),
        bg="#2ecc71",
        fg="white",
        command=self.roll_die,
    )
    self.roll_btn.pack(side=tk.LEFT, padx=10)

    self.die_label = tk.Label(
        die_frame,
        text="Die Result: [-]",
        font=("Arial", 12, "bold"),
        bg="#1e272e",
        fg="#ffdd59",
    )
    self.die_label.pack(side=tk.LEFT, padx=10)

    # Display Container (Pyramid Stack vs Hand Inventory)
    main_frame = tk.Frame(root, bg="#1e272e")
    main_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    # Left: Animal Pyramid Tower
    tower_container = tk.Frame(main_frame, bg="#2c3e50", bd=3, relief="solid")
    tower_container.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

    tk.Label(
        tower_container,
        text="🐊 Animal Stacking Pyramid 🐊",
        font=("Arial", 11, "bold"),
        bg="#2c3e50",
        fg="#2ecc71",
    ).pack(pady=5)

    self.pyramid_listbox = tk.Listbox(
        tower_container,
        font=("Arial", 12, "bold"),
        bg="#34495e",
        fg="#ecf0f1",
        justify="center",
    )
    self.pyramid_listbox.pack(
        padx=10, pady=10, fill=tk.BOTH, expand=True
    )

    # Right: Player Hand / Inventory
    hand_container = tk.Frame(main_frame, bg="#2c3e50", bd=3, relief="solid")
    hand_container.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)

    self.hand_title_label = tk.Label(
        hand_container,
        text="Player 1 Inventory:",
        font=("Arial", 11, "bold"),
        bg="#2c3e50",
        fg="#3498db",
    )
    self.hand_title_label.pack(pady=5)

    self.hand_frame = tk.Frame(hand_container, bg="#2c3e50")
    self.hand_frame.pack(pady=5, fill=tk.BOTH, expand=True)

    self.update_pyramid_ui()
    self.update_hand_ui()
    self.update_timer()

  def show_rules(self):
    rules = (
        "ANIMAL UPON ANIMAL RULES:\n\n"
        "1. Click 'Roll Die' to see your stacking assignment:\n"
        "   • Place 1 Animal: Click an animal from your inventory to stack it.\n"
        "   • Place 2 Animals: Stack 2 animals onto the pyramid.\n"
        "   • Pass Animal: Give one of your animals to your opponent!\n"
        "2. Careful! Risk of pyramid collapse if placed unstable.\n"
        "3. First player to clear their entire animal inventory wins!"
    )
    messagebox.showinfo("How to Play - Animal Upon Animal", rules)

  def roll_die(self):
    if self.game_over or self.die_rolled:
      return

    outcomes = ["PLACE_1", "PLACE_2", "PASS_ANIMAL"]
    self.roll_result = random.choice(outcomes)
    self.die_rolled = True
    self.roll_btn.config(state=tk.DISABLED)

    if self.roll_result == "PLACE_1":
      self.die_label.config(text="Die Result: Place 1 Animal 🐒")
      self.status_label.config(
          text=f"{self.turn}: Select 1 animal from your inventory to stack!",
          fg="#f1c40f",
      )
    elif self.roll_result == "PLACE_2":
      self.die_label.config(text="Die Result: Place 2 Animals 🦔🦔")
      self.status_label.config(
          text=f"{self.turn}: Select an animal to stack (1 of 2)", fg="#f1c40f"
      )
    elif self.roll_result == "PASS_ANIMAL":
      self.die_label.config(text="Die Result: Pass Animal 🎁")
      self.status_label.config(
          text=f"{self.turn}: Click an animal to pass to your opponent!",
          fg="#e67e22",
      )

    self.update_hand_ui()

  def stack_animal(self, animal_name):
    if self.game_over or not self.die_rolled:
      return

    inv = (
        self.p1_inventory
        if self.turn == "Player 1"
        else self.p2_inventory
    )
    other_inv = (
        self.p2_inventory
        if self.turn == "Player 1"
        else self.p1_inventory
    )

    if self.roll_result == "PASS_ANIMAL":
      inv.remove(animal_name)
      other_inv.append(animal_name)
      messagebox.showinfo(
          "Passed Animal!",
          f"{self.turn} passed a {animal_name} to the opponent!",
      )
      self.finish_turn()
      return

    # Check for balance/collapse risk (15% chance of stack collapse)
    collapse = len(self.pyramid) > 3 and random.random() < 0.15

    if collapse:
      messagebox.showwarning(
          "OH NO! COLLAPSE! 💥",
          f"The animal pyramid tumbled! {self.turn} takes an extra animal penalization!",
      )
      penalty = ["Snake", "Penguin", "Toucan"]
      inv.append(random.choice(penalty))
    else:
      inv.remove(animal_name)
      self.pyramid.append(f"📦 {animal_name} ({self.turn})")

    self.update_pyramid_ui()

    # Check Win Condition
    if len(inv) == 0:
      self.game_over = True
      self.timer_running = False
      messagebox.showinfo(
          "🏆 Victory!", f"{self.turn} successfully stacked all animals!"
      )
      self.status_label.config(text=f"Winner: {self.turn}!", fg="#f1c40f")
      return

    if self.roll_result == "PLACE_2":
      self.roll_result = "PLACE_1"  # Convert to second placement
      self.status_label.config(
          text=f"{self.turn}: Select your 2nd animal to stack!", fg="#f1c40f"
      )
      self.update_hand_ui()
    else:
      self.finish_turn()

  def finish_turn(self):
    self.die_rolled = False
    self.roll_result = None
    self.roll_btn.config(state=tk.NORMAL)
    self.die_label.config(text="Die Result: [-]")

    self.turn = "Player 2" if self.turn == "Player 1" else "Player 1"
    color_code = "#3498db" if self.turn == "Player 1" else "#e67e22"
    self.status_label.config(
        text=f"Turn: {self.turn} -> Click '🎲 Roll Die' to start your turn!",
        fg=color_code,
    )
    self.update_hand_ui()

    if self.mode == "PvAI" and self.turn == "Player 2" and not self.game_over:
      self.root.after(600, self.ai_turn)

  def ai_turn(self):
    if self.game_over:
      return

    self.roll_die()

    if self.p2_inventory:
      animal = random.choice(self.p2_inventory)
      self.root.after(600, lambda: self.stack_animal(animal))

  def update_pyramid_ui(self):
    self.pyramid_listbox.delete(0, tk.END)
    for item in reversed(self.pyramid):
      self.pyramid_listbox.insert(tk.END, item)

  def update_hand_ui(self):
    for widget in self.hand_frame.winfo_children():
      widget.destroy()

    inv = (
        self.p1_inventory
        if self.turn == "Player 1"
        else self.p2_inventory
    )
    title = (
        "Player 1 Inventory:"
        if self.turn == "Player 1"
        else "Player 2 Inventory:"
    )
    self.hand_title_label.config(text=f"{title} ({len(inv)} left)")

    for animal in inv:
      btn = tk.Button(
          self.hand_frame,
          text=f"🐾 {animal}",
          font=("Arial", 10, "bold"),
          bg="#34495e",
          fg="white",
          command=lambda a=animal: self.stack_animal(a),
      )
      if not self.die_rolled:
        btn.config(state=tk.DISABLED)
      btn.pack(fill=tk.X, pady=2)

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
  app = AnimalUponAnimalApp(root, mode)
  root.mainloop()
