import pygame
import random

# --- SETTINGS ---
WIDTH = 400
HEIGHT = 400
GRID_SIZE = 4
CELL_SIZE = WIDTH // GRID_SIZE

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
    2048: (237, 194, 46)
}

class Game2048:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(" 2048")
        self.font = pygame.font.SysFont("Arial", 40, bold=True)
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = 2 if random.random() < 0.9 else 4

    def draw(self):
        self.screen.fill((187, 173, 160))  # Background color
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                value = self.grid[r][c]
                color = COLORS.get(value, (60, 58, 50))
                rect = pygame.Rect(c * CELL_SIZE + 5, r * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10)
                pygame.draw.rect(self.screen, color, rect, border_radius=8)
                
                if value != 0:
                    text_color = (119, 110, 101) if value <= 4 else (249, 246, 242)
                    text = self.font.render(str(value), True, text_color)
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)
        pygame.display.flip()

    def slide_and_merge(self, row):
        # Remove zeros, align numbers to the left
        new_row = [i for i in row if i != 0]
        # Merge identical numbers
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i+1]:
                new_row[i] *= 2
                new_row[i+1] = 0
        # Remove zeros again and fill the rest
        new_row = [i for i in new_row if i != 0]
        return new_row + [0] * (GRID_SIZE - len(new_row))

    def move(self, direction):
        old_grid = [row[:] for row in self.grid]
        
        if direction in ["LEFT", "RIGHT"]:
            for r in range(GRID_SIZE):
                row = self.grid[r]
                if direction == "RIGHT": row = row[::-1]
                new_row = self.slide_and_merge(row)
                if direction == "RIGHT": new_row = new_row[::-1]
                self.grid[r] = new_row
                
        elif direction in ["UP", "DOWN"]:
            for c in range(GRID_SIZE):
                column = [self.grid[r][c] for r in range(GRID_SIZE)]
                if direction == "DOWN": column = column[::-1]
                new_column = self.slide_and_merge(column)
                if direction == "DOWN": new_column = new_column[::-1]
                for r in range(GRID_SIZE):
                    self.grid[r][c] = new_column[r]

        if self.grid != old_grid:
            self.add_new_tile()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT: self.move("LEFT")
                    elif event.key == pygame.K_RIGHT: self.move("RIGHT")
                    elif event.key == pygame.K_UP: self.move("UP")
                    elif event.key == pygame.K_DOWN: self.move("DOWN")
            clock.tick(60)

if __name__ == "__main__":
    Game2048().run()
