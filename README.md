# 2048

A polished Python + Pygame implementation of the classic 2048 puzzle game, featuring smooth tile-slide animations, score tracking, a win celebration with confetti, and a game-over screen.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Pygame](https://img.shields.io/badge/Pygame-2.x-green) ![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🇬🇧 English

### Overview
Cyberia 2048 is a from-scratch recreation of the classic sliding tile puzzle, built with Python's Pygame library. Beyond the core game logic, it includes a proper game loop with animated transitions, live scoring, and win/lose states.

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
python cyberia_2048.py
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
cyberia_2048.py   # single-file game: logic, rendering, and main loop
```

### How It Works
Each move is computed as a set of tile transitions (start position → end position), which the renderer interpolates over ~130ms to produce the slide animation. Score increases by the value of every merged tile, matching the scoring rules of the original 2048.

---

