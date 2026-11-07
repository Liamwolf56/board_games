import os
import random
import sys
import tkinter as tk
from tkinter import messagebox

# Direct Python to load python-chess from venv site-packages to avoid local directory shadowing
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
venv_site_packages = os.path.join(
    base_dir,
    "venv",
    "lib",
    f"python{sys.version_info.major}.{sys.version_info.minor}",
    "site-packages",
)
if os.path.exists(venv_site_packages) and venv_site_packages not in sys.path:
  sys.path.insert(0, venv_site_packages)

try:
  import chess
except ImportError:
  messagebox.showerror(
      "Missing Package",
      "The 'python-chess' library was not found in venv.\nPlease run:"
      " venv/bin/pip install python-chess",
  )
  sys.exit(1)


class ChessPuzzlesModeFrame(tk.Frame):

  def __init__(self, parent, hub_app):
    super().__init__(parent, bg="#1e272e")
    self.hub_app = hub_app

    self.puzzles = [
        # Original 4 Puzzles
        {
            "title": "Puzzle 1: Back-Rank Mate (Mate in 1)",
            "fen": "6k1/5ppp/8/8/8/8/8/4R1K1 w - - 0 1",
            "solution": ["e1e8"],
            "description": (
                "White to move. Deliver checkmate on the back rank in 1 move!"
            ),
        },
        {
            "title": "Puzzle 2: Scholar's Mate Threat (Mate in 1)",
            "fen": "r1bqkb1r/pppp1ppp/2n5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 1",
            "solution": ["f3f7"],
            "description": (
                "White to move. Exploit the weak f7 square for Scholar's Mate!"
            ),
        },
        {
            "title": "Puzzle 3: Knight Fork Check (Tactical Advantage)",
            "fen": "r1bqk2r/pppp1ppp/2n5/4p3/2B1n3/5N2/PPPP1PPP/R1BQK2R w KQkq - 0 1",
            "solution": ["c4f7"],
            "description": "White to move. Strike the opponent with a quick check!",
        },
        {
            "title": "Puzzle 4: Smothered Mate Threat (Mate in 1)",
            "fen": "6rk/5Npp/8/8/8/8/8/6K1 w - - 0 1",
            "solution": ["f7h6"],
            "description": (
                "White to move. Execute the classic Smothered Mate with the"
                " Knight!"
            ),
        },
        # 26 New Puzzles
        {
            "title": "Puzzle 5: Queen Diagonal Mate (Mate in 1)",
            "fen": "6k1/5p1p/6p1/8/8/8/5Q2/6K1 w - - 0 1",
            "solution": ["f2f7"],
            "description": "White to move. Corner the black King on f7!",
        },
        {
            "title": "Puzzle 6: Rook Corridor Mate (Mate in 1)",
            "fen": "7k/R7/8/8/8/8/8/R5K1 w - - 0 1",
            "solution": ["a1a8"],
            "description": (
                "White to move. Sweep the 8th rank with the second Rook!"
            ),
        },
        {
            "title": "Puzzle 7: Anastasia's Mate (Mate in 1)",
            "fen": "5r1k/1R6/8/8/8/8/4N3/6RK w - - 0 1",
            "solution": ["g1g8"],
            "description": (
                "White to move. Use the Rook to seal checkmate on g8!"
            ),
        },
        {
            "title": "Puzzle 8: Arabian Mate (Mate in 1)",
            "fen": "7k/5R2/5N2/8/8/8/8/6K1 w - - 0 1",
            "solution": ["f7h7"],
            "description": (
                "White to move. Combine Knight and Rook for Arabian Mate on"
                " h7!"
            ),
        },
        {
            "title": "Puzzle 9: Boden's Mate (Mate in 1)",
            "fen": "2kr4/8/8/2B5/1B6/8/8/6K1 w - - 0 1",
            "solution": ["c5a7"],
            "description": (
                "White to move. Criss-cross Bishops for checkmate!"
            ),
        },
        {
            "title": "Puzzle 10: Epaulette Mate (Mate in 1)",
            "fen": "3rkr2/8/8/4Q3/8/8/8/6K1 w - - 0 1",
            "solution": ["e5e6"],
            "description": (
                "White to move. Trapped between Rooks, checkmate the King on"
                " e6!"
            ),
        },
        {
            "title": "Puzzle 11: Opera Mate Pattern (Mate in 1)",
            "fen": "4k3/8/8/8/8/8/4B3/3R3K w - - 0 1",
            "solution": ["d1d8"],
            "description": (
                "White to move. Deliver checkmate with the Rook guarded by the"
                " Bishop!"
            ),
        },
        {
            "title": "Puzzle 12: Swallow's Tail Mate (Mate in 1)",
            "fen": "3r1r2/2k5/8/3Q4/8/8/8/6K1 w - - 0 1",
            "solution": ["d5c5"],
            "description": "White to move. Pin the King against its own Rooks!",
        },
        {
            "title": "Puzzle 13: Pawn Push Mate (Mate in 1)",
            "fen": "k7/1P6/1K6/8/8/8/8/8 w - - 0 1",
            "solution": ["b7b8q"],
            "description": "White to move. Promote to Queen for instant checkmate!",
        },
        {
            "title": "Puzzle 14: Blackburne's Mate (Mate in 1)",
            "fen": "5rk1/5p1p/8/2B5/1B6/8/5N2/6K1 w - - 0 1",
            "solution": ["c5f8"],
            "description": (
                "White to move. Snag the defender on f8 with the Bishop!"
            ),
        },
        {
            "title": "Puzzle 15: Damiano's Mate (Mate in 1)",
            "fen": "6rk/6p1/8/7Q/8/8/8/6K1 w - - 0 1",
            "solution": ["h5h7"],
            "description": "White to move. Strike on h7 with Queen power!",
        },
        {
            "title": "Puzzle 16: Greco's Mate (Mate in 1)",
            "fen": "6rk/7p/8/8/8/8/8/6RQ w - - 0 1",
            "solution": ["h1h7"],
            "description": "White to move. Sac or strike directly on h7!",
        },
        {
            "title": "Puzzle 17: Hook Mate (Mate in 1)",
            "fen": "5k2/5P2/5K1R/8/8/8/8/8 w - - 0 1",
            "solution": ["h6h8"],
            "description": (
                "White to move. Deliver back-rank Hook Mate with the Rook!"
            ),
        },
        {
            "title": "Puzzle 18: Kill Box Mate (Mate in 1)",
            "fen": "3k4/3R4/3Q4/8/8/8/8/6K1 w - - 0 1",
            "solution": ["d6e7"],
            "description": "White to move. Lock the King in the kill box on e7!",
        },
        {
            "title": "Puzzle 19: Lawn Mower Mate (Mate in 1)",
            "fen": "k7/8/1R6/8/8/8/8/1R4K1 w - - 0 1",
            "solution": ["b1a1"],
            "description": (
                "White to move. Mow down the a-file with the second Rook!"
            ),
        },
        {
            "title": "Puzzle 20: Lolli's Mate (Mate in 1)",
            "fen": "6rk/5p1p/5P2/8/8/8/6Q1/6K1 w - - 0 1",
            "solution": ["g2g7"],
            "description": "White to move. Advance the Queen supported by the pawn!",
        },
        {
            "title": "Puzzle 21: Max Lange's Mate (Mate in 1)",
            "fen": "5rk1/5ppp/8/8/2B5/8/5Q2/6K1 w - - 0 1",
            "solution": ["f2f7"],
            "description": "White to move. Battery attack on f7!",
        },
        {
            "title": "Puzzle 22: Triangle Mate (Mate in 1)",
            "fen": "k7/1R6/Q7/8/8/8/8/6K1 w - - 0 1",
            "solution": ["a6a7"],
            "description": (
                "White to move. Seal the triangular corner trap on a7!"
            ),
        },
        {
            "title": "Puzzle 23: Corner Trap (Mate in 1)",
            "fen": "k7/2K5/8/8/8/8/8/1R6 w - - 0 1",
            "solution": ["b1a1"],
            "description": "White to move. Slide Rook to a1 for corner checkmate!",
        },
        {
            "title": "Puzzle 24: Corridor Trap (Mate in 1)",
            "fen": "k1K5/8/8/8/8/8/8/7R w - - 0 1",
            "solution": ["h1a1"],
            "description": "White to move. Rook to a1 down the open file!",
        },
        {
            "title": "Puzzle 25: Knight Jump Pin (Mate in 1)",
            "fen": "k7/2N5/1K6/8/8/8/8/8 w - - 0 1",
            "solution": ["c7a6"],
            "description": (
                "White to move. Reposition Knight to a6 for smother check!"
            ),
        },
        {
            "title": "Puzzle 26: Bishop Snipe (Mate in 1)",
            "fen": "k7/8/1K6/8/8/8/2B5/8 w - - 0 1",
            "solution": ["c2be4"],
            "description": (
                "White to move. Slice across the diagonal to e4 for mate!"
            ),
        },
        {
            "title": "Puzzle 27: Double Rook Sweep (Mate in 1)",
            "fen": "k7/8/1K6/8/8/8/1R6/2R5 w - - 0 1",
            "solution": ["c1c8"],
            "description": "White to move. Send the back Rook to c8!",
        },
        {
            "title": "Puzzle 28: Queen Overload (Mate in 1)",
            "fen": "k7/8/1K6/8/8/8/8/1Q6 w - - 0 1",
            "solution": ["b1a1"],
            "description": "White to move. Queen to a1 delivers fatal check!",
        },
        {
            "title": "Puzzle 29: Pawn Promotion Knight Check (Mate in 1)",
            "fen": "k7/2P5/1K6/8/8/8/8/8 w - - 0 1",
            "solution": ["c7c8q"],
            "description": "White to move. Promote pawn on c8 to Queen!",
        },
        {
            "title": "Puzzle 30: Grandmaster Finale (Mate in 1)",
            "fen": "k7/1R6/2K5/8/8/8/8/8 w - - 0 1",
            "solution": ["b7b8"],
            "description": (
                "White to move. Conclude with a Rook sacrifice on b8!"
            ),
        },
    ]

    self.current_puzzle_idx = 0
    self.board = chess.Board()
    self.selected_square = None

    self.symbols = {
        "P": "♙",
        "N": "♘",
        "B": "♗",
        "R": "♖",
        "Q": "♕",
        "K": "♔",
        "p": "♟",
        "n": "♞",
        "b": "♝",
        "r": "♜",
        "q": "♛",
        "k": "♚",
    }

    # Top Navigation Bar
    top_frame = tk.Frame(self, bg="#1e272e")
    top_frame.pack(fill=tk.X, padx=10, pady=10)

    self.puzzle_label = tk.Label(
        top_frame,
        text="",
        font=("Arial", 11, "bold"),
        bg="#1e272e",
        fg="#ffdd59",
    )
    self.puzzle_label.pack(side=tk.LEFT)

    tk.Button(
        top_frame,
        text="🎲 Random Puzzle",
        bg="#9b59b6",
        fg="white",
        font=("Arial", 9, "bold"),
        command=self.randomize_puzzle,
    ).pack(side=tk.RIGHT, padx=5)

    tk.Button(
        top_frame,
        text="Reset Puzzle",
        bg="#e74c3c",
        fg="white",
        font=("Arial", 9, "bold"),
        command=self.reset_current_puzzle,
    ).pack(side=tk.RIGHT, padx=5)

    tk.Button(
        top_frame,
        text="Next Puzzle ➡️",
        bg="#0984e3",
        fg="white",
        font=("Arial", 9, "bold"),
        command=self.next_puzzle,
    ).pack(side=tk.RIGHT, padx=5)

    # Goal Banner
    self.desc_label = tk.Label(
        self, text="", font=("Arial", 11), bg="#2c3e50", fg="#00d8d6", pady=5
    )
    self.desc_label.pack(fill=tk.X, padx=20, pady=5)

    # Chessboard Outer Frame
    board_outer = tk.Frame(self, bg="#2c3e50", bd=4, relief="solid")
    board_outer.pack(pady=10)

    self.squares = {}
    for r in range(8):
      for c in range(8):
        sq_idx = chess.square(c, 7 - r)
        bg_color = "#f0d9b5" if (r + c) % 2 == 0 else "#b58863"

        btn = tk.Button(
            board_outer,
            text="",
            font=("Arial", 22, "bold"),
            width=2,
            height=1,
            bg=bg_color,
            fg="#2c3e50",
            command=lambda s=sq_idx: self.on_square_click(s),
        )
        btn.grid(row=r, column=c)
        self.squares[sq_idx] = btn

    self.load_puzzle(0)

  def load_puzzle(self, idx):
    self.current_puzzle_idx = idx % len(self.puzzles)
    puzzle = self.puzzles[self.current_puzzle_idx]

    self.board = chess.Board(puzzle["fen"])
    self.selected_square = None

    self.puzzle_label.config(text=f"[{self.current_puzzle_idx + 1}/30] {puzzle['title']}")
    self.desc_label.config(text=f"🎯 Goal: {puzzle['description']}")

    self.update_board_ui()

  def reset_current_puzzle(self):
    self.load_puzzle(self.current_puzzle_idx)

  def next_puzzle(self):
    self.load_puzzle(self.current_puzzle_idx + 1)

  def randomize_puzzle(self):
    if len(self.puzzles) <= 1:
      return

    new_idx = self.current_puzzle_idx
    while new_idx == self.current_puzzle_idx:
      new_idx = random.randint(0, len(self.puzzles) - 1)

    self.load_puzzle(new_idx)

  def on_square_click(self, sq):
    piece = self.board.piece_at(sq)

    if self.selected_square is None:
      if piece and piece.color == self.board.turn:
        self.selected_square = sq
        self.highlight_squares(sq)
    else:
      move = chess.Move(self.selected_square, sq)

      if (
          self.board.piece_at(self.selected_square)
          and self.board.piece_at(self.selected_square).piece_type
          == chess.PAWN
      ):
        if chess.square_rank(sq) in [0, 7]:
          move = chess.Move(self.selected_square, sq, promotion=chess.QUEEN)

      if move in self.board.legal_moves:
        puzzle = self.puzzles[self.current_puzzle_idx]
        expected_move_uci = puzzle["solution"][0]

        if move.uci() == expected_move_uci:
          self.board.push(move)
          self.selected_square = None
          self.update_board_ui()

          messagebox.showinfo(
              "Puzzle Solved! 🎉",
              "BRILLIANT MOVE! You solved the puzzle perfectly!",
          )
        else:
          messagebox.showwarning(
              "Incorrect Move ❌",
              "That is a legal move, but not the winning tactical solution."
              " Try again!",
          )
          self.reset_current_puzzle()
      else:
        if piece and piece.color == self.board.turn:
          self.selected_square = sq
          self.highlight_squares(sq)
        else:
          self.selected_square = None
          self.update_board_ui()

  def highlight_squares(self, sq):
    self.update_board_ui()
    self.squares[sq].config(bg="#7b68ee")
    for move in self.board.legal_moves:
      if move.from_square == sq:
        self.squares[move.to_square].config(bg="#85bb65")

  def update_board_ui(self):
    for sq, btn in self.squares.items():
      r, c = chess.square_rank(sq), chess.square_file(sq)
      bg_color = "#f0d9b5" if (r + c) % 2 != 0 else "#b58863"
      btn.config(bg=bg_color)

      piece = self.board.piece_at(sq)
      if piece:
        symbol = self.symbols.get(piece.symbol(), "")
        fg_col = "#ffffff" if piece.color == chess.WHITE else "#000000"
        btn.config(text=symbol, fg=fg_col)
      else:
        btn.config(text="")
