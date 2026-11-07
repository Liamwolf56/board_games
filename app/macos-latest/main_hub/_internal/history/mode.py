import tkinter as tk
from tkinter import ttk


class HistoryModeFrame(tk.Frame):

  def __init__(self, parent, hub_app):
    super().__init__(parent, bg="#1e272e")
    self.hub_app = hub_app

    # Header
    tk.Label(
        self,
        text="📜 Master Board Game Wiki & Encyclopedia",
        font=("Arial", 14, "bold"),
        bg="#1e272e",
        fg="#ffdd59",
    ).pack(pady=10)

    # Main layout (Listbox left, Wiki Viewer right)
    content_frame = tk.Frame(self, bg="#1e272e")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Left: Game Selector Listbox
    list_frame = tk.Frame(content_frame, bg="#2c3e50")
    list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

    tk.Label(
        list_frame,
        text="Select a Game:",
        font=("Arial", 10, "bold"),
        bg="#2c3e50",
        fg="white",
    ).pack(padx=5, pady=5)

    self.game_listbox = tk.Listbox(
        list_frame,
        font=("Arial", 10, "bold"),
        bg="#34495e",
        fg="white",
        width=22,
        height=22,
        selectbackground="#0984e3",
    )
    self.game_listbox.pack(padx=5, pady=5, fill=tk.Y, expand=True)
    self.game_listbox.bind("<<ListboxSelect>>", self.on_game_select)

    # Right: Text Viewer
    text_frame = tk.Frame(content_frame, bg="#2c3e50", bd=2, relief="solid")
    text_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

    self.wiki_text = tk.Text(
        text_frame,
        wrap=tk.WORD,
        font=("Arial", 10),
        bg="#ecf0f1",
        fg="#2c3e50",
        padx=15,
        pady=15,
    )
    self.wiki_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(
        text_frame, command=self.wiki_text.yview, bg="#ecf0f1"
    )
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    self.wiki_text.config(yscrollcommand=scrollbar.set)

    # Comprehensive Database
    self.games_data = self.build_wiki_database()

    for game_name in sorted(self.games_data.keys()):
      self.game_listbox.insert(tk.END, game_name)

    if self.game_listbox.size() > 0:
      self.game_listbox.selection_set(0)
      self.load_game_wiki(list(sorted(self.games_data.keys()))[0])

  def on_game_select(self, event):
    selection = self.game_listbox.curselection()
    if selection:
      game_name = self.game_listbox.get(selection[0])
      self.load_game_wiki(game_name)

  def load_game_wiki(self, game_name):
    data = self.games_data.get(game_name, {})

    self.wiki_text.config(state=tk.NORMAL)
    self.wiki_text.delete("1.0", tk.END)

    self.wiki_text.insert(
        tk.END, f"🌟 {game_name.upper()} ENCYCLOPEDIA 🌟\n\n", "header"
    )

    self.wiki_text.insert(tk.END, "🏛️ Historical Origin & Evolution\n", "subheader")
    self.wiki_text.insert(
        tk.END, f"{data.get('origin', 'Data pending.')}\n\n", "body"
    )

    self.wiki_text.insert(
        tk.END, "🗺️ How It Was Used Through the Ages\n", "subheader"
    )
    self.wiki_text.insert(
        tk.END, f"{data.get('used', 'Data pending.')}\n\n", "body"
    )

    self.wiki_text.insert(tk.END, "🌐 Modern Standing Today\n", "subheader")
    self.wiki_text.insert(
        tk.END, f"{data.get('today', 'Data pending.')}\n\n", "body"
    )

    self.wiki_text.insert(
        tk.END, "📖 How to Play & Piece Mechanics\n", "subheader"
    )
    self.wiki_text.insert(
        tk.END, f"{data.get('rules', 'Data pending.')}\n", "body"
    )

    self.wiki_text.tag_config(
        "header", font=("Arial", 14, "bold"), foreground="#2980b9"
    )
    self.wiki_text.tag_config(
        "subheader", font=("Arial", 11, "bold"), foreground="#d35400"
    )
    self.wiki_text.tag_config("body", font=("Arial", 10), foreground="#2c3e50")
    self.wiki_text.config(state=tk.DISABLED)

  def build_wiki_database(self):
    return {
        "Chess": {
            "origin": (
                "Chess evolved from Chaturanga in 6th-century India before"
                " spreading into Persia as Shatranj. Following the Islamic"
                " expansion, it entered Europe where its rules accelerated"
                " during the 15th century into modern chess."
            ),
            "used": (
                "Historically used by monarchs, scholars, and knights as a"
                " tool for studying military tactics, statecraft, and"
                " courtly honor. During the Cold War, it served as an"
                " intellectual battleground between superpowers."
            ),
            "today": (
                "Today, chess is a globally recognized sport overseen by FIDE,"
                " enjoyed by millions across online hubs, Grandmaster"
                " tournaments, and AI research programs."
            ),
            "rules": (
                "• Played on an 8x8 grid. Goal: Checkmate the opposing King.\n•"
                " King (♔): Moves 1 square any direction.\n• Queen (♕): Moves"
                " any vacant distance horizontally, vertically, or"
                " diagonally.\n• Rook (♖): Moves horizontally or vertically.\n•"
                " Bishop (♗): Moves diagonally.\n• Knight (♘): Moves in an"
                " L-shape and jumps over pieces.\n• Pawn (♙): Moves forward 1"
                " (or 2 on start) and captures diagonally."
            ),
        },
        "Shogi": {
            "origin": (
                "Shogi (Japanese Chess) evolved from Chaturanga via China and"
                " Korea, developing its signature 'drop rule' during Japan's"
                " Muromachi period (1336–1573)."
            ),
            "used": (
                "Utilized by samurai commanders and feudal lords to study"
                " tactical adaptability, resource recycling, and field"
                " logistics."
            ),
            "today": (
                "Remains Japan's premier strategy tradition with professional"
                " Meijin title matches broadcast nationally."
            ),
            "rules": (
                "• Played on a 9x9 grid. Goal: Capture the enemy King.\n• Drop"
                " Rule: Captured enemy pieces are added to your hand and dropped"
                " onto empty squares as your own!\n• King (♔): Moves 1 square"
                " any direction.\n• Rook (♖): Moves in cardinal lines.\n• Bishop"
                " (♗): Moves diagonally.\n• Gold General (★): Moves 1 square in"
                " 6 directions.\n• Silver General (◆): Moves 1 square"
                " diagonally or 1 forward.\n• Knight (♘): Jumps 2 forward, 1"
                " sideways.\n• Lance (▲): Moves forward any distance.\n• Pawn"
                " (●): Moves and captures 1 square forward."
            ),
        },
        "Xiangqi": {
            "origin": (
                "Xiangqi (Chinese Chess) originated over 2,000 years ago during"
                " the Warring States period, modeling Chinese battlefields"
                " divided by the Yellow River."
            ),
            "used": (
                "Employed by Chinese generals and strategists to practice choke"
                " point defense, river crossings, and artillery positioning."
            ),
            "today": (
                "One of the world's most popular board games, played daily"
                " across public parks and competitive leagues in Asia."
            ),
            "rules": (
                "• Played on grid intersections (9x10) divided by a River and"
                " Palace. Goal: Trap the General.\n• General (♔): Confined to"
                " Palace; moves 1 step cardinally.\n• Advisors (★): Confined to"
                " Palace; move 1 step diagonally.\n• Elephants (♗): Move 2"
                " steps diagonally; cannot cross River.\n• Horses (♘): Move 1"
                " step cardinally, 1 step diagonally (can be blocked).\n•"
                " Chariots (♖): Move along lines like a Rook.\n• Cannons (◎):"
                " Move like a Chariot, but MUST jump a piece to capture.\n•"
                " Soldiers (●): Move 1 step forward; after crossing River, can"
                " also move sideways."
            ),
        },
        "Chaturanga": {
            "origin": (
                "The ancient 6th-century Indian game created during the Gupta"
                " Empire, serving as the common ancestor of Chess, Shogi, and"
                " Xiangqi."
            ),
            "used": (
                "Designed to simulate the four classical divisions of ancient"
                " Indian warfare: Infantry, Cavalry, Elephants, and Chariots."
            ),
            "today": (
                "Studied by gaming historians as the foundational milestone of"
                " all modern abstract strategy games."
            ),
            "rules": (
                "• Played on an uncheckered 8x8 Ashtāpada board. Goal:"
                " Decimate enemy forces or trap the King.\n• King (♔): Moves 1"
                " square any direction.\n• Counselor (♕): Ancestor of the Queen;"
                " moves 1 square diagonally.\n• Elephant (♗): Moves 2 squares"
                " diagonally, jumping over interjacent pieces.\n• Horse (♘):"
                " Moves identically to the modern Knight.\n• Chariot (♖): Moves"
                " identically to the modern Rook.\n• Pawn (♙): Moves 1 square"
                " forward, captures 1 square diagonally."
            ),
        },
        "Checkers": {
            "origin": (
                "Evolved from ancient Middle Eastern board games like Ur and"
                " Alquerque into modern Draughts in 12th-century France."
            ),
            "used": (
                "Used throughout history as a accessible exercise in diagonal"
                " spatial control and forced jump calculations."
            ),
            "today": (
                "Played worldwide in informal settings and high-level"
                " tournament championships featuring mathematical checkers"
                " engines."
            ),
            "rules": (
                "• Played on dark squares of an 8x8 grid. Goal: Capture all"
                " opponent pieces or block their moves.\n• Regular Pieces:"
                " Move 1 step diagonally forward. Capture by jumping over an"
                " enemy piece into an empty square.\n• Kings: Created when a"
                " piece reaches the far rank. Kings can move and jump both"
                " forward and backward!"
            ),
        },
        "Reversi": {
            "origin": (
                "Invented in Victorian England in 1883 by Lewis Waterman and"
                " John W. Mollett, later trademarked as Othello in Japan."
            ),
            "used": (
                "Leveraged as a tactical demonstration of sudden momentum"
                " flips and edge control in logical reasoning."
            ),
            "today": (
                "Features an international circuit with world championships"
                " adhering to the slogan: 'A minute to learn, a lifetime to"
                " master.'"
            ),
            "rules": (
                "• Played on an 8x8 board with 2-sided disks (Black/White)."
                " Goal: Own the most disks when the board fills.\n• Placement:"
                " Place a disk so that it traps 1 or more opponent disks"
                " between your new disk and an existing friendly disk in a"
                " straight line.\n• Flip: All trapped opponent disks flip to"
                " your color!"
            ),
        },
        "Connect 4": {
            "origin": (
                "Created by Howard Wexler and Ned Strongin, released"
                " commercially by Milton Bradley in 1974."
            ),
            "used": (
                "Popularized in education as a foundational game for teaching"
                " pattern recognition and vertical gravity tactics."
            ),
            "today": (
                "A staple family game mathematically solved as a first-player"
                " win under perfect play."
            ),
            "rules": (
                "• Played on a vertical 7-column, 6-row grid. Goal: Connect 4"
                " of your colored disks in a row.\n• Mechanics: Players alternate"
                " dropping disks down a chosen column. The disk falls to the"
                " lowest open row.\n• Win Condition: Form a line of 4 horizontal,"
                " vertical, or diagonal disks."
            ),
        },
        "Tic-Tac-Toe": {
            "origin": (
                "Traced back to ancient Egypt and Rome around 100 BC as 'Terni"
                " Lapilli' carved into marble counters."
            ),
            "used": (
                "Used across millennia as an introductory exercise in zero-sum"
                " game theory and grid strategy."
            ),
            "today": (
                "The world's most ubiquitous simple game, played everywhere as a"
                " quick pastime."
            ),
            "rules": (
                "• Played on a 3x3 grid. Goal: Align 3 of your symbols (X or"
                " O).\n• Rules: Players alternate placing marks in empty"
                " cells. First to get 3 in a row horizontally, vertically, or"
                " diagonally wins."
            ),
        },
        "Battleship": {
            "origin": (
                "Evolved from World War I French paper game 'L'Attaque' into"
                " the 1967 Milton Bradley plastic peg board."
            ),
            "used": (
                "Simulates naval radar scanning, hidden grid positioning, and"
                " target deduction."
            ),
            "today": (
                "A classic guessing strategy game adapted into digital,"
                " mobile, and arcade versions worldwide."
            ),
            "rules": (
                "• Played on twin 10x10 grids. Goal: Sink all 5 enemy ships.\n•"
                " Setup: Secretly arrange Carrier (5), Battleship (4), Cruiser"
                " (3), Submarine (3), and Destroyer (2).\n• Gameplay: Call out"
                " coordinate shots ('B-4'). Opponent responds 'Hit' or"
                " 'Miss'."
            ),
        },
        "Otrio": {
            "origin": (
                "Designed by Brady Peterson in 2015 as an elevated multi-tier"
                " extension of classic Tic-Tac-Toe."
            ),
            "used": (
                "Utilized in modern game design to demonstrate nested spatial"
                " dimensions and multi-front defense."
            ),
            "today": (
                "An award-winning strategy board game enjoyed in casual and"
                " competitive abstract strategy circles."
            ),
            "rules": (
                "• Played on a grid using 3 sizes of concentric rings (Large,"
                " Medium, Small).\n• Win Conditions:\n  1. Three of your same-size"
                " pieces in a row.\n  2. Three of your pieces in ascending or"
                " descending size order.\n  3. Three of your pieces nested inside"
                " the SAME space!"
            ),
        },
        "Sequence for Kids": {
            "origin": (
                "Developed as an early-childhood adaptation of the popular"
                " 1981 Sequence board game by Jax Ltd."
            ),
            "used": (
                "Used in primary education to foster animal visual matching,"
                " hand management, and early strategic planning."
            ),
            "today": (
                "A leading children's board game across schools and homes"
                " worldwide."
            ),
            "rules": (
                "• Played with animal cards and a matching board grid. Goal:"
                " Get 4 chips in a row.\n• Mechanics: Play an animal card from"
                " your hand and place a chip on the matching board space.\n•"
                " Special Cards: Dragon cards remove an opponent chip; Unicorn"
                " cards act as wild spaces!"
            ),
        },
        "Animal Upon Animal": {
            "origin": (
                "Designed by Klaus Miltenberger and published by HABA in 2005"
                " in Germany."
            ),
            "used": (
                "Promotes fine motor skills, structural balance inspection, and"
                " risk mitigation."
            ),
            "today": (
                "Widely considered one of the benchmark physical dexterity"
                " games in modern tabletop history."
            ),
            "rules": (
                "• Played with 29 wooden animals. Goal: Be the first player to"
                " place all your animals onto the shared stack.\n• Mechanics:"
                " Roll the die to determine how many animals to stack on top of"
                " the central Crocodile base. If any drop, you must take them"
                " into your supply!"
            ),
        },
        "Monza": {
            "origin": (
                "Created by Jürgen P.K. Grunau for HABA in 2000, named after"
                " the famous Italian Grand Prix circuit."
            ),
            "used": (
                "Teaches children multi-step combinatorial thinking and color"
                " sequence planning."
            ),
            "today": (
                "A world-renowned educational racing game praised for replacing"
                " pure luck with tactical choices."
            ),
            "rules": (
                "• Played on a multi-lane color-coded track. Goal: Cross the"
                " finish line first.\n• Mechanics: Roll 6 colored dice."
                " Sequence your dice to move your race car step-by-step onto"
                " matching colored track squares."
            ),
        },
        "Yahtzee": {
            "origin": (
                "Invented in 1954 by a wealthy Canadian couple who played it on"
                " their yacht ('The Yacht Game'), acquired by E.S. Lowe in"
                " 1956."
            ),
            "used": (
                "Teaches mathematical probability, score-card optimization, and"
                " tactical risk management."
            ),
            "today": (
                "Sells over 50 million sets annually globally, remaining a"
                " cornerstone family classic."
            ),
            "rules": (
                "• Played with 5 dice and a scorecard. Goal: Score the highest"
                " points across 13 rounds.\n• Mechanics: On your turn, roll die"
                " up to 3 times, locking desired dice. Fill 1 open category on"
                " your scorecard (3 of a Kind, Full House, Straight, or Yahtzee"
                " - 5 of a kind)."
            ),
        },
        "Mastermind": {
            "origin": (
                "Invented by Israeli postal worker Mordecai Meirowitz in 1970,"" becoming one of the most successful puzzle games of the 1970s."
            ),
            "used": (
                "Used in computer science and psychology to study deductive"
                " logic, information elimination, and codebreaking algorithms."
            ),
            "today": (
                "A timeless logic puzzle benchmark played physically and"
                " digitally across the globe."
            ),
            "rules": (
                "• Codemaker sets a hidden code of 4 colored pegs. Goal:"
                " Codebreaker guesses code within 10 turns.\n• Feedback Pegs:\n "
                " Black Peg = Right color in the RIGHT position.\n  White Peg ="
                " Right color in the WRONG position."
            ),
        },
    }
