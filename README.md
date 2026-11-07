# 👑 Master Board Game Hub

A collection of classic board games in one app, with a roguelike story campaign where you take on 15 Kings, one game at a time.

## ⬇️ How to Download and Play

**You don't need to install Python or use a terminal.**

### Windows
1. Click the green **Code** button at the top of this page.
2. Click **Download ZIP**.
3. Find the ZIP in your Downloads folder, right-click it, and choose **Extract All**.
4. Open the extracted folder and double-click **play** (it may show as `play.bat`).
5. The game opens. Have fun!

> **Windows shows a blue "Windows protected your PC" warning?**
> This is normal for small games made by individuals. Click **More info**, then **Run anyway**.

### Mac and Linux (experimental)
The Windows version is the most tested. Mac and Linux builds are included but haven't been fully tested. To try them:
1. Download and extract the ZIP as above.
2. Open a terminal in the extracted folder and run:
   ```
   bash play.sh
   ```

If something doesn't work, please open an **Issue** on this page and tell me what happened.

## 🎮 Game Modes

The top of the app has four buttons. Click one to switch modes.

### 🕹️ Arcade Mode
Jump straight into any of the board games for a quick match, with no campaign pressure.

### 📖 Story Mode: The King's Gauntlet
An ironman-style roguelike campaign. Defeat as many Kings as you can!

- There are **15 Kings**, and each challenges you to a different game.
- The first 14 Kings appear in a **random order** every run. The 15th is always the **Final Boss**.
- **One loss ends your run.** Win a game to move on to the next King.
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
2. Click the first King on the list and enter your name when asked.
3. Win the game to unlock the next King. Beaten Kings get a ✅.
4. Click **🏆 View Leaderboard** at any time to see the top 10 scores.

> Leaderboard scores are saved on your own computer, in a folder called `board_games` in your home folder.

### ♟️ Chess Puzzles
Test your tactical vision with chess puzzle challenges.

### 📜 History Mode
Track your past match performance, stats, and run history across the hub.

## 📋 Included Games

Chess (with a Grandmaster AI and puzzles) • Shogi (Japanese Chess) • Xiangqi (Chinese Chess) • Chaturanga • Yahtzee • Otrio • Tic-Tac-Toe • Connect 4 • Checkers • Reversi • Battleship • Mastermind • Monza • Animal Upon Animal • Sequence for Kids

## ❓ Troubleshooting

| Problem | What to do |
|---------|-----------|
| Windows shows a blue warning | Click **More info → Run anyway**. |
| Nothing happens when I double-click | Make sure you **extracted** the ZIP first. Don't run it from inside the ZIP. |
| The leaderboard is empty | Scores are saved when a run **ends** (a loss or a win). Finish a run to see yours. |
| A game won't open | Tell me which one by opening an Issue on this page. |

## 🛠️ For Developers

The game is written in Python with Tkinter. To run it from source:

```
pip install python-chess
python main_hub.py
```

**Project structure**
- `main_hub.py`: the main hub application and launcher
- `arcade/`: quick-play arcade mode
- `story/`: the roguelike campaign and its boss games
- `chess_puzzles/`: tactical chess puzzles
- `history/`: match history and statistics
- `leaderboard.py`: the Story Mode leaderboard
- `play.bat` and `play.sh`: the launch scripts
- `app/`: the ready-to-play app, built automatically by GitHub Actions

To rebuild the app after changing the code, go to **Actions → Build app into repo → Run workflow**.
