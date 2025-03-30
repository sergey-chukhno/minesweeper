class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_revealed = False
        self.adjacent_mines = 0
        self.state = 'covered'  # "covered" -> cellule cachée

    def reveal(self):
        """ Révèle la cellule et met à jour son état """
        self.is_revealed = True
        self.state = 'revealed'

    def get_state(self):
        """ Retourne l'état actuel de la cellule (pour afficher dans le terminal) """
        return self.state[0].upper()  # Première lettre de l'état (C, R, F, etc.)

class GridManager:
    def __init__(self, rows, cols):
        self.grid = [[Cell(row, col) for col in range(cols)] for row in range(rows)]

    def print_grid(self):
        """ Affiche la grille dans le terminal """
        for row in self.grid:
            print(' '.join([cell.get_state() for cell in row]))

    def reveal_cell(self, row, col):
        """ Révèle une cellule spécifique et affiche la grille """
        cell = self.grid[row][col]
        cell.reveal()
        self.print_grid()

# main pour démarrer et tester
if __name__ == "__main__":
    grid_manager = GridManager(5, 5)  
    grid_manager.print_grid()  

    
    print("\nAprès révélation de la cellule (2, 2) :")
    grid_manager.reveal_cell(2, 2)  


    
