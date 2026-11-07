import sys
import tkinter as tk
from tkinter import messagebox
import chess


class ChessApp:

  def __init__(self, root, mode="PvP"):
    self.root = root
    self.root.title(f"Chess - Mode: {mode}")
    self.root.geometry("650x780")
    self.root.config(bg="#2c3e50")

    self.board = chess.Board()
    self.mode = mode
    self.selected_square = None
    self.buttons = {}

    # Timer variables (in seconds)
    self.white_time = 300  # 5 minutes
    self.black_time = 300
    self.timer_running = True

    # Header frame for Instructions and Timer
    top_frame = tk.Frame(root, bg="#2c3e50")
    top_frame.pack(fill=tk.X, padx=10, pady=10)

    rules_btn = tk.Button(
        top_frame,
        text="📖 How to Play Chess",
        bg="#f39c12",
        fg="white",
        font=("Arial", 10, "bold"),
        command=self.show_rules,
    )
    rules_btn.pack(side=tk.LEFT)

    self.timer_label = tk.Label(
        top_frame,
        text="White: 05:00 | Black: 05:00",
        font=("Arial", 11, "bold"),
        bg="#2c3e50",
        fg="white",
    )
    self.timer_label.pack(side=tk.RIGHT)

    # Board Frame
    self.canvas_frame = tk.Frame(root, bg="#34495e", bd=3, relief="solid")
    self.canvas_frame.pack(pady=10)

    self.pieces_unicode = {
        "P": "♙",
        "R": "♖",
        "N": "♘",
        "B": "♗",
        "Q": "♕",
        "K": "♔",
        "p": "♟",
        "r": "♜",
        "n": "♞",
        "b": "♝",
        "q": "♛",
        "k": "♚",
    }

    self.create_board_ui()
    self.update_board_ui()
    self.update_timer()

  def show_rules(self):
    rules = (
        "CHESS RULES FOR BEGINNERS:\n\n"
        "• Objective: Trap the opponent's King ('Checkmate').\n"
        "• Pawns (♙): Move forward 1 square (or 2 on first move), capture diagonally.\n"
        "• Knights (♘): Move in an L-shape and can jump over pieces.\n"
        "• Bishops (♗): Move diagonally any number of squares.\n"
        "• Rooks (♖): Move horizontally or vertically any number of squares.\n"
        "• Queen (♕): Combines Rook and Bishop powers.\n"
        "• King (♔): Moves 1 square in any direction."
    )
    messagebox.showinfo("How to Play - Chess", rules)

  def create_board_ui(self):
    for r in range(8):
      for c in range(8):
        board_row = 7 - r
        board_col = c
        bg_color = "#f0d9b5" if (r + c) % 2 == 0 else "#b58863"

        btn = tk.Button(
            self.canvas_frame,
            text="",
            font=("Arial", 28),
            width=2,
            height=1,
            bg=bg_color,
            activebackground=bg_color,
            command=lambda row=board_row, col=board_col: self.square_clicked(
                row, col
            ),
        )
        btn.grid(row=r, column=c)
        self.buttons[(board_row, board_col)] = btn

  def square_clicked(self, row, col):
    square_index = chess.square(col, row)

    if self.selected_square is None:
      piece = self.board.piece_at(square_index)
      if piece and piece.color == self.board.turn:
        self.selected_square = square_index
        self.highlight_squares(square_index)
    else:
      move = chess.Move(self.selected_square, square_index)
      if (
          self.board.piece_at(self.selected_square).piece_type == chess.PAWN
          and (row == 7 or row == 0)
      ):
        move = chess.Move(self.selected_square, square_index, promotion=chess.QUEEN)

      if move in self.board.legal_moves:
        self.board.push(move)
        self.selected_square = None
        self.update_board_ui()

        if self.board.is_game_over():
          self.show_game_over()
        elif self.mode == "PvAI" and not self.board.is_game_over():
          self.make_ai_move()
      else:
        piece = self.board.piece_at(square_index)
        if piece and piece.color == self.board.turn:
          self.selected_square = square_index
          self.highlight_squares(square_index)
        else:
          self.selected_square = None
          self.update_board_ui()

  def make_ai_move(self):
    # Simple random AI logic for beginner friend
    import random

    legal_moves = list(self.board.legal_moves)
    if legal_moves:
      ai_move = random.choice(legal_moves)
      self.board.push(ai_move)
      self.update_board_ui()
      if self.board.is_game_over():
        self.show_game_over()

  def highlight_squares(self, square):
    self.update_board_ui()
    r = chess.square_rank(square)
    c = chess.square_file(square)
    self.buttons[(r, c)].config(bg="#7b68ee")
    for move in self.board.legal_moves:
      if move.from_square == square:
        tr = chess.square_rank(move.to_square)
        tc = chess.square_file(move.to_square)
        self.buttons[(tr, tc)].config(bg="#a9dfbf")

  def update_board_ui(self):
    for r in range(8):
      for c in range(8):
        square_index = chess.square(c, r)
        piece = self.board.piece_at(square_index)
        bg_color = "#f0d9b5" if (r + c) % 2 != 0 else "#b58863"
        text = self.pieces_unicode.get(piece.symbol(), "") if piece else ""
        self.buttons[(r, c)].config(text=text, bg=bg_color)

  def update_timer(self):
    if self.timer_running and not self.board.is_game_over():
      if self.board.turn == chess.WHITE:
        if self.white_time > 0:
          self.white_time -= 1
      else:
        if self.black_time > 0:
          self.black_time -= 1

      w_min, w_sec = divmod(self.white_time, 60)
      b_min, b_sec = divmod(self.black_time, 60)
      self.timer_label.config(
          text=f"White: {w_min:02d}:{w_sec:02d} | Black:"
          f" {b_min:02d}:{b_sec:02d}"
      )

    self.root.after(1000, self.update_timer)

  def show_game_over(self):
    self.timer_running = False
    result = self.board.result()
    messagebox.showinfo("Game Over", f"Game Over! Result: {result}")


if __name__ == "__main__":
  mode = sys.argv[1] if len(sys.argv) > 1 else "PvP"
  root = tk.Tk()
  app = ChessApp(root, mode)
  root.mainloop()
