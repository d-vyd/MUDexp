# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 21:26:33 2018

@author: david
"""

# Add ghosts to maze

from evennia import create_object, search_object
from typeclasses.objects import Object
from typeclasses.rooms import Room
from random import randint

# SIZE OF MAX
max_x = 100
max_y = 100
max_ghosts = 500000


for n in range(1000,max_ghosts):
    if n % 500 == 0:
        caller.msg("Creating ghost: "+str(n)+" of "+str(max_ghosts))
    x=randint(0,max_x-1)
    y=randint(0,max_y-1)
    loc_str = "ROOM_"+str(x)+"-"+str(y)
    loc_obj = search_object(loc_str)[0]
    key_str = "ghost_"+str(n)
    ghost = create_object("typeclasses.characters.NPC", key=key_str, location=loc_obj, destination=None, aliases=[])
    ghost.db.desc = "a scary ghost"

