# 🎮 Master Board Game Hub

A collection of classic board games in one app, with a story campaign where you take on 15 Kings, one game at a time.

## ⬇️ How to Download and Play

**You don't need to install Python or use a terminal.**

### Windows
1. Click the green **Code** button at the top of this page.
2. Click **Download ZIP**.
3. Find the ZIP in your Downloads folder, right-click it, and choose **Extract All**.
4. Open the extracted folder and double-click **play.bat**.
5. The game opens. Have fun!

> **Windows shows a blue "Windows protected your PC" warning?**
> This is normal for small games made by individuals. Click **More info**, then **Run anyway**.

### Mac and Linux (experimental)
The Windows version is the one tested most. Mac and Linux builds are included but have not been fully tested. To try them:
1. Download and extract the ZIP as above.
2. Open a terminal in the extracted folder and run:
   ```
   bash play.sh
   ```

If something doesn't work, please open an issue on this page and tell me what happened.

## 🕹️ The Game Modes

The top of the app has four buttons. Click one to switch modes.

### 🕹️ Arcade Mode
Pick any game from the list and play it right away, without any story. *(Edit this line: describe how many players or which game options Arcade has, for example playing against a friend or the computer.)*

### 📖 Story Mode: The King's Gauntlet
Defeat as many Kings as you can!

- There are **15 Kings**. Each one challenges you to a different game.
- The first 14 Kings come in a **random order** every run. The 15th is always the **Final Boss**.
- **One loss ends your run.** You win a game to move on to the next King.
- When your run ends, your score is saved to the **Leaderboard**.
- Beat all 15 Kings, including the Final Boss, to earn the **⭐ Grand Champion** star next to your name.

**The Kings and their games:**

| King | Game |
|------|------|
| High Lord Wild Unicorn | Sequence for Kids |
| Gridmaster First Strike | Connect 4 |
| High Lord Concentric Ring | Otrio |
| Admiral Blind Grid | Battleship |
| High Sovereign Apex Stack | Animal Upon Animal |
| High Lord Turbo Combo | Monza |
| King Ultimate Gridlock | Tic-Tac-Toe |
| High King Crown Jump | Checkers |
| Sovereign Flipside | Reversi |
| Emperor Dragon King | Shogi |
| Grand General Sky Cannon | Xiangqi |
| Raja Four-Fold War | Chaturanga |
| High Lord Five-of-a-Kind | Yahtzee |
| Grandmaster Cipher Lock | Mastermind |
| 👑 **King Chess.com (Final Boss)** | Chess |

**How to play Story Mode:**
1. Click **Story Mode**.
2. Click the first King on the list. Enter your name when asked.
3. Win the game to unlock the next King. Beaten Kings get a ✅.
4. Click **🏆 View Leaderboard** at any time to see the top 10 scores.

> Your leaderboard scores are saved on your own computer, in a folder called `board_games` in your home folder.

### 📜 History Mode
*(Edit this line: describe what History Mode does, for example looking at past games.)*

### ♟️ Chess Puzzles
Solve chess puzzles on the board. *(Edit this line: add details such as how many puzzles there are or how to get hints.)*

## ❓ Troubleshooting

| Problem | What to do |
|---------|-----------|
| Windows shows a blue warning | Click **More info → Run anyway**. |
| Nothing happens when I double-click | Make sure you **extracted** the ZIP first. Don't run it from inside the ZIP. |
| The leaderboard is empty | Scores are saved when a run **ends** (a loss or a win). Finish a run to see yours. |
| A game won't open | Tell me which one in an issue on this page. |

## 🛠️ For Developers

The game is written in Python with Tkinter. To run it from source:

```
pip install python-chess
python main_hub.py
```

The ready-to-play app in the `app` folder is built automatically by GitHub Actions (**Actions → Build app into repo → Run workflow**).
