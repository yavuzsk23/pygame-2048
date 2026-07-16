import pygame
import random
import sys

# ============================================================
# SETTINGS
# ============================================================
WIDTH = 400
GAME_AREA_HEIGHT = 400
SCORE_BAR_HEIGHT = 90
WINDOW_HEIGHT = GAME_AREA_HEIGHT + SCORE_BAR_HEIGHT
GRID_SIZE = 4
CELL_SIZE = WIDTH // GRID_SIZE
TOP_MARGIN = SCORE_BAR_HEIGHT  # game board starts below this (space for score bar)

ANIMATION_DURATION_MS = 130  # duration of slide animation
WIN_VALUE = 2048

# Color Palette (Classic 2048 Colors)
COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

CONFETTI_COLORS = [
    (255, 89, 94), (255, 202, 58), (138, 201, 38),
    (25, 130, 196), (106, 76, 147), (255, 158, 0),
]


class Game2048:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Cyberia 2048")
        self.font = pygame.font.SysFont("Arial", 40, bold=True)
        self.ui_font = pygame.font.SysFont("Arial", 22, bold=True)
        self.overlay_font = pygame.font.SysFont("Arial", 30, bold=True)
        self.overlay_font_small = pygame.font.SysFont("Arial", 18)

        self.high_score = 0  # stored in memory while program runs
        self.new_game()

    # --------------------------------------------------------
    # GAME STATE MANAGEMENT
    # --------------------------------------------------------
    def new_game(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.game_state = "playing"  # playing | animating | game_over | won
        self.win_shown = False
        self.animations = []
        self.animation_start = 0
        self._won_this_move = False
        self.confetti = []
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [
            (r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)
            if self.grid[r][c] == 0
        ]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = 2 if random.random() < 0.9 else 4

    def is_game_over(self):
        """Game ends if board is full AND no adjacent cells can merge."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] == 0:
                    return False
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                v = self.grid[r][c]
                if c + 1 < GRID_SIZE and self.grid[r][c + 1] == v:
                    return False
                if r + 1 < GRID_SIZE and self.grid[r + 1][c] == v:
                    return False
        return True

    # --------------------------------------------------------
    # MOVE LOGIC (slide + merge + animation data)
    # --------------------------------------------------------
    def process_line(self, line):
        """
        Slides and merges a row/column.
        Returns: (new_line, moves)
        moves -> [(original_index, value, target_index, result_value, visible), ...]
        visible=False means the tile was merged and disappears in animation.
        """
        items = [(i, v) for i, v in enumerate(line) if v != 0]
        moves = []
        new_line = [0] * GRID_SIZE
        write_idx = 0
        i = 0
        n = len(items)
        while i < n:
            orig_i, val_i = items[i]
            if i + 1 < n and items[i + 1][1] == val_i:
                orig_j, val_j = items[i + 1]
                result = val_i * 2
                moves.append((orig_i, val_i, write_idx, result, True))
                moves.append((orig_j, val_j, write_idx, result, False))
                new_line[write_idx] = result
                write_idx += 1
                i += 2
            else:
                moves.append((orig_i, val_i, write_idx, val_i, True))
                new_line[write_idx] = val_i
                write_idx += 1
                i += 1
        return new_line, moves

    def cell_center(self, r, c):
        x = c * CELL_SIZE + CELL_SIZE // 2
        y = TOP_MARGIN + r * CELL_SIZE + CELL_SIZE // 2
        return x, y

    def move(self, direction):
        if self.game_state != "playing":
            return

        new_grid = [row[:] for row in self.grid]
        all_moves = []
        score_gain = 0
        won_this_move = False
        is_row = direction in ("LEFT", "RIGHT")

        for fixed in range(GRID_SIZE):
            if is_row:
                base = self.grid[fixed][:]
            else:
                base = [self.grid[r][fixed] for r in range(GRID_SIZE)]

            line = base[::-1] if direction in ("RIGHT", "DOWN") else base[:]
            new_line, moves = self.process_line(line)

            def idx_to_cell(line_idx, fixed=fixed, direction=direction):
                if direction == "LEFT":
                    return (fixed, line_idx)
                elif direction == "RIGHT":
                    return (fixed, GRID_SIZE - 1 - line_idx)
                elif direction == "UP":
                    return (line_idx, fixed)
                else:  # DOWN
                    return (GRID_SIZE - 1 - line_idx, fixed)

            for orig_idx, val, target_idx, result_val, visible in moves:
                start_r, start_c = idx_to_cell(orig_idx)
                end_r, end_c = idx_to_cell(target_idx)
                all_moves.append({
                    "start": self.cell_center(start_r, start_c),
                    "end": self.cell_center(end_r, end_c),
                    "value": val,
                })
                if visible and result_val != val:
                    score_gain += result_val
                    if result_val == WIN_VALUE:
                        won_this_move = True

            for line_idx, v in enumerate(new_line):
                r, c = idx_to_cell(line_idx)
                new_grid[r][c] = v

        if new_grid == self.grid:
            return  # no change, invalid move

        self.grid = new_grid
        self.score += score_gain
        self.high_score = max(self.high_score, self.score)
        self.animations = all_moves
        self.animation_start = pygame.time.get_ticks()
        self.game_state = "animating"
        self._won_this_move = won_this_move

    def update_animation(self):
        if self.game_state != "animating":
            return
        elapsed = pygame.time.get_ticks() - self.animation_start
        if elapsed >= ANIMATION_DURATION_MS:
            self.animations = []
            self.add_new_tile()
            if self._won_this_move and not self.win_shown:
                self.game_state = "won"
                self.win_shown = True
                self._create_confetti()
            elif self.is_game_over():
                self.game_state = "game_over"
            else:
                self.game_state = "playing"

    # --------------------------------------------------------
    # CONFETTI
    # --------------------------------------------------------
    def _create_confetti(self):
        self.confetti = [
            {
                "x": random.randint(0, WIDTH),
                "y": random.randint(-WINDOW_HEIGHT, 0),
                "vx": random.uniform(-1.2, 1.2),
                "vy": random.uniform(2.5, 5.5),
                "color": random.choice(CONFETTI_COLORS),
                "size": random.randint(4, 9),
            }
            for _ in range(90)
        ]

    def _update_draw_confetti(self):
        for p in self.confetti:
            p["y"] += p["vy"]
            p["x"] += p["vx"]
            if p["y"] > WINDOW_HEIGHT:
                p["y"] = random.randint(-40, -10)
                p["x"] = random.randint(0, WIDTH)
            pygame.draw.rect(self.screen, p["color"], (p["x"], p["y"], p["size"], p["size"]))

    # --------------------------------------------------------
    # DRAWING
    # --------------------------------------------------------
    def _draw_tile(self, center_x, center_y, value):
        color = COLORS.get(value, (60, 58, 50))
        rect = pygame.Rect(0, 0, CELL_SIZE
