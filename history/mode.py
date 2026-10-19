import tkinter as tk


class HistoryModeFrame(tk.Frame):

  def __init__(self, parent, hub_app):
    super().__init__(parent, bg="#2c3e50", bd=2, relief="solid")
    self.hub_app = hub_app

    tk.Label(
        self,
        text="📜 THE HISTORY OF BOARD GAMES",
        font=("Arial", 14, "bold"),
        bg="#2c3e50",
        fg="#ffdd59",
    ).pack(pady=10)

    self.game_histories = {
        "Chess": (
            "Originating in 6th-century India as Chaturanga, Chess evolved"
            " through Persia and medieval Europe into the ultimate strategy game"
            " of kings."
        ),
        "Shogi": (
            "Known as Japanese Chess, Shogi developed in feudal Japan."
            " Unique for its 'drop' rule, allowing captured enemy pieces to be"
            " reused."
        ),
        "Xiangqi": (
            "Chinese Chess dates back to the Han Dynasty. It features a river"
            " in the middle and cannons that jump over pieces to attack."
        ),
        "Chaturanga": (
            "The ancient ancestor of Chess, Shogi, and Xiangqi. Played in 6th"
            " century India representing four divisions of the military."
        ),
        "Checkers": (
            "Traceable to 3000 BCE in ancient Mesopotamia (Ur). Played across"
            " centuries with simple yet deep jumping strategy."
        ),
        "Reversi": (
            "Invented in 1883 in England by Lewis Waterman, later popularized"
            " worldwide as Othello in 1970s Japan."
        ),
        "Connect 4": (
            "First published by Milton Bradley in 1974. A vertical drop strategy"
            " game inspired by classic Tic-Tac-Toe mechanics."
        ),
        "Tic-Tac-Toe": (
            "Traced back to ancient Egypt around 1300 BCE. One of the oldest known"
            " two-player alignment games in human history."
        ),
        "Battleship": (
            "Originated as a pad-and-pencil game during World War I before being"
            " produced as a plastic board game by Milton Bradley in 1967."
        ),
        "Otrio": (
            "A modern, multi-tiered expansion of Tic-Tac-Toe invented by Brain"
            " Wright, featuring concentric rings and chain strategy."
        ),
        "Sequence for Kids": (
            "A streamlined child-friendly variant of the famous 1981 board game"
            " Sequence, matching cards with board animal icons."
        ),
        "Animal Upon Animal": (
            "Created in Germany by HABA in 2005. A physical dexterity stacking"
            " game designed to challenge steady hands."
        ),
        "Monza": (
            "Designed by HABA in 2000. A tactical racing game where dice roll"
            " colors dictate track movement across racing lanes."
        ),
        "Yahtzee": (
            "Invented in 1954 by a Canadian couple who played it on their yacht."
            " Later bought by E.S. Lowe and trademarked as Yahtzee in 1956."
        ),
        "Mastermind": (
            "Invented in 1970 by Mordecai Meirowitz, an Israeli postmaster and"
            " telecommunications expert. A classic code-breaking game."
        ),
    }

    content_f = tk.Frame(self, bg="#2c3e50")
    content_f.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    list_frame = tk.Frame(content_f, bg="#2c3e50")
    list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

    self.history_list = tk.Listbox(
        list_frame,
        font=("Arial", 11, "bold"),
        bg="#1e272e",
        fg="white",
        selectbackground="#0984e3",
        width=20,
    )
    self.history_list.pack(fill=tk.BOTH, expand=True)

    for g in self.game_histories.keys():
      self.history_list.insert(tk.END, g)

    self.history_list.bind("<<ListboxSelect>>", self.on_history_select)

    display_frame = tk.Frame(content_f, bg="#1e272e", bd=2, relief="solid")
    display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

    self.history_title = tk.Label(
        display_frame,
        text="Select a game to read its history",
        font=("Arial", 12, "bold"),
        bg="#1e272e",
        fg="#00d8d6",
    )
    self.history_title.pack(pady=10)

    self.history_text = tk.Text(
        display_frame,
        font=("Arial", 11),
        bg="#1e272e",
        fg="white",
        wrap=tk.WORD,
        bd=0,
    )
    self.history_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

  def on_history_select(self, event):
    selection = self.history_list.curselection()
    if selection:
      game_name = self.history_list.get(selection[0])
      history_info = self.game_histories[game_name]

      self.history_title.config(text=f"History of {game_name}")
      self.history_text.delete("1.0", tk.END)
      self.history_text.insert(tk.END, history_info)
