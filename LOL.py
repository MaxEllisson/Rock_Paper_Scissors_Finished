import tkinter as tk
from Rock_Paper_Scissors import Game, PlayerObject, RPS_OBJECTS, RPS_WIN_DICT
from functools import partial


class GameApp(tk.Tk):
    """ GameApp initialises a game and a Tk instance (window)
    The window includes a title and sets up frames with the different views on the game
    The show_frame method unpacks all the frames except for the one that needs to be shown """

    def __init__(self):
        super().__init__()
        self.game = create_game()
        title_string = ", ".join(obj.title() for obj in PlayerObject.allowable_objects) + " Game"

        
        self.title(title_string)
        self.resizable(False, False)


        title_label = tk.Label(self,
                               text=title_string,
                               bg="red", fg="white",
                               width=40,
                               font=("Arial", 20))
        title_label.pack(side=tk.TOP)


        self.frames = {
            "game_options": GameOptionsGUI(self),
            "main_game": GameGUI(self)}


        self.show_frame("game_options")


    def show_frame(self, current_frame: str):
        widgets = self.winfo_children()

        for w in widgets:
            if w.winfo_class() == "Frame":
                w.pack_forget()


        frame_to_show = self.frames[current_frame]
        frame_to_show.pack(expand=True, fill=tk.BOTH)
        frame_to_show.set_up()


class GameOptionsGUI(tk.Frame):
    """ GameOptionsGUI is a subclass of tk.Frame that allows the user to enter options and then start the game"""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.game = controller.game
        self.player = self.game.player


        self.user_name = tk.StringVar()
        self.num_rounds = tk.IntVar()

        name_label = tk.Label(self, text="Player Name:")
        rounds_label = tk.Label(self, text="Number of Rounds:")


        vcmd = (self.register(self.validate_entry), '%P')
        self.name_edit = tk.Entry(self, textvariable=self.user_name,
                                  name='editbox',
                                  validate='key',
                                  validatecommand=vcmd,
                                  justify=tk.CENTER, width=15)
        round_spin = tk.Spinbox(self, textvariable=self.num_rounds,
                                state='readonly',
                                from_=1, to=100, justify=tk.CENTER, width=13)
        self.start_button = tk.Button(self, text="Start game",
                                      state=tk.DISABLED,
                                      command=self.start_game,
                                      width=15)
        self.quit_button = tk.Button(self, text="Quit",
                                     width=15, command=self.controller.destroy)

        name_label.grid(row=1, column=0, pady=5)
        rounds_label.grid(row=2, column=0, pady=5)

        self.name_edit.grid(row=1, column=1, pady=5)
        round_spin.grid(row=2, column=1, pady=5)
        self.quit_button.grid(row=5, column=0, pady=(5, 10))
        self.start_button.grid(row=5, column=1, pady=(5, 10))


        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)


        self.controller.bind('<Return>', lambda event=None: self.start_button.invoke())


    def set_up(self):
        if self.game.players:
            self.user_name.set(self.player.name)
        if self.game.max_rounds:
            self.num_rounds.set(self.game.max_rounds)
        else:
            self.num_rounds.set(5)

        self.name_edit.focus()
        self.focus()

    def start_game(self):
        self.game.set_max_rounds(self.num_rounds.get())

        self.controller.show_frame("main_game")

    def validate_entry(self, user_name):
        if (0 < len(user_name) < 13) and user_name.isalpha():
            self.start_button.config(state=tk.NORMAL)
            self.player.set_name(user_name)
        elif len(user_name) == 0:
            self.start_button.config(state=tk.DISABLED)
        else:
            return False
        return True


class GameGUI(tk.Frame):
    def __init__(self, controller):

        super().__init__()

        self.controller = controller
        self.game = controller.game

        self.report_message = tk.StringVar()
        self.results_message = tk.StringVar()

        self.outcome = tk.Label(self, textvariable=self.report_message, bg="blue", fg="white", width=35)


        self.action_buttons = {player_obj: tk.Button(self, text=player_obj.title(),
                                                     width=15,
                                                     command=partial(self.select_object, player_obj),
                                                     )
                               for player_obj in PlayerObject.allowable_objects}

        self.quit_button = tk.Button(self, text="Quit", width=15, command=self.controller.destroy)
        self.restart_button = tk.Button(self, text="New game (N)", width=15, command=self.restart_game)
        self.options_button = tk.Button(self, text="Change Options (O)", width=15, command=self.reset_game)
        self.results = tk.Label(self, textvariable=self.results_message, height=2)

        for i, btn in enumerate(self.action_buttons.values(), 1):
            btn.grid(row=i, column=0, pady=5)

        num_buttons = len(self.action_buttons)
        self.outcome.grid(row=1, column=1, rowspan=3)
        self.results.grid(row=num_buttons+2, column=0, columnspan=2, pady=5)
        self.quit_button.grid(row=num_buttons+3, column=0, pady=(5, 10), rowspan=2)
        self.restart_button.grid(row=num_buttons+3, column=1, pady=5)
        self.options_button.grid(row=num_buttons+4, column=1, pady=(5, 10))


        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.bind('<Key>', self.press_key)

    def set_up(self):
        obj_str = ", ".join(PlayerObject.allowable_objects[:-1]) + f"\n or {PlayerObject.allowable_objects[-1]}"
        self.report_message.set(f"Choose {obj_str} to start")
        self.results_message.set(
            f"Welcome {self.game.players[0].name}. You have {self.game.max_rounds} rounds to play")
        self.focus()

    def press_key(self, event):
        key_pressed = event.char.lower()
        action_key_bindings = {"r": "rock",
                               "p": "paper",
                               "s": "scissors",
                               "l": "lizard",
                               "k": "spock",
                               }
        if key_pressed in action_key_bindings:
            self.action_buttons[action_key_bindings[key_pressed]].invoke()
        if key_pressed == "o":
            self.options_button.invoke()
        if key_pressed == "n":
            self.restart_button.invoke()
        if key_pressed == "q" or event.keysym == "Escape":
            self.quit_button.invoke()

    def select_object(self, item):
        self.game.next_round()
        self.game.players[0].choose_object(item)
        self.game.players[1].choose_object()
        self.game.find_winner()
        self.show_report()

    def show_report(self):
        if self.game.current_round == 0:
            self.set_up()
        else:
            self.report_message.set(self.game.report_round())
            result_msg = self.game.report_score()
            result_msg = result_msg.replace("\n", " ")

            if self.game.is_finished():
                result_msg += "\n" + self.game.report_winner()
                for btn in self.action_buttons.values():
                    btn.config(state=tk.DISABLED)
            else:
                result_msg += f"\nYou have {self.game.max_rounds - self.game.current_round} rounds left to play"

            self.results_message.set(result_msg)

    def restart_game(self):
        self.game.reset()
        self.show_report()
        for btn in self.action_buttons.values():
            btn.config(state=tk.NORMAL)

    def reset_game(self):
        self.restart_game()
        self.controller.show_frame("game_options")


def create_game():
    game = Game()
    game.player = game.add_human_player()
    game.add_computer_player()
    return game


if __name__ == "__main__":
    app = GameApp()
    app.mainloop()