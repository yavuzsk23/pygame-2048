# 2048

A polished Python + Pygame implementation of the classic 2048 puzzle game, featuring smooth tile-slide animations, score tracking, a win celebration with confetti, and a game-over screen.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Pygame](https://img.shields.io/badge/Pygame-2.x-green) ![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🇬🇧 English

### Overview
2048 is a from-scratch recreation of the classic sliding tile puzzle, built with Python's Pygame library. Beyond the core game logic, it includes a proper game loop with animated transitions, live scoring, and win/lose states.

### Features
- 4×4 grid with the classic 2048 color palette
- Smooth sliding animation for every move (tiles glide to their new position instead of jumping)
- Live score tracking + session high score
- Win screen with a confetti celebration when reaching the 2048 tile — play continues afterward if desired
- Game-over detection (no empty cells and no possible merges)
- Instant restart at any time

### Installation
```bash
pip install pygame
python 2048.py
```

### Requirements
- Python 3.8+
- Pygame

### Controls
| Key | Action |
|---|---|
| ↑ ↓ ← → | Move / merge tiles |
| `R` | Restart the game |
| `Space` | Continue playing after reaching 2048 |

### Project Structure
```
2048.py   # single-file game: logic, rendering, and main loop
```

### How It Works
Each move is computed as a set of tile transitions (start position → end position), which the renderer interpolates over ~130ms to produce the slide animation. Score increases by the value of every merged tile, matching the scoring rules of the original 2048.

---

## 🇩🇪 Deutsch

### Überblick
2048 ist eine vollständige Neuimplementierung des klassischen Schiebe-Puzzles mit Python und der Pygame-Bibliothek. Neben der reinen Spiellogik enthält es eine animierte Spielschleife, eine Live-Punkteanzeige sowie Sieg- und Niederlage-Zustände.

### Funktionen
- 4×4-Spielfeld mit der klassischen 2048-Farbpalette
- Flüssige Verschiebe-Animation bei jedem Zug (Kacheln gleiten statt zu springen)
- Live-Punktestand + Session-Highscore
- Sieg-Bildschirm mit Konfetti-Animation beim Erreichen der 2048-Kachel — das Spiel kann danach fortgesetzt werden
- Erkennung des Spielendes (kein leeres Feld und keine möglichen Zusammenführungen mehr)
- Jederzeit neu starten

### Installation
bash
pip install pygame
python 2048.py


### Voraussetzungen
- Python 3.8+
- Pygame

### Steuerung
| Taste | Aktion |
|---|---|
| ↑ ↓ ← → | Kacheln bewegen / zusammenführen |
| R | Spiel neu starten |
| Leertaste | Nach Erreichen von 2048 weiterspielen |

### Projektstruktur

2048.py   # Einzeldatei-Spiel: Logik, Rendering und Hauptschleife


### Funktionsweise
Jeder Zug wird als eine Reihe von Kachelbewegungen (Startposition → Zielposition) berechnet, die beim Rendern über ca. 130ms interpoliert werden, um die Gleitanimation zu erzeugen. Der Punktestand erhöht sich um den Wert jeder zusammengeführten Kachel, entsprechend den Regeln des Original-2048.

---

## 🇹🇷 Türkçe

### Genel Bakış
2048, klasik kayan taş bulmacasının Python ve Pygame kütüphanesiyle sıfırdan yazılmış, cilalı bir versiyonudur. Temel oyun mantığının ötesinde; animasyonlu geçişler, canlı skor takibi ve kazanma/kaybetme durumları içerir.

### Özellikler
- Klasik 2048 renk paletiyle 4×4 oyun tahtası
- Her hamlede akıcı kaydırma animasyonu (taşlar zıplamak yerine yeni konumlarına kayar)
- Canlı skor takibi + oturum içi en yüksek skor
- 2048 taşına ulaşınca konfeti efektli kazanma ekranı — istenirse oyuna devam edilebilir
- Oyun bitişi tespiti (boş hücre kalmadığında ve birleşme imkanı olmadığında)
- İstenilen anda anında yeniden başlatma

### Kurulum
bash
pip install pygame
python 2048.py


### Gereksinimler
- Python 3.8+
- Pygame

### Kontroller
| Tuş | İşlev |
|---|---|
| ↑ ↓ ← → | Taşları hareket ettir / birleştir |
| R | Oyunu yeniden başlat |
| Boşluk | 2048'e ulaştıktan sonra oyuna devam et |

### Proje Yapısı

2048.py   # Tek dosyalık oyun: mantık, çizim ve ana döngü


### Nasıl Çalışır
Her hamle, taşların başlangıç ve bitiş konumlarını içeren bir hareket listesi olarak hesaplanır; bu liste render sırasında ~130ms boyunca enterpolasyonla çizilerek kaydırma animasyonunu oluşturur. Skor, orijinal 2048'in kurallarına uygun şekilde, birleşen her taşın değeri kadar artar.
