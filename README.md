# 🐍 Yılan Oyunu (Snake) — Python & Pygame

Tam özellikli, çok dosyalı bir Snake oyunu.

## Özellikler

- **Ana menü**: Zorluk seviyesi seçimi (Kolay / Orta / Zor)
- **3 zorluk seviyesi**: Yılan hızı zorluğa göre değişir
- **Duraklatma menüsü**: `P` veya `ESC` ile oyunu duraklat
- **Oyun sonu ekranı**: Skor gösterimi ve tekrar oyna / ana menü seçenekleri
- **Yüksek skor sistemi**: `highscores.json` dosyasında zorluk bazlı kalıcı kayıt
- **Normal + Özel (bonus) yem**: Özel yemler zamanla kaybolur, daha çok puan verir ve yılanı 2 hücre büyütür
- **Ses efektleri**: Harici dosya gerekmeden anlık üretilen tonlar (yem yeme, çarpma, tıklama)
- **Farenin de çalıştığı butonlu arayüz**: Menülerde hem klavye hem fare kullanılabilir
- **Yönlü yılan başı (gözlerle)**, yuvarlatılmış gövde çizimi, ızgara arka plan

## Kurulum

```bash
pip install -r requirements.txt
```

## Çalıştırma

```bash
python main.py
```

## Kontroller

| Tuş | İşlev |
|---|---|
| Yön tuşları / WASD | Yılanı yönlendir |
| P / ESC | Duraklat / Devam et |
| Enter | Menüde başlat, oyun sonunda tekrar oyna |
| Fare | Menü butonlarına tıkla |

## Dosya Yapısı

```
snake_game/
├── main.py         # Oyun döngüsü ve durum makinesi (menü/oyun/pause/gameover)
├── snake.py         # Yılan sınıfı: hareket, büyüme, çarpışma, çizim
├── food.py           # Normal ve özel (bonus) yem mantığı
├── settings.py       # Tüm sabitler, renkler, zorluk ayarları
├── ui.py              # Buton bileşeni ve HUD (skor çubuğu) çizimi
├── highscore.py       # JSON tabanlı yüksek skor kaydı/okuma
├── sounds.py           # pygame ile anlık üretilen ses efektleri
├── requirements.txt
└── README.md
```

## Notlar

- Yüksek skorlar her zorluk seviyesi için ayrı ayrı `highscores.json` dosyasında saklanır.
- Ses cihazı bulunamayan ortamlarda (örn. bazı sunucular) oyun sessiz modda otomatik devam eder, hata vermez.
- `settings.py` içinden `WRAP_AROUND = True` yaparsanız yılan duvardan geçip karşı taraftan çıkar.
