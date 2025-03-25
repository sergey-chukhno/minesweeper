import random

class Demineur:
    def __init__(self, taille=10, nb_mines=10):
        """
        Initialise une partie de démineur
        
        :param taille: Taille de la grille (par défaut 10x10)
        :param nb_mines: Nombre de mines (par défaut 10)
        """
        self.taille = taille
        self.nb_mines = nb_mines
        
        # Création de la grille
        self.grille = [[0 for _ in range(taille)] for _ in range(taille)]
        self.mines = [[False for _ in range(taille)] for _ in range(taille)]
        self.cases_revelees = [[False for _ in range(taille)] for _ in range(taille)]
        self.drapeaux = [[False for _ in range(taille)] for _ in range(taille)]
        
        # Placement des mines
        self._placer_mines()
        
    def _placer_mines(self):
        """
        Place les mines aléatoirement sur la grille
        """
        mines_placees = 0
        while mines_placees < self.nb_mines:
            x = random.randint(0, self.taille - 1)
            y = random.randint(0, self.taille - 1)
            
            if not self.mines[x][y]:
                self.mines[x][y] = True
                mines_placees += 1
        
        # Calcul des nombres autour des mines
        for x in range(self.taille):
            for y in range(self.taille):
                if not self.mines[x][y]:
                    self.grille[x][y] = self._compter_mines_adjacentes(x, y)
        
    def _compter_mines_adjacentes(self, x, y):
        """
        Compte le nombre de mines adjacentes à une case
        
        :param x: Coordonnée x
        :param y: Coordonnée y
        :return: Nombre de mines adjacentes
        """
        nb_mines = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.taille and 
                    0 <= ny < self.taille and 
                    self.mines[nx][ny]):
                    nb_mines += 1
        return nb_mines
    
    def reveler_case(self, x, y):
        """
        Révèle une case et gère la logique de révélation
        
        :param x: Coordonnée x
        :param y: Coordonnée y
        :return: True si la partie continue, False si mine explose
        """
        # Vérification des coordonnées
        if (x < 0 or x >= self.taille or 
            y < 0 or y >= self.taille or 
            self.cases_revelees[x][y]):
            return True
        
        # Vérification de la mine
        if self.mines[x][y]:
            return False
        
        # Révèle la case
        self.cases_revelees[x][y] = True
        
        # Révélation récursive des cases vides
        if self.grille[x][y] == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    self.reveler_case(x + dx, y + dy)
        
        return True
    
    def placer_drapeau(self, x, y):
        """
        Place ou retire un drapeau
        
        :param x: Coordonnée x
        :param y: Coordonnée y
        """
        if not self.cases_revelees[x][y]:
            self.drapeaux[x][y] = not self.drapeaux[x][y]
    
    def verifier_victoire(self):
        """
        Vérifie si le joueur a gagné
        
        :return: True si victoire, False sinon
        """
        for x in range(self.taille):
            for y in range(self.taille):
                if not self.mines[x][y] and not self.cases_revelees[x][y]:
                    return False
        return True
    
    def afficher_grille(self):
        """
        Affiche l'état actuel de la grille
        """
        for x in range(self.taille):
            ligne = []
            for y in range(self.taille):
                if self.drapeaux[x][y]:
                    ligne.append('🚩')
                elif not self.cases_revelees[x][y]:
                    ligne.append('■')
                elif self.mines[x][y]:
                    ligne.append('💥')
                elif self.grille[x][y] > 0:
                    ligne.append(str(self.grille[x][y]))
                else:
                    ligne.append('□')
            print(' '.join(ligne))

# Exemple d'utilisation
def jouer():
    """
    Fonction principale pour jouer au démineur
    """
    jeu = Demineur()
    
    while True:
        jeu.afficher_grille()
        
        # Logique de jeu simplifiée (à compléter avec une interface utilisateur)
        action = input("Entrez l'action (r x y pour révéler, d x y pour drapeau) : ").split()
        
        if len(action) != 3:
            print("Action invalide!")
            continue
        
        action_type, x, y = action[0], int(action[1]), int(action[2])
        
        try:
            if action_type == 'r':
                if not jeu.reveler_case(x, y):
                    print("Boom! Vous avez perdu!")
                    jeu.afficher_grille()
                    break
            elif action_type == 'd':
                jeu.placer_drapeau(x, y)
            
            if jeu.verifier_victoire():
                print("Félicitations! Vous avez gagné!")
                break
        
        except IndexError:
            print("Coordonnées invalides!")

# Décommenter pour lancer le jeu
jouer()