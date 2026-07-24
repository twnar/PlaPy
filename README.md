# 🐍 Yılan Oyunu (Snake) — Python & Pygame

Tam özellikli, çok dosyalı, **pixel-art temalı** bir Snake oyunu.
Görsel stil, "Plassy" logosundaki orman/gece temasına ve pixel-art
yılan karakterine göre tasarlanmıştır.

## Özellikler

- **Pixel-art grafikler**: Yılan başı (4 yön), gövde, kıvrım, kuyruk, elma, özel yem ve orman zemin karoları özel üretilmiş sprite'lardır
- **Ana menü**: Zorluk seviyesi seçimi (Kolay / Orta / Zor)
- **3 zorluk seviyesi**: Yılan hızı zorluğa göre değişir
- **Duraklatma menüsü**: `P` veya `ESC` ile oyunu duraklat
- **Oyun sonu ekranı**: Skor gösterimi ve tekrar oyna / ana menü seçenekleri
- **Yüksek skor sistemi**: `highscores.json` dosyasında zorluk bazlı kalıcı kayıt
- **Normal + Özel (bonus) yem**: Özel yemler zamanla kaybolur, daha çok puan verir ve yılanı 2 hücre büyütür
- **Ses efektleri**: Harici dosya gerekmeden anlık üretilen tonlar (yem yeme, çarpma, tıklama)
- **Farenin de çalıştığı butonlu arayüz**: Menülerde hem klavye hem fare kullanılabilir
- **Sprite bulunamazsa otomatik yedek mod**: PNG dosyaları eksikse oyun eski vektörel çizime geri döner, çökmez

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
├── main.py               # Oyun döngüsü ve durum makinesi (menü/oyun/pause/gameover)
├── snake.py               # Yılan sınıfı: hareket, büyüme, çarpışma, sprite/vektör çizim
├── food.py                 # Normal ve özel (bonus) yem mantığı
├── settings.py              # Tüm sabitler, renkler (orman teması), zorluk ayarları
├── ui.py                     # Buton bileşeni ve HUD (skor çubuğu) çizimi
├── highscore.py               # JSON tabanlı yüksek skor kaydı/okuma
├── sounds.py                   # pygame ile anlık üretilen ses efektleri
├── assets.py                    # Pixel-art sprite'ları yükleyip ölçekleyen modül
├── generate_sprites.py           # Sprite PNG'lerini üreten script (Pillow ile)
├── assets/
│   └── sprites/                   # Üretilmiş pixel-art PNG dosyaları
│       ├── head_up.png, head_down.png, head_left.png, head_right.png
│       ├── body_straight.png, body_turn.png, tail.png
│       ├── food_apple.png, food_special.png
│       └── grass_0.png, grass_1.png
├── requirements.txt
└── README.md
```

## Pixel-Art Sprite'ları Yeniden Üretme

Sprite'lar `assets/sprites/` klasöründe hazır PNG olarak gelir; oyunu
doğrudan çalıştırabilirsiniz. Renk paletini veya şekilleri değiştirmek
isterseniz `generate_sprites.py` dosyasını düzenleyip yeniden çalıştırın:

```bash
python generate_sprites.py
```

Bu script Pillow (PIL) kullanır ve `assets/sprites/` altındaki tüm
PNG'leri yeniden oluşturur.

## Notlar

- Yüksek skorlar her zorluk seviyesi için ayrı ayrı `highscores.json` dosyasında saklanır.
- Ses cihazı bulunamayan ortamlarda (örn. bazı sunucular) oyun sessiz modda otomatik devam eder, hata vermez.
- `assets/sprites/` klasörü eksik veya bozuksa (`settings.py` içinde `USE_SPRITES = True` olsa bile) oyun otomatik olarak eski vektörel çizim moduna geçer, çökmez.
- `settings.py` içinden `USE_SPRITES = False` yaparsanız pixel-art yerine düz vektörel çizim kullanılır.
- `settings.py` içinden `WRAP_AROUND = True` yaparsanız yılan duvardan geçip karşı taraftan çıkar.
