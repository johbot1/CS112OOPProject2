'''
Created on Apr 15, 2023

@author: johnbotonakis
'''
from Human import *
import random
import tkinter as tk
from Pickup_lines import arrive
class LifeBar(object):
    '''
    classdocs
    '''


    
    def __init__(self, num_rows = 10, num_cols = 10):
        '''
        Constructor
        '''
        self.humans = []
        self.dimensions = [num_rows, num_cols]
        self.__grid = self.__create_grid(num_rows, num_cols)
    
    def __create_grid(self, rows, cols):
        temp = []
        for _ in range(rows):
            r = []
            for _ in range(cols):  
                r.append(None)
            temp.append(r)
        return temp
    
    def populate(self, n_men = 1, n_women = 5, n_bartender = 1):
        # Place the bartender first
        for _ in range(n_bartender):
            bartender = Bartender()
            valid_placement = False
            while not valid_placement:
                if self.isEmpty(0,0):
                    self.place(bartender, 0, 0)
                    self.humans.append(bartender)
                    valid_placement = True     
        
        # Place women next             
        for _ in range(n_women):
            new_woman = Woman()
            valid_placement = False
            while not valid_placement:
                x = random.randint(0, self.dimensions[1] - 1)
                y = random.randint(0, self.dimensions[0] - 1)
                if self.isEmpty(x,y):
                    self.place(new_woman, x, y)
                    self.humans.append(new_woman)
                    valid_placement = True     
        
        # Place the men
        for _ in range(n_men):
            new_man = Man()                                     #Make a new instance
            valid_placement = False                             #Set placement to false
            while not valid_placement:                          #While false,
                x = random.randint(0, self.dimensions[1] - 1)   #Generate a random X coord
                y = random.randint(0, self.dimensions[0] - 1)   #Generate a random Y coord
                if self.isEmpty(x,y):                           #If that spot is empty,
                    self.place(new_man, x, y)                   #Place a shark there
                    self.humans.append(new_man)                 #Append the list of agents with the new shark
                    valid_placement = True                      #Set the placement to True

    def getHumanAt(self, x, y):
        if 0 <= x < self.dimensions[1] and 0<=y < self.dimensions[0]:
            return self.__grid[y][x]
        else:
            return None 
                    
    def isEmpty(self, x, y):                                                #Check if the spot is empty
        if 0 <= x < self.dimensions[1] and 0<=y < self.dimensions[0]:       #If the provided coordinates are within the grid,
            return self.__grid[y][x] == None                                #Return None if there are nothin in that space
        else:                                                               #Otherwise
            return False                                                    #Returns False
        
    def validMove(self, x, y):                                              #Check if in bounds
        return 0 <= x < self.dimensions[1] and 0<=y < self.dimensions[0]    #Checking if in bounds
    
    def place(self, human, x, y):
        self.__grid[y][x] = human
        human.set_location([x,y])
        
    def vacate(self, x, y):
        self.__grid[y][x] = None
        
    def spawn_near(self, x, y, type):
        open = []
        # get all of the open spots nearby
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if self.isEmpty(x + dx,y + dy):
                    open.append([x + dx,y + dy])
        
        if len(open) > 0:
            newx, newy = random.choice(open)
            if type == Man:
                new_entity = Man()
                print(f"{arrive[random.randint(0,len(arrive)-1)]} It's {new_entity.name}!")
            else:
                new_entity = Woman()
                print(f"{arrive[random.randint(0,len(arrive)-1)]} It's {new_entity.name}!")
            self.place(new_entity, newx, newy)
            self.humans.append(new_entity)
        
        
    def print_environment(self):
        # mostly for testing purposes
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
        
                if self.__grid[i][j] == None:
                    print("_", end = '')
                else:
                    if type(self.__grid[i][j]) == Man:
                        print("M", end = '')
                    elif type(self.__grid[i][j]) == Woman:
                        print("W", end = '')
                    elif type(self.__grid[i][j]) == Bartender:
                        print("B", end = '')
                    else:
                        print("A", end = '')
            print()
            
    def render(self, cvs):
        cvs.delete(tk.ALL)
        rows = self.dimensions[0]
        cols = self.dimensions[1]
        width = int(cvs['width'])
        height = int(cvs['height'])
        
        w = (width - 10) // cols
        h = (height - 10) // rows
        cvs.create_rectangle(5, 5, width - 5, width - 5)
        for i in range(1, rows + 1):
            cvs.create_line(5, 5 + i*h, width - 5, 5 + i*h)
        for j in range(1, cols + 1):
            cvs.create_line(5 + j*w, 5, 5 + j*w, height - 5)
            
        for a in self.humans:
            if a.get_status() == "Sober" or a.get_status()=="Robot" or a.get_status()=="Rejected":
                a.draw(cvs, w)
        
if __name__ == '__main__':
    myEnv = LifeBar(10, 10)
    myEnv.populate(10, 8,1)
    myEnv.print_environment()
    
    import tkinter as tk
    wn = tk.Tk()
    cvs = tk.Canvas(wn, width = 400, height = 400)
    cvs.grid(row = 0,column = 0)

    # new_image = ImageTk.PhotoImage(Image.open("../img/Shark-L.png").resize((38,38)))
    #
    # cvs.create_image(6,6, anchor=tk.NW, image = new_image)        
    myEnv.render(cvs)
    wn.mainloop()
    
    