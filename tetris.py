import pygame
import random

# Initialisation
pygame.init()

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
CYAN = (0, 255, 255)
JAUNE = (255, 255, 0)
MAGENTA = (255, 0, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
ORANGE = (255, 165, 0)

# Paramètres du jeu
LARGEUR_BLOC = 30
HAUTEUR_BLOC = 30
COLONNES = 10
LIGNES = 20
LARGEUR = LARGEUR_BLOC * COLONNES
HAUTEUR = HAUTEUR_BLOC * LIGNES
VITESSE_INITIALE = 500  # Millisecondes

# Formes des pièces
PIECES = [
    [[1, 1, 1, 1]], # I
    [[1, 1], [1, 1]], # O
    [[1, 1, 1], [0, 1, 0]], # T
    [[1, 1, 1], [1, 0, 0]], # L
    [[1, 1, 1], [0, 0, 1]], # J
    [[1, 1, 0], [0, 1, 1]], # S
    [[0, 1, 1], [1, 1, 0]]  # Z
]

COULEURS = [CYAN, JAUNE, MAGENTA, ORANGE, BLEU, VERT, ROUGE]

class Piece:
    def __init__(self):
        self.forme = random.randint(0, len(PIECES) - 1)
        self.rotation = 0
        self.blocks = PIECES[self.forme]
        self.couleur = COULEURS[self.forme]
        self.x = COLONNES // 2 - len(self.blocks[0]) // 2
        self.y = 0

    def tourner(self):
        # Créer une nouvelle matrice pour la rotation
        ancienne_forme = self.blocks
        hauteur = len(self.blocks)
        largeur = len(self.blocks[0])
        nouvelle_forme = [[0 for x in range(hauteur)] for y in range(largeur)]
        
        for y in range(hauteur):
            for x in range(largeur):
                nouvelle_forme[x][hauteur-1-y] = ancienne_forme[y][x]
        
        return nouvelle_forme

class Tetris:
    def __init__(self):
        self.ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.grille = [[NOIR for x in range(COLONNES)] for y in range(LIGNES)]
        self.piece_courante = None
        self.game_over = False
        self.score = 0
        self.vitesse = VITESSE_INITIALE
        self.dernier_chute = pygame.time.get_ticks()

    def nouvelle_piece(self):
        self.piece_courante = Piece()

    def collision(self, piece, x_offset=0, y_offset=0):
        for y, ligne in enumerate(piece.blocks):
            for x, cellule in enumerate(ligne):
                if cellule:
                    nouveau_x = piece.x + x + x_offset
                    nouveau_y = piece.y + y + y_offset
                    if (nouveau_x < 0 or nouveau_x >= COLONNES or 
                        nouveau_y >= LIGNES or 
                        (nouveau_y >= 0 and self.grille[nouveau_y][nouveau_x] != NOIR)):
                        return True
        return False

    def fixer_piece(self):
        for y, ligne in enumerate(self.piece_courante.blocks):
            for x, cellule in enumerate(ligne):
                if cellule:
                    self.grille[self.piece_courante.y + y][self.piece_courante.x + x] = self.piece_courante.couleur

    def verifier_lignes(self):
        lignes_completes = 0
        y = LIGNES - 1
        while y >= 0:
            if NOIR not in self.grille[y]:
                del self.grille[y]
                self.grille.insert(0, [NOIR for _ in range(COLONNES)])
                lignes_completes += 1
            else:
                y -= 1
        if lignes_completes:
            self.score += lignes_completes * 100
            self.vitesse = max(100, VITESSE_INITIALE - (self.score // 1000) * 50)

    def dessiner(self):
        self.ecran.fill(NOIR)
        
        # Dessiner la grille
        for y in range(LIGNES):
            for x in range(COLONNES):
                pygame.draw.rect(self.ecran, self.grille[y][x],
                               (x * LARGEUR_BLOC, y * HAUTEUR_BLOC, LARGEUR_BLOC - 1, HAUTEUR_BLOC - 1))

        # Dessiner la pièce courante
        if self.piece_courante:
            for y, ligne in enumerate(self.piece_courante.blocks):
                for x, cellule in enumerate(ligne):
                    if cellule:
                        pygame.draw.rect(self.ecran, self.piece_courante.couleur,
                                       ((self.piece_courante.x + x) * LARGEUR_BLOC,
                                        (self.piece_courante.y + y) * HAUTEUR_BLOC,
                                        LARGEUR_BLOC - 1, HAUTEUR_BLOC - 1))

        pygame.display.flip()

    def executer(self):
        self.nouvelle_piece()
        
        while not self.game_over:
            temps_actuel = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if not self.collision(self.piece_courante, x_offset=-1):
                            self.piece_courante.x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if not self.collision(self.piece_courante, x_offset=1):
                            self.piece_courante.x += 1
                    elif event.key == pygame.K_UP:
                        nouvelle_forme = self.piece_courante.tourner()
                        ancienne_forme = self.piece_courante.blocks
                        self.piece_courante.blocks = nouvelle_forme
                        if self.collision(self.piece_courante):
                            self.piece_courante.blocks = ancienne_forme
                    elif event.key == pygame.K_DOWN:
                        if not self.collision(self.piece_courante, y_offset=1):
                            self.piece_courante.y += 1

            # Chute automatique
            if temps_actuel - self.dernier_chute > self.vitesse:
                if not self.collision(self.piece_courante, y_offset=1):
                    self.piece_courante.y += 1
                else:
                    self.fixer_piece()
                    self.verifier_lignes()
                    self.nouvelle_piece()
                    if self.collision(self.piece_courante):
                        self.game_over = True
                self.dernier_chute = temps_actuel

            self.dessiner()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    jeu = Tetris()
    jeu.executer()