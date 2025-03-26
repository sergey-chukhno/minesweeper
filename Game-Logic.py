import random
import time

class Minesweeper:
    def __init__(self, difficulty='intermediaire'):
        """
        Initialise le jeu de démineur avec un niveau de difficulté
        """
        self.difficulties = {
            'debutant': {'grid_size': (9, 9), 'min_mines': 10, 'max_mines': 15},
            'intermediaire': {'grid_size': (16, 16), 'min_mines': 40, 'max_mines': 50},
            'expert': {'grid_size': (24, 24), 'min_mines': 99, 'max_mines': 120}
        }
        
        self.current_difficulty = difficulty
        self.rows, self.cols = self.difficulties[difficulty]['grid_size']
        self.min_mines = self.difficulties[difficulty]['min_mines']
        self.max_mines = self.difficulties[difficulty]['max_mines']
        
        self.grid = None
        self.mines = None
        self.revealed = None
        self.flags = None
        
        self.game_over = False
        self.game_won = False
        self.first_click = True
        
        self.start_time = None
        self.total_time = 0

    def initialize_grid(self, first_click_row, first_click_col):
        """
        Initialise la grille avec les mines après le premier clic
        """
        # Créer une grille vide
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flags = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Générer un nombre aléatoire de mines
        num_mines = random.randint(self.min_mines, self.max_mines)
        self.mines = set()

        # Placer les mines en évitant la première case cliquée et ses adjacentes
        while len(self.mines) < num_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            
            # Vérifier que la mine n'est pas sur la case initiale ou adjacente
            if (row, col) != (first_click_row, first_click_col) and \
               not self._is_adjacent_to_first_click(row, col, first_click_row, first_click_col):
                if (row, col) not in self.mines:
                    self.mines.add((row, col))
                    self.grid[row][col] = -1  # -1 représente une mine
        
        # Calculer les nombres autour des mines
        self._calculate_adjacent_mines()

    def _is_adjacent_to_first_click(self, mine_row, mine_col, click_row, click_col):
        """
        Vérifie si une mine est adjacente à la première case cliquée
        """
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                adjacent_row, adjacent_col = click_row + dx, click_col + dy
                if (mine_row, mine_col) == (adjacent_row, adjacent_col):
                    return True
        return False

    def _calculate_adjacent_mines(self):
        """
        Calcule le nombre de mines adjacentes pour chaque case
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] != -1:
                    self.grid[row][col] = self._count_adjacent_mines(row, col)

    def _count_adjacent_mines(self, row, col):
        """
        Compte le nombre de mines adjacentes à une case
        """
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                new_row, new_col = row + dx, col + dy
                if (0 <= new_row < self.rows and 
                    0 <= new_col < self.cols and 
                    (new_row, new_col) in self.mines):
                    count += 1
        return count

    def reveal_cell(self, row, col):
        """
        Révèle une cellule et gère les différents scénarios
        """
        if self.first_click:
            self.initialize_grid(row, col)
            self.start_time = time.time()
            self.first_click = False

        if self.revealed[row][col] or self.flags[row][col]:
            return

        self.revealed[row][col] = True

        # Case mine
        if self.grid[row][col] == -1:
            self.game_over = True
            return

        # Case vide sans mines adjacentes
        if self.grid[row][col] == 0:
            self._reveal_empty_adjacent_cells(row, col)

        # Vérifier si le jeu est gagné
        self._check_win_condition()

    def _reveal_empty_adjacent_cells(self, row, col):
        """
        Révèle récursivement les cases vides adjacentes
        """
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                new_row, new_col = row + dx, col + dy
                if (0 <= new_row < self.rows and 
                    0 <= new_col < self.cols and 
                    not self.revealed[new_row][new_col]):
                    self.reveal_cell(new_row, new_col)

    def flag_cell(self, row, col):
        """
        Gère le placement des drapeaux et points d'interrogation
        """
        if not self.revealed[row][col]:
            if not self.flags[row][col]:
                self.flags[row][col] = True
            else:
                self.flags[row][col] = False

    def _check_win_condition(self):
        """
        Vérifie si le joueur a gagné
        """
        unrevealed_safe_cells = sum(
            1 for row in range(self.rows) 
            for col in range(self.cols) 
            if not self.revealed[row][col] and self.grid[row][col] != -1
        )
        
        if unrevealed_safe_cells == 0:
            self.game_won = True
            self.total_time = time.time() - self.start_time

    def reset_game(self):
        """
        Réinitialise le jeu
        """
        self.__init__(self.current_difficulty)

# Exemple d'utilisation
def main():
    game = Minesweeper('intermediaire')
    
    # Simuler quelques interactions
    game.reveal_cell(5, 5)  # Premier clic
    game.reveal_cell(6, 6)  # Révéler une autre case
    game.flag_cell(7, 7)    # Placer un drapeau

if __name__ == "__main__":
    main()