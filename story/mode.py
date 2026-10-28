import json
import os
import random
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog

# Import individual King modules from their subfolders
from story.animal_upon_animal.mode import KING_DATA as k_animal
from story.battleship.mode import KING_DATA as k_battleship
from story.checkers.mode import KING_DATA as k_checkers
from story.chess.mode import KING_DATA as k_chess
from story.chaturanga.mode import KING_DATA as k_chaturanga
from story.connect4.mode import KING_DATA as k_connect4
from story.mastermind.mode import KING_DATA as k_mastermind
from story.monza.mode import KING_DATA as k_monza
from story.otrio.mode import KING_DATA as k_otrio
from story.reversi.mode import KING_DATA as k_reversi
from story.sequence_for_kids.mode import KING_DATA as k_sequence
from story.shogi.mode import KING_DATA as k_shogi
from story.tictactoe.mode import KING_DATA as k_tictactoe
from story.xiangqi.mode import KING_DATA as k_xiangqi
from story.yahtzee.mode import KING_DATA as k_yahtzee

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class StoryModeFrame(tk.Frame):

  def __init__(self, parent, hub_app):
    super().__init__(parent, bg="#1e272e")
    self.hub_app = hub_app
    self.save_file = os.path.join(base_dir, "story", "progress.json")

    # Map all imported modules into master roster dictionary
    self.master_kings = {
        k["game"]: k
        for k in [
            k_tictactoe,
            k_monza,
            k_animal,
            k_sequence,
            k_otrio,
            k_battleship,
            k_mastermind,
            k_yahtzee,
            k_connect4,
            k_reversi,
            k_checkers,
            k_chaturanga,
            k_xiangqi,
            k_shogi,
            k_chess,
        ]
    }

    self.player_name = "Challenger"
    self.campaign_order = []
    self.current_stage_idx = 0
    self.high_score = 0

    # Header Banner
    tk.Label(
        self,
        text="👑 ROGUELIKE STORY MODE: REALM OF 15 KINGS 👑",
        font=("Arial", 14, "bold"),
        bg="#1e272e",
        fg="#ffdd59",
    ).pack(pady=10)

    # Score & Player Info Bar
    self.info_bar = tk.Label(
        self,
        text="",
        font=("Arial", 11, "bold"),
        bg="#2c3e50",
        fg="#00d8d6",
        pady=5,
    )
    self.info_bar.pack(fill=tk.X, padx=20, pady=5)

    # Main layout
    main_frame = tk.Frame(self, bg="#1e272e")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Left: Map Listbox
    left_frame = tk.Frame(main_frame, bg="#2c3e50", width=250)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

    tk.Label(
        left_frame,
        text="Campaign Path:",
        font=("Arial", 10, "bold"),
        bg="#2c3e50",
        fg="white",
    ).pack(pady=5)

    self.stage_listbox = tk.Listbox(
        left_frame,
        font=("Arial", 10, "bold"),
        bg="#34495e",
        fg="white",
        width=26,
        height=18,
        selectbackground="#0984e3",
    )
    self.stage_listbox.pack(padx=5, pady=5, fill=tk.Y, expand=True)

    tk.Button(
        left_frame,
        text="🔄 Start Fresh Run",
        font=("Arial", 9, "bold"),
        bg="#d35400",
        fg="white",
        command=self.prompt_new_run,
    ).pack(pady=5)

    # Right: King Details & Action Button
    right_frame = tk.Frame(main_frame, bg="#2c3e50", bd=2, relief="solid")
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

    self.boss_title_label = tk.Label(
        right_frame,
        text="",
        font=("Arial", 13, "bold"),
        bg="#2c3e50",
        fg="#ffdd59",
    )
    self.boss_title_label.pack(pady=10)

    self.dialogue_box = tk.Text(
        right_frame,
        wrap=tk.WORD,
        font=("Arial", 11),
        bg="#ecf0f1",
        fg="#2c3e50",
        height=12,
        padx=15,
        pady=15,
    )
    self.dialogue_box.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    btn_frame = tk.Frame(right_frame, bg="#2c3e50")
    btn_frame.pack(pady=15)

    tk.Button(
        btn_frame,
        text="⚔️ Challenge King in Combat",
        font=("Arial", 12, "bold"),
        bg="#e74c3c",
        fg="white",
        padx=15,
        pady=8,
        command=self.challenge_king,
    ).pack(pady=5)

    self.after(100, self.load_or_generate_campaign)

  def load_or_generate_campaign(self):
    if os.path.exists(self.save_file):
      try:
        with open(self.save_file, "r") as f:
          data = json.load(f)
          self.player_name = data.get("player_name", "Challenger")
          self.campaign_order = data.get("campaign_order", [])
          self.current_stage_idx = data.get("current_stage_idx", 0)
          self.high_score = data.get("high_score", 0)
          if len(self.campaign_order) == 15:
            self.refresh_ui()
            return
      except Exception:
        pass

    self.create_new_campaign()

  def create_new_campaign(self):
    name = simpledialog.askstring(
        "New Strategist",
        "Enter your Player Name for this Campaign:",
        initialvalue=self.player_name,
    )
    if name and name.strip():
      self.player_name = name.strip()

    # FULL 15-KING CAMPAIGN MODE
    other_games = [g for g in self.master_kings.keys() if g != "Chess"]
    random.shuffle(other_games)
    self.campaign_order = other_games + ["Chess"]
    self.current_stage_idx = 0
    self.save_progress()
    self.refresh_ui()

  def save_progress(self):
    os.makedirs(os.path.dirname(self.save_file), exist_ok=True)
    with open(self.save_file, "w") as f:
      json.dump(
          {
              "player_name": self.player_name,
              "campaign_order": self.campaign_order,
              "current_stage_idx": self.current_stage_idx,
              "high_score": max(self.high_score, self.current_stage_idx),
          },
          f,
      )

  def prompt_new_run(self):
    if messagebox.askyesno(
        "Reset Campaign",
        "Start a brand new campaign run? Current progress will be reset!",
    ):
      self.create_new_campaign()

  def refresh_ui(self):
    total_stages = len(self.campaign_order)
    self.info_bar.config(
        text=(
            f"👤 Player: {self.player_name}   |   ⚔️ Kings Beat:"
            f" {self.current_stage_idx}/{total_stages}   |   🏆 Record Score:"
            f" {max(self.high_score, self.current_stage_idx)}"
        )
    )

    self.stage_listbox.delete(0, tk.END)
    for idx, game_name in enumerate(self.campaign_order):
      king = self.master_kings.get(game_name, {"title": game_name})
      if idx < self.current_stage_idx:
        status = "✅"
      elif idx == self.current_stage_idx:
        status = "⚔️"
      else:
        status = "🔒"

      stage_num = idx + 1
      label = (
          f"{status} Final Boss: {king.get('title', game_name)}"
          if game_name == "Chess"
          else f"{status} Stage {stage_num}: {game_name}"
      )
      self.stage_listbox.insert(tk.END, label)

    if self.campaign_order:
      self.stage_listbox.selection_set(
          min(self.current_stage_idx, len(self.campaign_order) - 1)
      )
      self.load_king_details(
          min(self.current_stage_idx, len(self.campaign_order) - 1)
      )

  def load_king_details(self, idx):
    if not self.campaign_order or idx >= len(self.campaign_order):
      return
    game_name = self.campaign_order[idx]
    king = self.master_kings.get(
        game_name, {"title": game_name, "intro": "Prepare yourself!"}
    )

    stage_str = (
        "FINAL BOSS" if game_name == "Chess" else f"Stage {idx + 1}"
    )
    self.boss_title_label.config(
        text=f"👑 {stage_str}: {king.get('title', game_name)} ({game_name})"
    )

    self.dialogue_box.config(state=tk.NORMAL)
    self.dialogue_box.delete("1.0", tk.END)

    self.dialogue_box.insert(
        tk.END,
        f"🗣️ KING'S BATTLE TAUNT:\n\"{king.get('intro', '')}\"\n\n",
        "taunt",
    )
    self.dialogue_box.insert(
        tk.END,
        "💡 Rule of the Realm:\nWhen you challenge this King, you must defeat"
        " them in combat. If you lose, your ironman run resets from Stage"
        " 1!\n",
        "rule",
    )

    self.dialogue_box.tag_config(
        "taunt", font=("Arial", 11, "bold"), foreground="#d35400"
    )
    self.dialogue_box.tag_config(
        "rule", font=("Arial", 10), foreground="#2c3e50"
    )
    self.dialogue_box.config(state=tk.DISABLED)

  def challenge_king(self):
    if not self.campaign_order or self.current_stage_idx >= len(
        self.campaign_order
    ):
      return
    game_name = self.campaign_order[self.current_stage_idx]

    folder_mapping = {
        "Tic-Tac-Toe": "tictactoe",
        "Monza": "monza",
        "Animal Upon Animal": "animal_upon_animal",
        "Sequence for Kids": "sequence_for_kids",
        "Otrio": "otrio",
        "Battleship": "battleship",
        "Mastermind": "mastermind",
        "Yahtzee": "yahtzee",
        "Connect 4": "connect4",
        "Reversi": "reversi",
        "Checkers": "checkers",
        "Chaturanga": "chaturanga",
        "Xiangqi": "xiangqi",
        "Shogi": "shogi",
        "Chess": "chess",
    }
    folder_name = folder_mapping.get(
        game_name, game_name.lower().replace(" ", "_")
    )

    script_path = os.path.join(base_dir, "story", folder_name, "mode.py")

    if not os.path.exists(script_path):
      messagebox.showerror(
          "Error",
          f"Story Mode script for {game_name} not found at:\n{script_path}",
      )
      return

    venv_python = os.path.join(base_dir, "venv", "bin", "python3")
    python_executable = (
        venv_python if os.path.exists(venv_python) else sys.executable
    )

    proc = subprocess.Popen([python_executable, script_path])
    self.after(500, self.check_process_completion, proc)

  def check_process_completion(self, proc):
    if proc.poll() is None:
      self.after(500, self.check_process_completion, proc)
    else:
      old_idx = self.current_stage_idx
      self.load_or_generate_campaign()

      if self.current_stage_idx > old_idx and self.current_stage_idx < len(
          self.campaign_order
      ):
        next_game = self.campaign_order[self.current_stage_idx]
        king = self.master_kings.get(next_game, {})
        messagebox.showinfo(
            "NEXT STAGE! ⚔️",
            f"Advancing to Stage {self.current_stage_idx + 1}!\nFacing:"
            f" {king.get('title', next_game)}",
        )
        self.challenge_king()
