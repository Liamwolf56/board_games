import chess
import tkinter as tk
from tkinter import messagebox


class ChessGUI:

  def __init__(self, root):
    self.root = root
    self.root.title("WSL Python Chess")
    self.board = chess.Board()

    self.selected_square = None
    self.buttons = {}

    # Unicode mapping for chess pieces
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

    # Create UI frame for board
    self.canvas_frame = tk.Frame(root)
    self.canvas_frame.pack(pady=10)

    self.create_board_ui()
    self.update_board_ui()

  def create_board_ui(self):
    for r in range(8):
      for c in range(8):
        board_row = 7 - r
        board_col = c

        bg_color = "#f0d9b5" if (r + c) % 2 == 0 else "#b58863"

        btn = tk.Button(
            self.canvas_frame,
            text="",
            font=("Arial", 32),
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

      # Auto promote pawn to queen
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
      else:
        piece = self.board.piece_at(square_index)
        if piece and piece.color == self.board.turn:
          self.selected_square = square_index
          self.highlight_squares(square_index)
        else:
          self.selected_square = None
          self.update_board_ui()

  def highlight_squares(self, square):
    self.update_board_ui()
    r = chess.square_rank(square)
    c = chess.square_file(square)
    self.buttons[(r, c)].config(bg="#7b68ee")  # Slate blue for selected

    for move in self.board.legal_moves:
      if move.from_square == square:
        tr = chess.square_rank(move.to_square)
        tc = chess.square_file(move.to_square)
        self.buttons[(tr, tc)].config(bg="#a9dfbf")  # Light green for legal moves

  def update_board_ui(self):
    for r in range(8):
      for c in range(8):
        square_index = chess.square(c, r)
        piece = self.board.piece_at(square_index)

        bg_color = "#f0d9b5" if (r + c) % 2 != 0 else "#b58863"

        text = ""
        if piece:
          text = self.pieces_unicode.get(piece.symbol(), "")

        self.buttons[(r, c)].config(text=text, bg=bg_color)

  def show_game_over(self):
    result = self.board.result()
    messagebox.showinfo("Game Over", f"Game Over! Result: {result}")
    self.root.quit()


if __name__ == "__main__":
  root = tk.Tk()
  app = ChessGUI(root)
  root.mainloop()
