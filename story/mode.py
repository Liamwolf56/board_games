import tkinter as tk


class StoryModeFrame(tk.Frame):

  def __init__(self, parent, hub_app):
    super().__init__(parent, bg="#2c3e50", bd=2, relief="solid")
    self.hub_app = hub_app

    tk.Label(
        self,
        text="📖 STORY MODE CAMPAIGN",
        font=("Arial", 14, "bold"),
        bg="#2c3e50",
        fg="#ffdd59",
    ).pack(pady=20)

    tk.Label(
        self,
        text=(
            "Progression Journey Across the Arcade Realm\n(Folder:"
            " story/mode.py)"
        ),
        font=("Arial", 12),
        bg="#2c3e50",
        fg="white",
    ).pack(pady=40)
