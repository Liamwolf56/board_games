import json
import os

DATA_DIR = os.path.expanduser("~/board_games")
LEADERBOARD_FILE = os.path.join(DATA_DIR, "leaderboard.json")


def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(LEADERBOARD_FILE):
        save_leaderboard([])


def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_leaderboard(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def record_score(name, kings_defeated, beat_chess=False):
    board = load_leaderboard()
    display_name = f"{name} ⭐" if beat_chess else name

    entry = {
        "name": name,
        "display_name": display_name,
        "kings_defeated": kings_defeated,
        "beat_chess": beat_chess
    }

    board.append(entry)
    # Sort by kings defeated descending
    board.sort(key=lambda x: (x["kings_defeated"], x.get("beat_chess", False)), reverse=True)

    # Keep top 10
    save_leaderboard(board[:10])
