Voici une version mise à jour du README pour refléter que le code a été entièrement généré par une IA (Claude.ai) et pour souligner l'impact de l'IA générative sur la prise de décision et la gestion du temps.

---

# Tetris Game - Select Difficulty

Ce projet est une implémentation du célèbre jeu **Tetris**, générée entièrement par une **IA** (Claude.ai). L'objectif principal est de démontrer l'efficacité de l'IA générative dans la réduction du temps de développement, en particulier dans la prise de décision et les processus managériaux.

## Fonctionnalités
- **Niveaux de difficulté** : Facile, Moyen, Difficile.
- **Formes des pièces** : 7 formes distinctes avec différentes couleurs.
- **Effets sonores** : Sons personnalisés pour des actions comme la rotation des pièces, la chute des pièces, la suppression des lignes et la fin du jeu.
- **Musique de fond** : Musique d'ambiance en boucle pour améliorer l'expérience de jeu.
- **Système de grille** : Une grille où les pièces de Tetris tombent et s'alignent.
- **Système de boutons** : Sélection de la difficulté via des boutons interactifs.

## Contexte du Projet
Ce projet a été entièrement généré par **Claude.ai**, une intelligence artificielle générative. Ce processus met en évidence l'impact potentiel de l'IA dans le développement logiciel, en particulier dans les domaines de la prise de décision rapide et de la gestion du temps. L'utilisation de l'IA a permis de :
- **Accélérer la prise de décision** : L'IA génère automatiquement le code en fonction des spécifications, réduisant ainsi le temps passé à la conception.
- **Optimiser les ressources managériales** : Les tâches répétitives et de codage basiques ont été automatisées, permettant aux équipes de se concentrer sur des aspects plus stratégiques.
- **Explorer les multiples possibilités de l'IA générative** : L'IA a généré des solutions créatives et efficaces pour la gestion des composants du jeu (son, graphisme, interactions, etc.).

## Installation et Configuration

### Prérequis
- **Python 3.x** : Assurez-vous que Python 3 est installé sur votre machine.
- **Bibliothèque Pygame** : Installez la bibliothèque Pygame via pip.

```bash
pip install pygame
```

### Ressources du jeu
Pour que le jeu fonctionne correctement, assurez-vous d’avoir les fichiers suivants dans votre répertoire de projet :
1. **Sons** :
   - `sounds/clear.wav`
   - `sounds/drop.wav`
   - `sounds/lateralmove.wav`
   - `sounds/levelup.wav`
   - `sounds/rotate.wav`
   - `sounds/select.wav`
   - `sounds/start.wav`
   - `sounds/tetris.wav`
   - `sounds/gameover.wav`
2. **Musique de fond** :
   - `sounds/background_music.mp3`

### Lancer le jeu
1. Clonez ou téléchargez le repository.
2. Placez les ressources du jeu (fichiers sonores) dans le dossier approprié.
3. Exécutez le script avec la commande suivante :

```bash
python tetris_game.py
```

Le jeu commencera avec un écran de sélection de difficulté. Choisissez la difficulté souhaitée pour commencer à jouer.

## Vue d'ensemble du code

### Constantes et Paramètres
- **GRID_SIZE** : Définie la taille de chaque bloc et les dimensions de la grille.
- **SCREEN_WIDTH et SCREEN_HEIGHT** : Déterminent la taille de la fenêtre de jeu.
- **SOUNDS** : Effets sonores prédéfinis pour différentes actions du jeu.
- **COLORS** : Couleurs utilisées dans le jeu pour l'arrière-plan, les lignes de grille et les pièces.
- **SHAPES** : Définit les formes des pièces de Tetris sous forme de grille.
- **DIFFICULTIES** : Configure les différents niveaux de difficulté, incluant la vitesse de chute et l'augmentation de la vitesse.

### Classes

- **Piece** : Représente une pièce de Tetris avec sa forme, sa position et son type.
- **Button** : Gère la création des boutons, leur dessin et les effets de survol pour la sélection de la difficulté.
- **DifficultySelect** : La classe principale pour l'écran de sélection de difficulté, avec des boutons interactifs pour choisir entre Facile, Moyen ou Difficile.

### Initialisation Pygame
Le script initialise Pygame et charge les ressources nécessaires (sons et polices). Il configure également la fenêtre d'affichage et gère les événements de survol de la souris sur les boutons de sélection de difficulté.

## Impact de l'IA Générative
Ce projet illustre l'énorme potentiel des **IA génératives** comme **Claude.ai** dans le domaine du développement logiciel. En générant rapidement des solutions logicielles efficaces et adaptées, l'IA permet non seulement de gagner du temps, mais aussi de libérer les équipes de tâches répétitives, leur permettant ainsi de se concentrer sur des aspects plus créatifs et stratégiques du projet.

## Contribuer
N'hésitez pas à forker le projet et à contribuer ! Si vous trouvez des bugs ou avez des suggestions d'amélioration, veuillez créer un problème ou soumettre une pull request.

<video controls src="Screen Recording 2024-11-27 113707.mp4" title="Title"></video>