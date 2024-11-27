import pygame
import random
from dataclasses import dataclass
from typing import List, Tuple

# Initialisation de Pygame
pygame.init()
pygame.font.init()

# Constantes
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = GRID_WIDTH * BLOCK_SIZE + 300  # Largeur augmentée pour l'interface
SCREEN_HEIGHT = GRID_HEIGHT * BLOCK_SIZE
SIDEBAR_WIDTH = 250

# Couleurs
COLORS = {
    'background': (20, 20, 20),
    'grid_lines': (50, 50, 50),
    'text': (255, 255, 255),
    'button_normal': (70, 70, 70),
    'button_hover': (100, 100, 100),
    'pieces': {
        'I': (0, 255, 255),   # Cyan
        'O': (255, 255, 0),   # Jaune
        'T': (128, 0, 128),   # Violet
        'S': (0, 255, 0),     # Vert
        'Z': (255, 0, 0),     # Rouge
        'J': (0, 0, 255),     # Bleu
        'L': (255, 165, 0)    # Orange
    }
}

class Button:
    def __init__(self, x, y, width, height, text, font_size=24):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.hovered = False

    def draw(self, screen):
        # Change color when hovered
        color = COLORS['button_hover'] if self.hovered else COLORS['button_normal']
        pygame.draw.rect(screen, color, self.rect)
        
        # Render text
        text_surface = self.font.render(self.text, True, COLORS['text'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_hovered(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        return self.hovered

@dataclass
class Piece:
    shape: List[List[int]]
    x: int
    y: int
    type: str

class TetrisUI:
    def __init__(self, game):
        self.game = game
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        
        # Créer les boutons
        button_width = 200
        button_x = GRID_WIDTH * BLOCK_SIZE + 50
        self.buttons = {
            'pause': Button(button_x, 400, button_width, 50, 'Pause'),
            'restart': Button(button_x, 460, button_width, 50, 'Restart'),
            'quit': Button(button_x, 520, button_width, 50, 'Quit')
        }

    def draw(self):
        # Fond de l'écran
        self.screen.fill(COLORS['background'])
        
        # Dessiner la grille de jeu
        self._draw_grid()
        
        # Dessiner la pièce courante
        self._draw_current_piece()
        
        # Dessiner la prochaine pièce
        self._draw_next_piece()
        
        # Dessiner les statistiques
        self._draw_stats()
        
        # Dessiner les boutons
        for button in self.buttons.values():
            button.draw(self.screen)
        
        # Afficher les messages de pause et game over
        self._draw_game_messages()
        
        pygame.display.flip()

    def _draw_grid(self):
        # Dessiner la grille de jeu
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if self.game.grid[i][j]:
                    pygame.draw.rect(self.screen, 
                                     COLORS['pieces'][self.game.grid[i][j]],
                                     (j * BLOCK_SIZE, 
                                      i * BLOCK_SIZE, 
                                      BLOCK_SIZE - 1, 
                                      BLOCK_SIZE - 1))
        
        # Dessiner les lignes de la grille
        for x in range(0, GRID_WIDTH * BLOCK_SIZE, BLOCK_SIZE):
            pygame.draw.line(self.screen, COLORS['grid_lines'], 
                             (x, 0), (x, GRID_HEIGHT * BLOCK_SIZE))
        for y in range(0, GRID_HEIGHT * BLOCK_SIZE, BLOCK_SIZE):
            pygame.draw.line(self.screen, COLORS['grid_lines'], 
                             (0, y), (GRID_WIDTH * BLOCK_SIZE, y))

    def _draw_current_piece(self):
        if not self.game.paused and not self.game.game_over:
            for i, row in enumerate(self.game.current_piece.shape):
                for j, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self.screen,
                                       COLORS['pieces'][self.game.current_piece.type],
                                       ((self.game.current_piece.x + j) * BLOCK_SIZE,
                                        (self.game.current_piece.y + i) * BLOCK_SIZE,
                                        BLOCK_SIZE - 1,
                                        BLOCK_SIZE - 1))

    def _draw_next_piece(self):
        # Titre "Next"
        font = pygame.font.Font(None, 36)
        next_text = font.render('Next:', True, COLORS['text'])
        self.screen.blit(next_text, (GRID_WIDTH * BLOCK_SIZE + 50, 50))
        
        # Dessiner la prochaine pièce
        if not self.game.paused:
            for i, row in enumerate(self.game.next_piece.shape):
                for j, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self.screen,
                                       COLORS['pieces'][self.game.next_piece.type],
                                       (GRID_WIDTH * BLOCK_SIZE + 70 + j * BLOCK_SIZE,
                                        100 + i * BLOCK_SIZE,
                                        BLOCK_SIZE - 1,
                                        BLOCK_SIZE - 1))

    def _draw_stats(self):
        font = pygame.font.Font(None, 36)
        
        # Afficher les statistiques
        stats = [
            f'Score: {self.game.score}',
            f'Level: {self.game.level}',
            f'Lines: {self.game.lines}'
        ]
        
        for i, stat in enumerate(stats):
            stat_text = font.render(stat, True, COLORS['text'])
            self.screen.blit(stat_text, (GRID_WIDTH * BLOCK_SIZE + 50, 250 + i * 50))

    def _draw_game_messages(self):
        font = pygame.font.Font(None, 48)
        
        # Message de pause
        if self.game.paused:
            pause_text = font.render('PAUSE', True, COLORS['text'])
            text_rect = pause_text.get_rect(
                center=(GRID_WIDTH * BLOCK_SIZE // 2, 
                        GRID_HEIGHT * BLOCK_SIZE // 2)
            )
            self.screen.blit(pause_text, text_rect)
        
        # Message de game over
        if self.game.game_over:
            game_over_text = font.render('GAME OVER', True, COLORS['text'])
            text_rect = game_over_text.get_rect(
                center=(GRID_WIDTH * BLOCK_SIZE // 2, 
                        GRID_HEIGHT * BLOCK_SIZE // 2)
            )
            self.screen.blit(game_over_text, text_rect)

class Tetris:
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
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.ui = TetrisUI(self)

    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.level = 1
        self.lines = 0
        self.game_over = False
        self.paused = False

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
        rotated = list(zip(*shape[::-1]))
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

    def run(self):
        fall_time = 0
        fall_speed = 0.5  # Secondes entre chaque chute
        
        while True:
            # Gestion du temps
            self.clock.tick(60)
            if not self.paused:
                fall_time += self.clock.get_rawtime()
            
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                # Gestion de la souris
                if event.type == pygame.MOUSEMOTION:
                    for button in self.ui.buttons.values():
                        button.is_hovered(event.pos)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for name, button in self.ui.buttons.items():
                        if button.is_hovered(event.pos):
                            if name == 'pause':
                                self.paused = not self.paused
                            elif name == 'restart':
                                self.reset_game()
                            elif name == 'quit':
                                pygame.quit()
                                return
                
                if event.type == pygame.KEYDOWN:
                    # Contrôles du jeu uniquement si pas en pause et pas game over
                    if not self.paused and not self.game_over:
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
            
            # Chute automatique si pas en pause et pas game over
            if fall_time >= fall_speed * 1000 and not self.paused and not self.game_over:
                fall_time = 0
                if self.is_valid_move(self.current_piece.shape,
                                   self.current_piece.x,
                                   self.current_piece.y + 1):
                    self.current_piece.y += 1
                else:
                    self.place_piece()
            
            # Dessiner l'interface
            self.ui.draw()

if __name__ == '__main__':
    game = Tetris()
    game.run()