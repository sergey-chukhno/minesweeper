import random

class Cell:
    def __init__(self, grid_manager, row, col, size):
        self.grid_manager = grid_manager  
        self.row = row 
        self.col = col  
        self.size = size  
        self.is_mine = False  
        self.is_revealed = False 
        self.adjacent_mines = 0  
        self.state = 'covered'  

    def set_mine(self, is_mine):
        """ Définit si la cellule est une mine """
        self.is_mine = is_mine
    
    def set_adjacent_mines(self, count):
        """ Définit le nombre de mines adjacentes à la cellule """
        self.adjacent_mines = count
    
    def toggle_mark(self):
        """ Alterne entre marquer avec un drapeau, un point d'interrogation ou réinitialiser l'état """
        if self.state == 'covered':
            self.state = 'flagged'
        elif self.state == 'flagged':
            self.state = 'question_mark'
        elif self.state == 'question_mark':
            self.state = 'covered'
    
    def reveal(self):
        """ Révèle la cellule et met à jour l'état de l'interface """
        self.is_revealed = True
        self.state = 'revealed'  # état apres révélation
    
    def highlight_mine(self, exploded=False):
        """ Met en évidence la cellule si c'est une mine (explosée ou non) """
        self.state = 'exploded' if exploded else 'mine'

    def highlight_wrong_flag(self):
        """ Met en évidence un mauvais drapeau placé sur une cellule sans mine """
        self.state = 'wrong_flag'

    def is_flagged(self):
        """ Vérifie si la cellule est marquée avec un drapeau """
        return self.state == 'flagged'

    def is_question(self):
        """ Vérifie si la cellule est marquée avec un point d'interrogation """
        return self.state == 'question_mark'

    def is_covered(self):
        """ Vérifie si la cellule est couverte (non révélée) """
        return self.state == 'covered'

    def get_state(self):
        """ Retourne l'état actuel de la cellule """
        return self.state
