"""
highscore.py
Yüksek skorların JSON dosyasına kaydedilip okunmasını yönetir.
"""

import json
import os
from settings import HIGH_SCORE_FILE

DEFAULT_DATA = {
    "Kolay": 0,
    "Orta": 0,
    "Zor": 0,
}


def load_high_scores():
    """JSON dosyasından yüksek skorları okur. Dosya yoksa varsayılan döner."""
    if not os.path.exists(HIGH_SCORE_FILE):
        return DEFAULT_DATA.copy()
    try:
        with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Eksik anahtarları tamamla
        for key in DEFAULT_DATA:
            if key not in data:
                data[key] = 0
        return data
    except (json.JSONDecodeError, OSError):
        return DEFAULT_DATA.copy()


def save_high_scores(data):
    """Yüksek skor sözlüğünü JSON dosyasına yazar."""
    try:
        with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError:
        pass  # Dosyaya yazılamazsa sessizce geç (oyun akışını bozmasın)


def update_high_score(difficulty, score):
    """
    Belirtilen zorluk seviyesi için skor mevcut rekordan yüksekse günceller.
    Yeni rekor kırıldıysa True, kırılmadıysa False döner.
    """
    data = load_high_scores()
    current_best = data.get(difficulty, 0)
    if score > current_best:
        data[difficulty] = score
        save_high_scores(data)
        return True
    return False
