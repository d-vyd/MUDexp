"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter
from random import choice
from evennia import TICKER_HANDLER
from evennia import objects


class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """
    #pass
    
    def at_object_creation(self):
        """
        Called once, when this object is first created. This is the
        normal hook to overload for most object types.

        to force reload:
        @typeclass/force/reload objectname

        """
   
        self.db.rooms = list() # initialize a list of rooms visited
        self.db.doors = list() # initialize a list of doors used

class NPC(Character):
    
    def at_object_creation(self):
        self.db.rooms = list() # initialize a list of rooms visited
        self.db.doors = list() # initialize a list of doors used
        TICKER_HANDLER.add(15, self.think, idstring="NPC")
    
    def think(self):
        exits = [x for x in self.location.exits
                 if x.access(self, "traverse")]
        if exits:
            # scan the exits destination for targets
            exit_choice = choice(exits)
            self.move_to(exit_choice.destination)
        return
    
    