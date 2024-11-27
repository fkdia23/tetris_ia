import pygame
import random
from dataclasses import dataclass
from typing import List, Tuple

# Initialisation de Pygame
pygame.init()

# Constantes
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = GRID_WIDTH * BLOCK_SIZE + 200  # Espace supplémentaire pour le menu
SCREEN_HEIGHT = GRID_HEIGHT * BLOCK_SIZE

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = {
    'I': (0, 255, 255),   # Cyan
    'O': (255, 255, 0),   # Jaune
    'T': (128, 0, 128),   # Violet
    'S': (0, 255, 0),     # Vert
    'Z': (255, 0, 0),     # Rouge
    'J': (0, 0, 255),     # Bleu
    'L': (255, 165, 0)    # Orange
}

@dataclass
class Piece:
    shape: List[List[int]]
    x: int
    y: int
    type: str

class Tetris:
    # Définition des pièces comme variable de classe
    SHAPES = {
        'I': [[1, 1, 1, 1]],
        'O': [[1, 1],
              [1, 1]],
        'T': [[0, 1, 0],
              [1, 1, 1]],
        'S': [[0, 1, 1],
              [1, 1, 0]],
        'Z': [[1, 1, 0],
              [0, 1, 1]],
        'J': [[1, 0, 0],
              [1, 1, 1]],
        'L': [[0, 0, 1],
              [1, 1, 1]]
    }

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.level = 1
        self.lines = 0
        self.game_over = False

    def new_piece(self) -> Piece:
        piece_type = random.choice(list(self.SHAPES.keys()))
        shape = self.SHAPES[piece_type]
        return Piece(
            shape=shape,
            x=GRID_WIDTH // 2 - len(shape[0]) // 2,
            y=0,
            type=piece_type
        )

    def rotate_piece(self) -> None:
        shape = self.current_piece.shape
        rotated = list(zip(*shape[::-1]))  # Rotation 90° horaire
        if self.is_valid_move(rotated, self.current_piece.x, self.current_piece.y):
            self.current_piece.shape = [list(row) for row in rotated]

    def is_valid_move(self, shape: List[List[int]], x: int, y: int) -> bool:
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    if (y + i >= GRID_HEIGHT or 
                        x + j < 0 or 
                        x + j >= GRID_WIDTH or 
                        y + i >= 0 and self.grid[y + i][x + j]):
                        return False
        return True

    def place_piece(self) -> None:
        for i, row in enumerate(self.current_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece.y + i][self.current_piece.x + j] = \
                        self.current_piece.type
        
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        
        if not self.is_valid_move(self.current_piece.shape, 
                                self.current_piece.x, 
                                self.current_piece.y):
            self.game_over = True

    def clear_lines(self) -> None:
        lines_cleared = 0
        for i in range(GRID_HEIGHT):
            if all(self.grid[i]):
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1
        
        if lines_cleared:
            self.lines += lines_cleared
            self.score += lines_cleared * 100 * self.level
            self.level = self.lines // 10 + 1

    def draw(self) -> None:
        self.screen.fill(BLACK)
        
        # Dessiner la grille
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if self.grid[i][j]:
                    pygame.draw.rect(self.screen, 
                                   COLORS[self.grid[i][j]],
                                   (j * BLOCK_SIZE, 
                                    i * BLOCK_SIZE, 
                                    BLOCK_SIZE - 1, 
                                    BLOCK_SIZE - 1))
        
        # Dessiner la pièce courante
        for i, row in enumerate(self.current_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen,
                                   COLORS[self.current_piece.type],
                                   ((self.current_piece.x + j) * BLOCK_SIZE,
                                    (self.current_piece.y + i) * BLOCK_SIZE,
                                    BLOCK_SIZE - 1,
                                    BLOCK_SIZE - 1))
        
        # Afficher le score et le niveau
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        level_text = font.render(f'Level: {self.level}', True, WHITE)
        lines_text = font.render(f'Lines: {self.lines}', True, WHITE)
        
        # Afficher la prochaine pièce
        next_text = font.render('Next:', True, WHITE)
        self.screen.blit(next_text, (GRID_WIDTH * BLOCK_SIZE + 20, 20))
        
        # Position pour la prochaine pièce
        next_x = GRID_WIDTH * BLOCK_SIZE + 50
        next_y = 60
        
        for i, row in enumerate(self.next_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen,
                                   COLORS[self.next_piece.type],
                                   (next_x + j * BLOCK_SIZE,
                                    next_y + i * BLOCK_SIZE,
                                    BLOCK_SIZE - 1,
                                    BLOCK_SIZE - 1))
        
        self.screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 20, 150))
        self.screen.blit(level_text, (GRID_WIDTH * BLOCK_SIZE + 20, 190))
        self.screen.blit(lines_text, (GRID_WIDTH * BLOCK_SIZE + 20, 230))
        
        if self.game_over:
            game_over_text = font.render('GAME OVER', True, WHITE)
            self.screen.blit(game_over_text, 
                           (GRID_WIDTH * BLOCK_SIZE // 2 - 70, 
                            GRID_HEIGHT * BLOCK_SIZE // 2))
        
        pygame.display.flip()

    def run(self) -> None:
        fall_time = 0
        fall_speed = 0.5  # Secondes entre chaque chute
        
        while True:
            # Gestion du temps
            self.clock.tick(60)
            fall_time += self.clock.get_rawtime()
            
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                if event.type == pygame.KEYDOWN and not self.game_over:
                    if event.key == pygame.K_LEFT:
                        if self.is_valid_move(self.current_piece.shape,
                                           self.current_piece.x - 1,
                                           self.current_piece.y):
                            self.current_piece.x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.is_valid_move(self.current_piece.shape,
                                           self.current_piece.x + 1,
                                           self.current_piece.y):
                            self.current_piece.x += 1
                    elif event.key == pygame.K_DOWN:
                        if self.is_valid_move(self.current_piece.shape,
                                           self.current_piece.x,
                                           self.current_piece.y + 1):
                            self.current_piece.y += 1
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        while self.is_valid_move(self.current_piece.shape,
                                              self.current_piece.x,
                                              self.current_piece.y + 1):
                            self.current_piece.y += 1
                        self.place_piece()
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset_game()
            
            # Chute automatique
            if fall_time >= fall_speed * 1000:
                fall_time = 0
                if not self.game_over:
                    if self.is_valid_move(self.current_piece.shape,
                                       self.current_piece.x,
                                       self.current_piece.y + 1):
                        self.current_piece.y += 1
                    else:
                        self.place_piece()
            
            self.draw()

if __name__ == '__main__':
    game = Tetris()
    game.run()