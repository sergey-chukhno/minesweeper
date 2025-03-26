import customtkinter as ctk # Réalisation de l'UI
from PIL import Image # Pour charger l'image

"""NOTE : LEGEND
B_ = Button
T_ = Text
V_ = Value
"""

# Window creation
root = ctk.CTk(fg_color="lightgreen")
root.geometry("400x400")

# Variables
V_resolution = "400x400"
V_difficulty = int(1)
V_flag = 0
V_time = 0
V_question = 0

# Assets Loading
Ic_flag =  ctk.CTkImage(light_image=Image.open("assets/icon/flag.png"),size=(30,30))
Ic_clock = ctk.CTkImage(light_image=Image.open("assets/icon/clock.png"),size=(30,30))
Ic_question = ctk.CTkImage(light_image=Image.open("assets/icon/question.png"))

# Assets Labelling
flag_label = ctk.CTkLabel(root,image=Ic_flag,text="")
clock_label = ctk.CTkLabel(root,image=Ic_clock,text="")
question_label = ctk.CTkLabel(root,image=Ic_question,text="")

# Functions
def highlight_difficulty(choix):
    if choix == "Easy":
        B_difficulty.configure(fg_color="blue")
        root.geometry("400x400")
    if choix == "Medium":
        B_difficulty.configure(fg_color="Orange")
        root.geometry("650x650")
    if choix == "Hard":
        B_difficulty.configure(fg_color="Red")
        root.geometry("1000x1000")

# Buttons
B_difficulty = ctk.CTkOptionMenu(root, values=["Easy", "Medium", "Hard"], command=highlight_difficulty,fg_color="blue",button_color="black",width=75,height=23,corner_radius=10)
B_play = ctk.CTkButton(root,text="Play",font=("Helvetica",18),fg_color="red",text_color="white",hover_color="black",width=75,height=23,corner_radius=10)

# Text
T_title = ctk.CTkLabel(root,text="Minesweeper", font=("Arial",28))
T_flag = ctk.CTkLabel(root,text=str(V_flag),font=("Helvetica",18))
T_time = ctk.CTkLabel(root,text=str(V_time),font=("Helvetica",20))
T_question = ctk.CTkLabel(root,text=str(V_question),font=("Helvetica",20))






#NOTE : GRID

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)

B_difficulty.grid(row=0,column=0,padx=10,pady=10,sticky="nw")
flag_label.grid(row=0,column=1,padx=0,pady=10,sticky="nw")
T_flag.grid(row=0,column=1,padx=30,pady=10,sticky="nw")

question_label.grid(row=0,column=2,padx=10,pady=10,sticky="nw")
T_question.grid(row=0,column=2,padx=30,pady=10,sticky="nw")
clock_label.grid(row=0,column=3,padx=25,pady=10,sticky="ne")
T_time.grid(row=0,column=3,padx=10,pady=10,sticky="ne")

T_title.grid(row=1,column=0,columnspan=4,pady=10,sticky="n")


B_play.grid(row=2,column=0,columnspan=4,padx=10,pady=10,sticky="n")

# Window loop
root.mainloop()