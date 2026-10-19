import tkinter as tk


class HistoryModeFrame(tk.Frame):

  def __init__(self, parent, hub_app):
    super().__init__(parent, bg="#2c3e50", bd=2, relief="solid")
    self.hub_app = hub_app

    tk.Label(
        self,
        text="📜 THE COMPLETE HISTORY OF ARCADE BOARD GAMES",
        font=("Arial", 14, "bold"),
        bg="#2c3e50",
        fg="#ffdd59",
    ).pack(pady=10)

    self.game_histories = {
        "Chess": (
            "CHESS: FROM 6TH CENTURY INDIA TO MODERN DIGITAL ERA\n\n"
            "• Ancient Origin (c. 600 CE): Chess originated in northern India"
            " during the Gupta Empire under the name 'Chaturanga', representing"
            " the four divisions of the military: infantry, cavalry, elephants,"
            " and chariots.\n\n"
            "• Spread & Evolution: The game traveled along the Silk Road to"
            " Persia ('Shatranj') and was brought to Islamic Spain and medieval"
            " Europe in the 9th and 10th centuries. European rules evolved"
            " drastically around 1475 CE, giving the Queen and Bishop their"
            " modern, fast-moving power.\n\n"
            "• Modern Era: From global championship tournaments to computer"
            " engines like Deep Blue defeating world champions, Chess is now a"
            " digital staple played by millions worldwide."
        ),
        "Shogi": (
            "SHOGI: JAPANESE CHESS\n\n"
            "• Ancient Origin (c. 1100s CE): Shogi (Japanese Chess) arrived in"
            " Japan from China during the Nara or Heian period, blending"
            " elements of ancient Chinese chess with native strategic"
            " concepts.\n\n"
            "• The Drop Rule Innovation: Unlike Western chess where captured"
            " pieces are lost forever, Shogi's unique rule allows players to"
            " 'drop' captured enemy pieces back onto the board as their own,"
            " eliminating stalemates and creating deeply tactical, dynamic"
            " games.\n\n"
            "• Modern Era: Shogi remains one of Japan's most popular intellectual"
            " sports, played professionally with centuries-old traditions."
        ),
        "Xiangqi": (
            "XIANGQI: CHINESE CHESS\n\n"
            "• Ancient Origin (c. 200 BCE): Xiangqi traces its roots back to"
            " the Han Dynasty (and earlier military simulation games). It"
            " simulates a battle fought across a central river with a "
            "fortified palace for the General.\n\n"
            "• Unique Mechanics: Unlike grid intersection rules, Xiangqi pieces"
            " move along grid lines. Cannons require a screen to jump over, and"
            " the General and advisors are locked inside the palace.\n\n"
            "• Modern Era: Xiangqi is immensely popular throughout China and"
            " Southeast Asia, regularly played in public parks and international"
            " tournaments."
        ),
        "Chaturanga": (
            "CHATURANG: THE ANCESTOR\n\n"
            "• Ancient Origin (c. 6th Century CE): Mentioned in ancient Indian"
            " literature, Chaturanga is recognized globally by historians as the"
            " common ancestor from which Chess, Shogi, and Xiangqi descended.\n\n"
            "• Name Meaning: 'Chaturanga' translates to 'four limbs' (infantry,"
            " cavalry, elephants, and chariots), played with dice in some"
            " early variations to simulate the fog of war.\n\n"
            "• Modern Era: Preserved by historians and recreated digitally to"
            " let modern players experience the very roots of tactical board"
            " gaming."
        ),
        "Checkers": (
            "CHECKERS (DRAUGHTS): ANCIENT ROOTS\n\n"
            "• Ancient Origin (c. 3000 BCE): Archaeological finds in the ancient"
            " city of Ur in Mesopotamia reveal board games resembling checkers"
            " played over 5,000 years ago. A similar game, Alquerque, was played"
            " in ancient Egypt.\n\n"
            "• Evolution: In 12th-century southern France, Alquerque was"
            " combined with the board of Chess, creating 'Draughts' (known as"
            " Checkers in North America), introducing forced jumps and King"
            " crowning.\n\n"
            "• Modern Era: A simple yet profound mathematical game, Checkers was"
            " famously solved by computer scientists in 2007 (resulting in a"
            " guaranteed draw with perfect play)."
        ),
        "Reversi": (
            "REVERSI & OTHELLO: THE FLIPPING BATTLE\n\n"
            "• Origin (1883): Invented in England by Lewis Waterman under the"
            " name Reversi. It gained immense popularity in Victorian parlors"
            " before fading slightly.\n\n"
            "• The Othello Revival (1971): Goro Hasegawa redesigned and"
            " patented the game as 'Othello' in Japan, referencing"
            " Shakespeare's play about conflict and sudden reversals of"
            " fortune.\n\n"
            "• Modern Era: A staple strategy game of flanking and disc flipping,"
            " played worldwide in tournaments and digital app stores."
        ),
        "Connect 4": (
            "CONNECT 4: THE VERTICAL DROP\n\n"
            "• Origin (1974): Created and published by Milton Bradley (now"
            " Hasbro) under the name Connect Four, drawing inspiration from"
            " centuries-old alignment games like Tic-Tac-Toe.\n\n"
            "• Mechanics: Gravity is the defining feature—forcing players to"
            " think vertically and set up multi-directional traps across a"
            " 7x6 grid.\n\n"
            "• Modern Era: Solved mathematically in 1988 (the first player can"
            " always force a win with the center column), Connect 4 remains a"
            " beloved casual classic for all ages."
        ),
        "Tic-Tac-Toe": (
            "TIC-TAC-TOE: ANCIENT PENCIL & PAPER\n\n"
            "• Ancient Origin (c. 1300 BCE): Early variants of three-in-a-row"
            " games have been carved into the roofing tiles of ancient Egyptian"
            " temples and Roman ruins across the empire.\n\n"
            "• Evolution: Known historically as 'Noughts and Crosses' in the"
            " UK, it became known as Tic-Tac-Toe in the United States in the"
            " 20th century.\n\n"
            "• Modern Era: The quintessential children's puzzle that introduces"
            " basic logic, game theory, and the concept of unbeatable terminal"
            " states (cats' games)."
        ),
        "Battleship": (
            "BATTLESHIP: FROM TRENCHES TO TABLETOPS\n\n"
            "• Origin (WWI Era): Originally played with pencil and paper by"
            " French officers during World War I under the name "
            "'L'Attaque'.\n\n"
            "• Commercial Release (1967): Milton Bradley published the iconic"
            " plastic grid version with red and white pegs in 1967, turning a"
            " pen-and-paper pastime into a physical household sensation.\n\n"
            "• Modern Era: Adapted into video games, movies, and digital"
            " arcades as the ultimate game of hidden deduction and naval"
            " strategy."
        ),
        "Otrio": (
            "OTRIO: THE MODERN MULTI-TIERED PUZZLE\n\n"
            "• Origin (2014): Invented by toy designer Brain Wright and"
            " published by Spin Master, Otrio was created as a modern evolution"
            " of traditional Tic-Tac-Toe.\n\n"
            "• Mechanics: By introducing three concentric ring sizes and three"
            " win conditions (same color line, ascending/descending size line,"
            " or concentric rings on one spot), it transforms a simple game"
            " into a 3D tactical challenge.\n\n"
            "• Modern Era: Celebrated globally as an award-winning modern family"
            " and strategy board game."
        ),
        "Sequence for Kids": (
            "SEQUENCE FOR KIDS: ANIMAL ALIGNMENT\n\n"
            "• Origin (1981 / Modern Variant): The original adult 'Sequence'"
            " board game was invented by Doug ReQua in 1981, combining cards"
            " and token placement.\n\n"
            "• Kids Variant: Streamlined for younger audiences by replacing"
            " standard playing cards with vibrant animal illustrations, making"
            " matching and early strategy accessible.\n\n"
            "• Modern Era: A preschool favorite that teaches pattern recognition"
            " and tactical blocking."
        ),
        "Animal Upon Animal": (
            "ANIMAL UPON ANIMAL: THE STACKING PHENOMENON\n\n"
            "• Origin (2005): Created by German game designer Klaus Miltenberger"
            " and published by HABA, a renowned publisher of children's games.\n\n"
            "• Mechanics: A dexterity game where players roll dice to stack"
            " wooden crocodiles, penguins, sheep, and monkeys without causing a"
            " collapse.\n\n"
            "• Modern Era: Winner of multiple international game awards for"
            " bringing physical coordination, laughter, and tactile fun to"
            " tabletop gaming."
        ),
        "Monza": (
            "MONZA: THE COLOR-MATCHING RACER\n\n"
            "• Origin (2000): Designed by Jürgen Grunau and published by HABA."
            " Named after the famous Italian Grand Prix racing circuit.\n\n"
            "• Mechanics: Instead of numbers, players roll colored dice and"
            " strategically sequence which adjacent track lanes to jump"
            " across.\n\n"
            "• Modern Era: A brilliant educational and strategic board game that"
            " introduces children and adults to forward planning and color"
            " probability."
        ),
        "Yahtzee": (
            "YAHTZEE: THE YACHT PASSION PROJECT\n\n"
            "• Origin (1954): Invented by a wealthy Canadian couple while"
            " playing dice games on their yacht, originally calling it "
            "'The Yacht Game'.\n\n"
            "• Commercial Success (1956): Entrepreneur Edwin S. Lowe recognized"
            " its addictive nature, bought the rights, renamed it 'Yahtzee',"
            " and marketed it into a global phenomenon.\n\n"
            "• Modern Era: One of the best-selling dice games in history, found"
            " in millions of homes and digital arcades worldwide."
        ),
        "Mastermind": (
            "MASTERMIND: THE COLD WAR CODE BREAKER\n\n"
            "• Origin (1970): Invented by Mordecai Meirowitz, an Israeli"
            " postmaster and telecommunications expert. The concept of secret"
            " code-breaking dates back centuries to cryptographic ciphers.\n\n"
            "• Commercial Release: After being rejected by several major toy"
            " companies, Invicta Plastics published it in 1970, and it became an"
            " instant worldwide blockbuster during the 1970s.\n\n"
            "• Modern Era: A legendary test of deductive reasoning, logic, and"
            " elimination."
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
        width=22,
    )
    self.history_list.pack(fill=tk.BOTH, expand=True)

    for g in self.game_histories.keys():
      self.history_list.insert(tk.END, g)

    self.history_list.bind("<<ListboxSelect>>", self.on_history_select)

    display_frame = tk.Frame(content_f, bg="#1e272e", bd=2, relief="solid")
    display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

    self.history_title = tk.Label(
        display_frame,
        text="Select a game from the list to explore its full history",
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
