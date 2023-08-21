'''
Created on Apr 15, 2023

@author: johnbotonakis
'''
from Human import *
import random
from LifeBar import *

if __name__ == '__main__':
    verbose = True
    
    myEnv = LifeBar(10,10)
    myEnv.populate(9, 10)
    print("Initial State")
    myEnv.print_environment()
    
    done = False
    step = 0
    
    while not done:
        step += 1
        
        # for each agent in the environment
        for a in myEnv.humans:
            # Decide which direction
            dx = random.randint(-1,1)
            dy = random.randint(-1,1)
            myX, myY = a.get_location()
            if myEnv.isEmpty(myX + dx, myY + dy):
                # tell the agent that it has moved
                a.move(dx, dy)
                myEnv.vacate(myX, myY)
                myEnv.place(a, myX + dx, myY + dy)
        
        if verbose:        
            print(f"Updated environment: Step {step}")
            myEnv.print_environment()
            input("Press 'enter' to continue'.")
        
        # Interactions
        # for each agent in the environment
        for a in myEnv.humans:
            # Look for my neighbors
            myX, myY = a.get_location()
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if not (dx == 0 and dy == 0) and not myEnv.isEmpty(myX + dx, myY + dy):
                        # interact
                        neighbor = myEnv.getHumanAt(myX + dx, myY + dy)
                        if neighbor != None:
                            a.interact(neighbor)