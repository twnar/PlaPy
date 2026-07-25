import json
import os
from settings import HIGH_SCORE_FILE

DEFAULT_DATA = {
    "Easy": 0,
    "Medium": 0,
    "Hard": 0,
}


def load_high_scores():
    if not os.path.exists(HIGH_SCORE_FILE):
        return DEFAULT_DATA.copy()

    try:
        with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        for key in DEFAULT_DATA:
            if key not in data:
                data[key] = 0

        return data

    except (json.JSONDecodeError, OSError):
        return DEFAULT_DATA.copy()


def save_high_scores(data):
    try:
        with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    except OSError:
        pass


def update_high_score(difficulty, score):
    data = load_high_scores()
    current_best = data.get(difficulty, 0)

    if score > current_best:
        data[difficulty] = score
        save_high_scores(data)
        return True

    return False