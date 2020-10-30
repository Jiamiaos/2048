# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 15:59:50 2020
Game "2048"
@author: JiamiaoSun
"""


'''
#================================================
"""
This part enable keyboard monitor, so the player doesn't have to press enter after
type in each move. However, it required module pynput which is not supported on
colaboratoray. Further works will apply this function and a choice between keyboard.listener 
and straightforward input.
"""
from pynput import keyboard

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
'''

import random
import numpy as np
from IPython.display import clear_output

#================================================
#============Genrate New Number==================
#================================================

#Generate a new number after each move.
def add(n):
    num=random.choice([2,4])
    x=random.randint(0,3)
    y=random.randint(0,3)#Pick a random number to be generated and a random position.
    
    if n==0:#==========0 refers to initialize the first number.
        Map[x][y]=num
        
    elif n==1:#========1 refers to generating after the move to the upside.
        if Map[3][y]==0:#If there is no number on the picked position, put the number here.
            Map[3][y]=num
        else:#Else, put the number on the first blank from left to right.
            for i in range(4):
                if Map[3][i]==0:
                    Map[3][i]=num
                    break
                
    elif n==2:#========2 refers to generating after the move to the downside.
        if Map[0][y]==0:
            Map[0][y]=num
        else:
            for i in range(4):
                if Map[0][i]==0:
                    Map[0][i]=num
                    break
    
    elif n==3:#========3 refers to generating after the move to the left.
        if Map[x][3]==0:
            Map[x][3]=num
        else:
            for i in range(4):
                if Map[i][3]==0:
                    Map[i][3]=num
                    break
    
    elif n==4:#========4 refers to generating after the move to the right.
        if Map[x][0]==0:
            Map[x][0]=num
        else:
            for i in range(4):
                if Map[i][0]==0:
                    Map[i][0]=num
                    break
        
    return

#================================================
#============Move the Whole Map==================
#================================================
    
#This function makes the whole Map move up.
def moveup():
    tf=0#Denote whether a move is success or not.
    global score
    global Map
    global goal
    for j in range(4):#====Iterating across all four columns.
        n=4
        while(n):#Repeat to make sure each bolck has been moved to the furthest place.
            n-=1
            for i in range(3):
                if Map[i][j]==0:
                    for t in range(i,3):#If there is a blank above a certain block, move it up.
                        Map[t][j]=Map[t+1][j]
                        Map[t+1][j]=0
                        tf=1
            for i in range(3):#If two blocks could be merged, add them up.
                if Map[i][j]==Map[i+1][j]:
                    Map[i][j]*=2
                    score+=Map[i][j]#Player earns points after a merge.
                    if Map[i][j]>=goal:#End the game after reaching the goal.
                        return 2
                    for t in range(i+1,3):#Move the other blocks after the merge.
                        Map[t][j]=Map[t+1][j]
                        Map[t+1][j]=0
                    tf=1
    if tf:
        add(1)#Generate a new number after move successfully.
    return tf

#This function makes the whole Map move down.
def movedown():
    tf=0
    global score
    global Map
    global goal
    for j in range(4):
        n=4
        while(n):
            n-=1
            for i in range(3,0,-1):
                if Map[i][j]==0:
                    for t in range(i,0,-1):
                        Map[t][j]=Map[t-1][j]
                        Map[t-1][j]=0
                        tf=1
            for i in range(3,0,-1):
                if Map[i][j]==Map[i-1][j]:
                    Map[i][j]*=2
                    score+=Map[i][j]
                    if Map[i][j]>=goal:
                        return 2
                    for t in range(i-1,0,-1):
                        Map[t][j]=Map[t-1][j]
                        Map[t-1][j]=0
                    tf=1
    if tf:
        add(2)
    return tf

#This function makes the whole Map move to the left.
def moveleft():
    tf=0
    global score
    global Map
    global goal
    for i in range(4):#====Iterating across all four rows.
        n=4
        while(n):
            n-=1
            for j in range(3):
                if Map[i][j]==0:
                    for t in range(j,3):
                        Map[i][t]=Map[i][t+1]
                        Map[i][t+1]=0
                        tf=1
            for j in range(3):
                if Map[i][j]==Map[i][j+1]:
                    Map[i][j]*=2
                    score+=Map[i][j]
                    if Map[i][j]>=goal:
                        return 2
                    for t in range(j+1,3):
                        Map[i][t]=Map[i][t+1]
                        Map[i][t+1]=0
                    tf=1
    if tf:
        add(3)
    return tf

#This function makes the whole Map move to the right.
def moveright():
    tf=0
    global score
    global Map
    global goal
    for i in range(4):
        n=4
        while(n):
            n-=1
            for j in range(3,0,-1):
                if Map[i][j]==0:
                    for t in range(j,0,-1):
                        Map[i][t]=Map[i][t-1]
                        Map[i][t-1]=0
                        tf=1
            for j in range(3,0,-1):
                if Map[i][j]==Map[i][j-1]:
                    Map[i][j]*=2
                    score+=Map[i][j]
                    if Map[i][j]>=goal:
                        return 2
                    for t in range(j-1,0,-1):
                        Map[i][t]=Map[i][t-1]
                        Map[i][t-1]=0
                    tf=1
    if tf:
        add(4)
    return tf

#================================================
#============Other Parts=========================
#================================================

#This function reads the command of moving direction.
def move():
    tf=0
    print('Next move:')
    key=input()
    if key=='w' or key=='W':
        tf=moveup()
    elif key=='a' or key=='A':
        tf=moveleft()
    elif key=='s' or key=='S':
        tf=movedown()
    elif key=='d' or key=='D':
        tf=moveright()
    else:
        tf=44
    return tf
                
#This function checks whether able to continue or not.
def check():
    global Map
    for i in range(4):
        for j in range(1,4):
            if Map[i][j]==Map[i][j-1]:
                return 1
    for i in range(1,4):
        for j in range(4):
            if Map[i][j]==Map[i-1][j]:
                return 1
    for i in range(4):
        for j in range(4):
            if Map[i][j]==0:
                return 1
    return 0


#This function prints the table as the game interface.
def maketable():
    print(''.center(40,'='))
    print('<<<<  2048  >>>>'.center(40,'='))
    print('*Super Plain Version'.center(40,'='))
    print(''.center(40,'='))
    print("Use WASD to control the moves.\nGood luck!")
    print('\t【Score: %d】'%score)
    print('\t+----+----+----+----+')
    print('\t|%4d|%4d|%4d|%4d|'%(Map[0][0],Map[0][1],Map[0][2],Map[0][3]))
    print('\t+----+----+----+----+')
    print('\t|%4d|%4d|%4d|%4d|'%(Map[1][0],Map[1][1],Map[1][2],Map[1][3]))
    print('\t+----+----+----+----+')
    print('\t|%4d|%4d|%4d|%4d|'%(Map[2][0],Map[2][1],Map[2][2],Map[2][3]))
    print('\t+----+----+----+----+')
    print('\t|%4d|%4d|%4d|%4d|'%(Map[3][0],Map[3][1],Map[3][2],Map[3][3]))
    print('\t+----+----+----+----+')
    
#================================================
#============Main Part===========================
#================================================    

Map=np.zeros([4,4],dtype=int)#Control the Map of this game.
score=0#Total score of the player.
goal=128#You can set the goal point of your play.

add(0)
maketable()
while(True):
    mov=move()
    if mov==1:
        clear_output(wait=True)
        maketable()
    elif mov==44:
        print('<<Invalid input>> Use WASD to control moving.')
    elif mov==2:
        print('Wow! You are GENIUS!!!')
        print('Congratulation!')
        break
    elif mov==0:
        life=check()
        if not life:
            print('Boom! No more moves possible.')
            print('HaHaHa u idiot!')
            break
        else:
            print("This won't help. Try another direction.")
