'''
Created on Apr 5, 2023

@author: johnbotonakis
'''
import random
import tkinter as tk
from LifeBar import *
import time

def step(myEnv, cvs, count):
    global Bx, By
    # for each agent in the environment
    for a in myEnv.humans:
        if a.get_status() == "Sober" or a.get_status()=="Robot":
            # Decide which direction
            dx = random.randint(-1,1)
            dy = random.randint(-1,1)
            myX, myY = a.get_location()
            if a.get_status() == "Robot":
                ROBO_COORDS= (a.get_location())
                
            if myEnv.validMove(myX + dx, myY + dy):
                if myEnv.isEmpty(myX + dx, myY + dy):
                    # tell the agent that it has moved
                    a.move(dx, dy)
                    myEnv.vacate(myX, myY)
                    myEnv.place(a, myX + dx, myY + dy)
                else:
                    neighbor = myEnv.getHumanAt(myX + dx, myY + dy)
                    result = a.interact(neighbor)
                    
                    #TOO MUCH FAILURE
                    if result == -1:                                                #If blackout:
                        a.set_status("Blackout")                                    #Set their status accordingly,
                        a.Blackout()                                                #Make them blackout
                        myEnv.vacate(myX, myY)                                      #Destroy.
                    
                    #FAILURE    
                    elif result == 1:                                               #If the result of the flirt was UNSUCESSFUL,
                        drink_chance= random.randint(0,1)                           #The rejected has to think about getting a drink.
                        if drink_chance == 1:                                       #If the drink is chosen,
                            a.set_location(ROBO_COORDS)
                            a.move(ROBO_COORDS[0]-1,ROBO_COORDS[1]-1)
                            # a.get_drink()
                    
                    #SUCCESS       
                    elif result == 2:                                               #If the result of the flirt was successful,
                        myEnv.vacate(myX, myY)                                      #The flirter leaves
                        a.set_status("Left")                                        #Set the status as Left to stop rendering
                        nx, ny = neighbor.get_location()                            #Get the location of the flirt-ee(?)
                        myEnv.vacate(nx, ny)                                        #The Flirt-ee leaves
                        neighbor.set_status("Left")                                 #Changing their status to left
                        myEnv.spawn_near(myX + dx, myY + dy, type(neighbor))        #This will spawn two new patrons to the bar
                        myEnv.spawn_near(myX + dx, myY + dy, type(neighbor))        #This will spawn two new patrons to the bar
                    else:
                        pass
    
    myEnv.render(cvs)
    if count < 500:
        cvs.after(1000, lambda: step(myEnv, cvs, count + 1))
        
if __name__ == '__main__':

    wn = tk.Tk()
    cvs = tk.Canvas(wn, width = 500, height = 500)
    cvs.grid(row = 0,column = 0)
    
    play = tk.Button(wn,text = "Play", command =lambda:cvs.after(2000, lambda: step(myEnv, cvs, 400)))
    play.grid(row=1, column=0)
    
    Quit = tk.Button(wn, text = "Quit",command =lambda:cvs.quit() )
    Quit.grid(row = 1,column = 1)
    
    # Step = tk.Button(wn,text = "Step ->", command =lambda:time.sleep(input("Please hit a button to resume")))
    # Step.grid(row=1, column=2)
    
    verbose = True
    
    myEnv = LifeBar(10,10)
    myEnv.populate(6,6)
    
    counter = tk.Label(wn,text = f"Current Patrons: {len(myEnv.humans)}")
    counter.grid(row = 1, column = 2)
    
    
    wn.mainloop()
    
    
    
    
    
    # # step = tk.Button(wn,text = "Step ->", command = lambda:cvs.after(1000, lambda: step(myEnv, cvs, 0)))
    # step.grid(row=1, column=1)