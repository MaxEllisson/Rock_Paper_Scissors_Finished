from tkinter import *
from Rock_Paper_Scissors import Game, PlayerObject, RPS_OBJECTS, RPS_WIN_DICT


root = Tk()
root.geometry('1440x720')
root.configure(bg='black')
root.title("Rock Paper Scizzors Lizard Spock")
root.resizable(False,False)

label_player = Label(root)
label_computer = Label(root)
label_computer.grid(row=1, column=0)
label_player.grid(row=1,column=4)

computer_score = Label(root,text=0)
player_score = Label(root,text=0)
player_score.grid(row=1,column=3)
computer_score.grid(row=1,column=0)


button_rock = Button(root,width=16,height=3,text='Rock').grid(row=2,column=1)

button_paper = Button(root,width=16,height=3,text='Paper').grid(row=3,column=1)
button_scizzors = Button(root,width=16,height=3,text='Scizzors').grid(row=4,column=1)
button_lizard = Button(root,width=16,height=3,text='Lizzard').grid(row=5,column=1)
button_spock = Button(root,width=16,height=3,text='Spock').grid(row=6,column=1)
root.mainloop()