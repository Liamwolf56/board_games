import tkinter as tk
from tkinter import messagebox

class XiangqiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Xiangqi (Chinese Chess)")
        self.root.geometry("650x750")
        self.root.config(bg="#2c3e50")

        title_label = tk.Label(root, text="🏮 Xiangqi (Chinese Chess - 10x9)", font=("Arial", 16, "bold"), bg="#2c3e50", fg="white")
        title_label.pack(pady=10)

        self.board_frame = tk.Frame(root, bg="#d35400", bd=3, relief="solid")
        self.board_frame.pack(pady=10)

        self.buttons = {}
        self.create_board()

    def create_board(self):
        # 10x9 Xiangqi grid setup (R=Chariot, H=Horse, E=Elephant, A=Advisor, G=General, C=Cannon, S=Soldier)
        setup = [
            ["R", "H", "E", "A", "G", "A", "E", "H", "R"],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", "C", ".", ".", ".", ".", ".", "C", "."],
            ["S", ".", "S", ".", "S", ".", "S", ".", "S"],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["s", ".", "s", ".", "s", ".", "s", ".", "s"],
            [".", "c", ".", ".", ".", ".", ".", "c", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["r", "h", "e", "a", "g", "a", "e", "h", "r"]
        ]

        for r in range(10):
            for c in range(9):
                bg_color = "#f39c12" if (r + c) % 2 == 0 else "#e67e22"
                btn = tk.Button(
                    self.board_frame,
                    text=setup[r][c] if setup[r][c] != "." else "",
                    font=("Arial", 13, "bold"),
                    width=3,
                    height=1,
                    bg=bg_color,
                    activebackground="#d35400",
                    command=lambda row=r, col=c: messagebox.showinfo("Xiangqi", f"Clicked Xiangqi square ({row}, {col})")
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[(r, c)] = btn

if __name__ == "__main__":
    root = tk.Tk()
    app = XiangqiGUI(root)
    root.mainloop()
