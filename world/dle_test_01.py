# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 21:41:12 2018

@author: david
"""

from evennia import create_object, search_object
from typeclasses.objects import Object
from typeclasses.rooms import Room

from random import choice, randint

# SIZE OF MAX
max_x = 100
max_y = 100
max_ghosts = 500000

# INITIALIZE DICTIONARIES THAT TRACK DOORS
n_door = {}
s_door = {}
w_door = {}
e_door = {}
for x in range(max_x):
    for y in range(max_y):
        n_door[str(x)+"-"+str(y)]=False    # True means there is a door
        s_door[str(x)+"-"+str(y)]=False
        w_door[str(x)+"-"+str(y)]=False
        e_door[str(x)+"-"+str(y)]=False


# CREATE ROOMS
n=0
for x in range(max_x):
    for y in range(max_y):
        n += 1
        if n % 500:
            caller.msg("Creating room: "+str(n)+" of "+str(max_x*max_y))
        room = create_object("typeclasses.rooms.Room", key="ROOM_"+str(x)+"-"+str(y), aliases=["ROOM_"+str(x)+"-"+str(y)])
        room_type = choice(['courtyard','room','room','room','room','hallway'])
        if room_type == 'room' or room_type == "courtyard":
            size = choice(['small','small','small','small','medium-sized','medium-sized','large'])
            shape = choice(['rectangular','rectangular','rectangular','square','square','round','L-shaped','oddly shaped'])
            color = choice(['white','white','white','white','gray','gray','blue','red','green','yellow','orange'])
            desc = "A "+str(size)+", "+str(shape)+" "+str(room_type)+" with "+str(color)+" walls."
            if room_type == "room":
                ceiling = choice(["a low ceiling","a high celing","an arched ceiling","a skylight","a design on the ceiling"])
                desc = desc + " It has "+str(ceiling)+"."
                if randint(1,10) <= 3:
                    desc = desc + " There are a few pictures on the walls."
            if room_type == "courtyard":
                ground = choice(["decorative tiles","brown dirt","black dirt","rust-colored dirt","green grass","yellowish grass"])
                desc = desc + " The ground is covered with "+str(ground)+"."
        if room_type == 'hallway':
            length = choice(["long","short"])
            width = choice(["wide","narrow"])
            shape = choice(["winding","straight","L-shaped"])
            floor = choice(["flat", "slanted"])
            desc = "a "+str(length)+", "+str(width)+", "+str(shape)+" "+str(room_type)+". The floor is "+str(floor)+"." 
        room.db.desc = desc


# CREATE THE MAIN CONNECTION BETWEEN LIMBO AND THE MAZE
loc_str = "limbo"
dest_str = "ROOM_0-0"
loc_obj = search_object(loc_str)[0]
dest_obj = search_object(dest_str)[0]

string='a large door with the label "Entrance to Maze"'
main_entrance = create_object("typeclasses.exits.Exit", key=string, location=loc_obj, destination=dest_obj, aliases=["in"])
main_entrance.db.facing = 's'
main_entrance.db.loc = loc_str
main_entrance.db.dest = dest_str
  
string = 'a large door with the label "Exit from Maze"'
main_exit = create_object("typeclasses.exits.Exit", key=string, location=dest_obj, destination=loc_obj, aliases=["out"])
main_exit.db.facing = 'n'
main_exit.db.loc = dest_str
main_exit.db.dest = loc_str

n_door["0-0"]=True

n=0

#CREATE THE OTHER DOORS OF THE MAZE
for x in range(max_x):
    for y in range(max_y):
        n += 1
        if n % 500:
            caller.msg("Creating exit: "+str(n)+" of "+str(max_x*max_y*3))
        # By default, it is fine to add a door
        north_ok = True
        south_ok = True
        west_ok = True
        east_ok = True

        # If there is already a door, don't add another one
        if n_door[str(x)+"-"+str(y)]:
            north_ok = False
        if s_door[str(x)+"-"+str(y)]:
            south_ok = False            
        if w_door[str(x)+"-"+str(y)]:
            west_ok = False            
        if e_door[str(x)+"-"+str(y)]:
            east_ok = False        
    
        # No doors should lead to empty space outside the maze
        if x==0:
            west_ok = False
        if y==0:
            north_ok = False
        if x==max_x-1:
            east_ok = False
        if y==max_y-1:
            south_ok = False
            
        # Determine how many doors to add by scaling the random maximum
        # by the number of doors that are already in the room. 
        # If room has no doors, at least one needs to be added.
        
        if west_ok+north_ok+east_ok+south_ok == 0:
            doors_to_add=0
            
        if west_ok+north_ok+east_ok+south_ok == 1:
            doors_to_add=randint(0,1)
            
        if west_ok+north_ok+east_ok+south_ok == 2:
            doors_to_add=randint(0,2)        
        
        if west_ok+north_ok+east_ok+south_ok == 3:
            doors_to_add=randint(1,3)            

        if west_ok+north_ok+east_ok+south_ok == 4:
            doors_to_add=randint(2,4)      

        
        # Add those doors!
        for n in range(doors_to_add):
            door_ok = False
            string = "Door made without name assigned!"   # A door with this name reflects and error!
            while not door_ok:
                door=choice(['n','s','e','w'])
                if door=='n' and north_ok:
                    door_ok = True
                    dest_x = x
                    dest_y = y-1
                if door=='s' and south_ok:
                    door_ok = True
                    dest_x = x
                    dest_y = y+1
                if door=='w' and west_ok:
                    door_ok = True
                    dest_x = x-1
                    dest_y = y
                if door=='e' and east_ok:
                    door_ok = True
                    dest_x = x+1
                    dest_y = y
                if door_ok:
                    shape = choice(['door','revolving door','iris portal','hole in the wall'])
                    if shape == 'door':
                        color = choice(['natural wood','red','yellow','blue','green','black','gray','white','orange'])
                    if shape == 'revolving door':
                        color = choice(['clear glass','blue glass','green glass'])
                    if shape == 'iris portal':
                        color = choice(['copper','silver','gold','steel','gray','rusted'])
                    if shape == 'hole in the wall':
                        color = choice(['roughtly person-sized','giant','crumbling','triangular'])
                    if shape == 'iris portal':
                        string = 'a circular, '+str(color)+' '+shape
                    else:
                        string = 'a '+str(color)+' '+shape
                    
                    
                    loc_str = "ROOM_"+str(x)+"-"+str(y)
                    dest_str = "ROOM_"+str(dest_x)+"-"+str(dest_y)
                    
                    loc_obj = search_object(loc_str)[0]
                    dest_obj = search_object(dest_str)[0]
                    
                    # create alias by counting up the doors in the room and adding one
                    door_count = n_door[str(x)+"-"+str(y)] + s_door[str(x)+"-"+str(y)] + w_door[str(x)+"-"+str(y)] + e_door[str(x)+"-"+str(y)]
                    alias = str(door_count+1)
                    temp = create_object("typeclasses.exits.Exit", key=string, location=loc_obj, destination=dest_obj, aliases=[alias])
                    temp.db.facing = door
                    temp.db.loc = loc_str
                    temp.db.dest = dest_str
                    
                    # create door in the opposite direction
                    door_count = n_door[str(dest_x)+"-"+str(dest_y)] + s_door[str(dest_x)+"-"+str(y)] + w_door[str(dest_x)+"-"+str(dest_y)] + e_door[str(dest_x)+"-"+str(dest_y)]
                    alias = str(door_count+1)
                    temp = create_object("typeclasses.exits.Exit", key=string, location=dest_obj, destination=loc_obj, aliases=[alias])
                    if door == 'n':
                        temp.db.facing = 's'
                    if door == 's':
                        temp.db.facing = 'n'                        
                    if door == 'e':
                        temp.db.facing = 'w'
                    if door == 'w':
                        temp.db.facing = 'e'
                    temp.db.loc = dest_str
                    temp.db.dest = loc_str

                    # update dictionaries with new door locations for this room and destination
                    if door=='s':
                        s_door[str(x)+"-"+str(y)]=True
                        n_door[str(dest_x)+"-"+str(dest_y)]=True
                    if door=='n':
                        n_door[str(x)+"-"+str(y)]=True
                        s_door[str(dest_x)+"-"+str(dest_y)]=True                        
                    if door=='e':
                        e_door[str(x)+"-"+str(y)]=True
                        w_door[str(dest_x)+"-"+str(dest_y)]=True                         
                    if door=='w':
                        w_door[str(x)+"-"+str(y)]=True
                        e_door[str(dest_x)+"-"+str(dest_y)]=True                         

                    # If we are adding more doors to the same room, we need to check these again
                    if n_door[str(x)+"-"+str(y)]:
                        north_ok = False
                    if s_door[str(x)+"-"+str(y)]:
                        south_ok = False            
                    if w_door[str(x)+"-"+str(y)]:
                        west_ok = False            
                    if e_door[str(x)+"-"+str(y)]:
                        east_ok = False  

# Add ghosts to maze
                        
for n in range(0,max_ghosts):
    if n % 500:
        caller.msg("Creating exit: "+str(n)+" of "+str(max_ghosts))
    x=randint(0,max_x-1)
    y=randint(0,max_y-1)
    loc_str = "ROOM_"+str(x)+"-"+str(y)
    loc_obj = search_object(loc_str)[0]
    key_str = "ghost_"+str(n)
    ghost = create_object("typeclasses.characters.NPC", key=key_str, location=loc_obj, destination=None, aliases=[])
    ghost.db.desc = "a scary ghost"

