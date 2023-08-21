'''
Created on Apr 15, 2023
Game of Life Cells
@author: johnbotonakis
'''
import random
from PIL import Image, ImageTk
import tkinter as tk
from Pickup_lines import *
import random
class Human (object):
    '''
    classdocs
    '''
    @classmethod
    def _load_image(cls, filename, dim = 40):       #Load the image to the proper class
        try:
            temp = Image.open(f"./img/{filename}")  #Using the provided file in the INIT, open the image
            temp = temp.resize((dim-2, dim-2))      #Resize the Image
            temp = ImageTk.PhotoImage(temp)         #Set the image in TK
            return temp                             #Return the modified image
        except FileNotFoundError:
            print(f"File '{filename}' cannot be found in the directory './img'.")
        except:
            print("An error occurred loading your image")

    def __init__(self):
        '''
        Constructor
        '''
        self.__location = [0,0]
        self.status = "Sober"
        self._image = None 
        self.__intelligence = random.randint(10,100)
        self.__charisma = random.randint(50,100)
        self.__ConsumedDrinks = 0
    
    def get_drink(self):          
        if self.get_ConsumedDrinks()<9:                                            #If they haven't had too many drinks,
            self.set_ConsumedDrinks((self.get_ConsumedDrinks())+1)                  #Drink to forget
            self.set_intelligence(int(self.get_intelligence())-10)                  #Drinks take off intelligence points
            self.set_charisma(self.get_charisma()+10)                               #But drinks also increase charisma
            print(f"{self.name} took a drink and their intelligence lowered to {self.get_intelligence()}, but charisma increased to {self.get_charisma()}") #Announce lowering of intelligence
        else:                                                                       #OTHERWISE, if they have had over 10 drinks,
            self.set_ConsumedDrinks(self.get_ConsumedDrinks()+1)                    #Set the amount of drinks to too much
            self.Blackout()
            
    def Blackout(self):
        self.set_status("Blackout")
        print(f"{self.name} drank too much!")
        
    def get_intelligence(self):
        return self.__intelligence

    def get_charisma(self):
        return self.__charisma

    def get_happy(self):
        return self.__happy

    def get_image(self):
        return self.__image
    
    def get_location(self):
        return self.__location

    def get_status(self):
        return self.status
    
    def get_ConsumedDrinks(self):
        return self.__ConsumedDrinks

    def set_location(self, value):
        self.__location = value

    def set_status(self, value):
        self.status = value

    def set_intelligence(self, value):
        self.__intelligence = value

    def set_charisma(self, value):
        self.__charisma = value

    def set_happy(self, value):
        self.__happy = value

    def set_image(self, value):
        self.__image = value
    
    def set_ConsumedDrinks(self,value):
        self.__ConsumedDrinks = value

    def draw(self, cvs, dim):           #This will tell where to draw the image
        
        x, y = self.get_location()      #Get the location
        if self._image != None:         #If free
            cvs.create_image(6 + x*dim, 6 + y * dim, anchor = tk.NW, image = self._image) #Put the image at that spot

    def move(self, deltaX, deltaY):
        self.__location[0] += deltaX
        self.__location[1] += deltaY

class Man (Human):
    def __init__(self):
        super().__init__()
        self.name = mnames[random.randint(0,len(mnames)-1)]
        self._image = Human._load_image(f"m{random.randint(1,len(mnames)-1)}.png")
        self.attempted = []
   
    def interact(self,other_Human):
        if type(other_Human) == Woman:                                                      #IF next to an human instance of Woman:
            if other_Human.name in self.attempted or self.name in other_Human.attempted:    #Check they haven't interacted before
                pass                                                                        #IF they have, pass it.
            elif self.get_ConsumedDrinks()>=10:
                return -1
            else:                                                                       #OTHERWISE,
                print(f"{self.name} said: {Mline[random.randint(0,len(Mline)-1)]}")     #Print the pickup line
                self.attempted.append(other_Human.name)                                 #Remember who they tried to hit on
                if self.get_charisma()>other_Human.get_intelligence() or self.get_intelligence()==other_Human.get_intelligence():   #IF the man's Charisma is higher than the Woman's intelligence or equal in intelligence,
                    print(f"{other_Human.name} said: {agrees[random.randint(0,len(agrees)-1)]}")                                    #Woman will find it charming
                    print(f"{self.name} took a shot and won! He's going home with {other_Human.name} tonight")                      #Announce this guy's got game
                    return 2                                                                                                        #Return a 1 to the neighbor interaction
                else:                                                                                                               #OTHERWISE,
                    print(f"{other_Human.name} replied: {rejections[random.randint(0,len(rejections)-1)]}")                         #Get shot down
                    print(f"{self.name} got rejected by {other_Human.name}!")                                                       #Announce the rejection
                    self.set_status("Rejected")                                                                                     #Switch status to rejected
                    damage = int(self.get_charisma())-5                                                                             #Calculate the damage
                    self.set_charisma(damage)                                                                                       #Take Pride damage
                    print(f"{self.name}'s charisma lowered to {self.get_charisma()}. Perhaps the bartender could help...")          #Announce Charisma loss
                    return 1

        elif type(other_Human) == Bartender:                                         #If the instance type is a Woman,
            print(f"{self.name}: {greets[random.randint(0,len(greets)-1)]}")         #Print the greeting
            return 0                                                                 #Return 0 to the neighbor interaction
        
        elif type(other_Human) == Woman:                                             #But if the instance type is a Woman,
            print(f"{self.name}: {greets[random.randint(0,len(greets)-1)]}")         #Print the greeting
            return 0                                                                 #Return 0 to the neighbor interaction
        
        return 0                                                                     #If none of those happen, return 0 to be safe
    

class Woman(Human):
    def __init__(self):
        super().__init__()
        self.name = wnames[random.randint(0,len(wnames)-1)]
        self._image = Human._load_image(f"w{random.randint(1,len(wnames)-1)}.png")
        self.attempted = []
    def interact(self,other_Human):
        if type(other_Human) == Man:                                                            #If next to an agent instance of Man:
                if other_Human.name in self.attempted or self.name in other_Human.attempted:    #and if they've been hit on 
                    pass
                elif self.get_ConsumedDrinks()>=10:
                    return -1
                else:
                    print(f"{self.name} said: {Wline[random.randint(0,len(Wline)-1)]}")     #Print the pickup line
                    self.attempted.append(other_Human.name)                                 #Remember who they hit on
                    if self.get_charisma()>other_Human.get_intelligence():                  #If the woman's charisma, is higher than the man's intelligence
                        print(f"{other_Human.name} said: {agrees[random.randint(0,len(agrees)-1)]}")
                        print(f"{self.name} took a shot and won! She's going home with {other_Human.name} tonight")
                        return 2                                                            #Return a 2 to the neighbor interaction
                    
                    else:
                        print(f"{other_Human.name} replied: {rejections[random.randint(0,len(rejections)-1)]}")                    #Get shot down
                        self.set_status("Rejected")                                                                                #Switch status to rejected
                        print(f"{self.name} got rejected by {other_Human.name}!")                                                  #Announce the rejection
                        damage = int(self.get_charisma())-5                                                                        #Calculate the damage
                        self.set_charisma(damage)                                                                                  #Take Pride damage
                        print(f"{self.name}'s charisma lowered to {self.get_charisma()}! Perhaps the bartender could help...")     #Announce Charisma loss
                        return 1
        
        elif type(other_Human) == Woman:                                             #But if the instance type is a Woman,
            print(f"{self.name}: {greets[random.randint(0,len(greets)-1)]}")         #Print the greeting
            return 0                                                                 #Return 0 to the neighbor interaction 
       
        elif type(other_Human) == Bartender:                                         #But if the instance type is a Woman,
            print(f"{self.name}: {greets[random.randint(0,len(greets)-1)]}")         #Print the greeting
            return 0                                                                 #Return 0 to the neighbor interaction
        return 0                                                                     #If none of those happen, return 0 to be safe

class Bartender(Human):
    def __init__(self):
        super().__init__()
        self.name = "SERVE-0"
        self._image = Human._load_image("b1.png")
        self.set_status("Robot")
        
    def interact(self,other_Human):
        if other_Human.get_status() == "Sober":
            print(f"{self.name}: {bgreets[random.randint(0,len(bgreets)-1)]}")         #Print the greeting
            return 0                                                                 #Return 0 to the neighbor interaction  
        elif other_Human.get_status() == "Rejected":
            print(f"{self.name}:My sensors indicate you have been dealt emotional damage. Here is some Bartender wisdom to cheer you up: {wisdom[random.randint(0,len(wisdom)-1)]}")
            other_Human.get_drink()
            return 0
        elif other_Human.get_ConsumedDrinks()==9:
            print(f"{self.name}:My sensors indicate you are drunk. You have been cut off. Initializing S0berup")
            other_Human.set_charisma(25)
            other_Human.set_intelligence(50)
            print("S0berup complete. You look as good as new! Go get em champ.")