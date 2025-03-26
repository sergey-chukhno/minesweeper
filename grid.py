import customtkinter as ctk

# Configuration de la fenêtre
root = ctk.CTk()
root.geometry("400x400")  # Par défaut : mode facile
root.title("Minesweeper")

# Paramètres de la grille
MODES = {
    "Easy": {"size": 400, "rows": 8, "cols": 8},
    "Medium": {"size": 650, "rows": 12, "cols": 12},
    "Hard": {"size": 1000, "rows": 16, "cols": 16},
}

# Fonction pour créer la grille
def create_grid(rows, cols):
    # Supprime tous les widgets existants
    for widget in root.winfo_children():
        if isinstance(widget, ctk.CTkButton):  # Garde les autres éléments
            widget.destroy()

    # Création des cases du Minesweeper
    for r in range(rows):
        for c in range(cols):
            btn = ctk.CTkButton(root, text="", width=30, height=30)
            btn.grid(row=r, column=c, padx=2, pady=2)

    # Ajuster la grille pour qu'elle s'étire bien
    for i in range(rows):
        root.grid_rowconfigure(i, weight=1)
    for j in range(cols):
        root.grid_columnconfigure(j, weight=1)

# Fonction pour changer la difficulté
def change_difficulty(mode):
    data = MODES[mode]
    root.geometry(f"{data['size']}x{data['size']}")  # Changer la taille de la fenêtre
    create_grid(data["rows"], data["cols"])

# Bouton de sélection de difficulté
difficulty_menu = ctk.CTkOptionMenu(root, values=list(MODES.keys()), command=change_difficulty)
difficulty_menu.grid(row=0, column=0, columnspan=3, pady=10)

# Création de la grille initiale (mode facile)
create_grid(MODES["Easy"]["rows"], MODES["Easy"]["cols"])

root.mainloop()