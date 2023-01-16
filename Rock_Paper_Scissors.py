"""

Module contains the class objects that control the underlying logic for rock-paper scissors game.
...
Classes
-------
    PlayerObject
    Player
    HumanPlayer (subclass of Player)
    ComputerPlayer (subclass of Player
    Game

"""
import random

# constants
RPSLS_OBJECTS = ('rock', 'paper', 'scissors', 'lizard', 'spock')
RPSLS_WIN_DICT = {'rock': ['scissors', 'lizard'],
                  'scissors': ['paper', 'lizard'],
                  'paper': ['rock', 'spock'],
                  'lizard': ['paper', 'spock'],
                  'spock': ['rock', '   scissors'],
                  }
RPS_OBJECTS = ('rock', 'paper', 'scissors')
RPS_WIN_DICT = {'rock': ['scissors'],
                'scissors': ['paper'],
                'paper': ['rock'],
                }


# PlayerObject represents an object that a player could choose
class PlayerObject:
    """
    A class to represent a playable object
    ...
    Attributes
    ----------
    name: str
        name of the object
    allowable_objects: tuple (class attribute)
        list of allowable objects
    win_dict: dict
        keys are allowable objects, values is list of what keys will beat
    Methods
    -------
    random_objects (class method)
        returns a PlayerObject randomly chosen from the allowable objects
    set_object_rules (class method)
        sets the allowable objects and the win_dict for what the object can beat
    """

    # Set default objects for the class
    allowable_objects = RPSLS_OBJECTS
    win_dict = RPSLS_WIN_DICT

    def __init__(self, name):


        """
        Constructs the attributes for the PlayerObject

        Parameters
        ----------
            name: str
                name of object - must be in allowable objects
        """
        name = name.lower()
        if name not in self.allowable_objects:
            raise ValueError(f'{name} is not an allowable object')
        self.name = name
        self.player = Player()

    @classmethod
    def random_object(cls):
        """ 
        Returns a random object from amongst the allowable objects
        """
        # The allowable objects are in cls.allowable_objects
        
        x = random.randint(0,len(cls.allowable_objects)-1)
        
        return cls.allowable_objects[x]

    @classmethod
    def set_object_rules(cls, allowable_objects, win_dict):
        """
        Sets the allowable objects and the win_dict for the class
        """
        # Leave this for now!
        ...
        cls.allowable_objects = allowable_objects
        cls.win_dict = win_dict


        
        return cls.allowable_objects

    def __eq__(self, other):
        """
        Returns True if the name attribute of self and other are the same
        """
        return self.name == other.name

    def __gt__(self, other):
        """
        Checks if the current object (self) beats the passed object (other), by checking win_dict
        """
        return other.name in self.win_dict[self.name]

    def __repr__(self):
        """
        Representation of the object
        """
        return f'PlayerObject("{self.name}")'


# The Player Class represents a player
class Player:
    """
    A class to represent a player of the game

    Attributes
    __________
        name: str
            Player name
        score: int
            Player score
        current_object: PlayerObject or None
            What the player's current object is None for not selected
    """

    def __init__(self, name=None):
        """
        Constructs the necessary attributes for the Player class
        """
        self.name = name
        self.current_object = None
        self.score = 0

    def set_name(self, name):
        """ Sets name attribute to name """
        self.name = name

    def reset_object(self):
        """ Sets the current_object to None - not selected"""
        self.current_object = None

    def win_round(self):
        """ Increases score by one """
        self.score += 1

    def __repr__(self):
        """ Representation of the object """
        check_object_chosen = bool(self.current_object)
        return f'Player: {self.name}\nScore: {self.score}\nObject chosen: {check_object_chosen}'


# The HumanPlayer Class is a subclass of Player representing a human player
class HumanPlayer(Player):
    """ Subclass of Player representing a human player (PC) """

    def choose_object(self, choice):
        """ Chooses a PlayerObject for the player"""
        self.current_object = PlayerObject(choice)


# The ComputerPlayer Class is a subclass of Player representing a Computer player
class ComputerPlayer(Player):
    """ Subclass of Player representing a Computer player (NPC) """

    def __init__(self):
        """ Constructs super Player object with name "Computer """
        super().__init__('Computer')
        

    def choose_object(self):
        """ Computer chooses a random PlayerObject """
        self.current_object = PlayerObject.random_object()


# The Game class contains the instructions for running the game
class Game:
    """
    A class representing the Rock, Paper Scissors Game
    Attributes
    __________
        allowable_objects (opt)
            list of allowable objects
        win_dict (opt)
            dict showing what objects the object in the key beats
        current_round: int
            the current round
        max_rounds: int
            the maximum rounds that can be played
        round_result
            None (not played), draw or win
        round_winner
            the PlayerObject for the round winner (None if no winner)
    """

    def __init__(self, allowable_objects=None, win_dict=None):
        if allowable_objects is None:
            allowable_objects = RPSLS_OBJECTS
        if win_dict is None:
            win_dict = RPSLS_WIN_DICT
        self.players = []
        self.current_round = 0
        self.set_max_rounds = 0
        self.round_result = None
        self.round_winner = None
        self.over = False
        PlayerObject.set_object_rules(allowable_objects, win_dict)
    def add_human_player(self, name=None):
        """ Add a human player with their name and appends it to players"""
        player = HumanPlayer(name)
        self.players.append(HumanPlayer(name))

    def add_computer_player(self):
        """ Add a computer player (no name) """
        
        self.players.append(ComputerPlayer())

    def set_max_rounds(self, mr):
        """ Set the maximum number of rounds """
        self.set_max_rounds = mr

    def find_winner(self):
        """ Finds the winner of the current round """
        if self.players[0].current_object > self.players[1].current_object:
            self.round_winner = self.players[0]
            self.round_result = 'Win'
        elif self.players[0].current_object == self.players[1].current_object:
            self.round_result = 'draw'
            self.round_winner = None
        else:
            self.round_winner = self.players[1] 
            self.round_result = 'Loss'

    def next_round(self):
        """ Resets game objects ready for a new round """
        self.current_round = self.current_round + 1
        self.round_result = None
        self.round_winner = None
        for player in self.players:
            player.reset_object()

    def is_finished(self):
        """ Checks if game is finished """
        if self.current_round == self.set_max_rounds:
            self.over = True

    def reset(self):
        """ Resets the whole game, setting current round to 0 and player scores to 0"""
        self.current_round = 0
        self.round_result = None
        self.round_winner = None
        for player in self.players:
            player.reset_object()
            player.score = 0

    def report_round(self):
        """ returns a message reporting on what the players played and what the result of the round was """
        
        return (f'You Played {self.players[0].current_object} and the Computer played {self.players[1].current_object}. {self.round_winner} Won!!')

    def report_score(self):
        """ Returns a string with the current scores """
        score_msg = f"After {self.current_round} rounds:\n"
        score_msg += "\n".join([f"{player.name} has scored {player.score}" for player in self.players])
        return score_msg

    def report_winner(self):
        """ Returns a message with the overall winner """
        return(f'The winner is {self.round_winner}!!')


