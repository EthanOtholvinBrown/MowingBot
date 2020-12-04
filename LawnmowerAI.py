# -*- coding: utf-8 -*-
"""

@author: Ethan
"""
import math
import botGarage  
import cv2
import numpy as np  
from matplotlib import pyplot as plt
#Sets number of mowers being used
NUM_MOWERS = 1
#Function for using the bot(s), takes in number of sections of lawns and 
#each section 
def useBot(l,section):    
    #Prints current program status
    print("Building grid for section",l+1,"...")
    #Adds title to current section image plot and shows plot
    title = "Property section",l+1
    plt.title(title,loc = 'center')
    plt.imshow(section[l])
    plt.show()
    #Saves current lawn section as an image in a temporary location
    #to be used for determining section dimensions
    cv2.imwrite("Isolated.jpg",section[l])
    #Reads back in current section image
    workWith = cv2.imread(r'Isolated.jpg')
    #Reads dimensions of current section 
    width = workWith.shape[1]
    length = workWith.shape[0]
    #Display image dimensions for user convenience and states status
    print("Width of the section: ", width)
    print("Length of the section: ", length)
    print("The program now knows the grid to use for the bot to move.")
    print("It will scale the size of the grid for the purposes of ",
          "this program.")
    #Set desired scale for simulation purposes    
    scaleX = int(input("Enter the desired scale for X: "))
    scaleY = int(input("Enter the desired scale for Y: "))
    xAxis = math.ceil(width/scaleX)
    yAxis = math.ceil(length/scaleY)
    #Display newly made dimensions
    print("New grid X-axis: ", xAxis)
    print("New grid Y-axis: ", yAxis)    
    #Submits dimensions and number of mowers to the simulation script
    botMove = botGarage.FPB(xAxis,yAxis,NUM_MOWERS)   
    #For simulation purposes, a desired length of time must be used to 
    #simulate the battery life of the mower.
    #Current time used is seconds, can be scaled according to user desire.
    #Uses error checking to ensure that a number is used for program stability
    while True:
        try:
            userT = int(input("Enter how long the battery will last(scaled to seconds):  "))
            break
        except ValueError:
            print("Please enter a number.")
    #Displaying current status while plot
    print("Using bot on section",l+1,"...")
    #Begin simulation for current section based on "battery life"
    botMove.bots(userT,0) 
    #Display how much of the section was covered by the bot
    print("Percentage of section covered: ",
          format(botMove.get_percentage(),'.2f'),'%')
    
def main():
    #Encapsulate entire program in error checking for quit option
    while True:
        try:            
            print("This program is going to simulate the lawnmower bot cutting grass.")
            print("The first thing required is an aerial image of a lawn.")
            print("(The actual product will acquire the image from a drone.)")
            #Ask user for aerial image of property to use
            #Commercial version will have image provided by drone
            q = str(input("Enter the file name of the lawn image(make sure to end with file extension): "))
            #Read in user submitted image and show what is found to user
            colorpic = cv2.imread(q)
            print("Plot window shows the picture you entered.")
            plt.imshow(cv2.cvtColor(colorpic, cv2.COLOR_BGR2RGB))
            plt.show()
            print("Do you want to use the Mower or the Blower?")
            print("'m' - Mower")
            print("'b' - Blower")
            print("'q' - Quit")
            #Convert image to HSV to use range finder
            converted = cv2.cvtColor(colorpic, cv2.COLOR_BGR2HSV) 
            while True:
                try:
                    q = str(input("Choice: "))
                    if(q == 'm' or q == 'b' or q == 'q'):
                        break
                    else:
                        print("Invalid Selection, select again...")
                except ValueError:
                    print("Still Wrong...")
            if (q == 'm'):    
                #Look for sections of image colored green (A lawn)
                look = cv2.inRange(converted, (40, 0, 0), (70, 255,255))
            elif (q == 'b'):
                #Look for sections of image colored bluish-grey (A driveway)
                look = cv2.inRange(converted, (80,0,0), (100,255,255))
            print("Plot window shows your image after isolating ",
                  "search parameter (Colored Yellow)")
            #Display result of search, found section is highlighted in yellow
            plt.imshow(look)
            plt.show()
            q = str(input("Press any key to continue...[q to quit]: ")) 
            #Look for all contours found in the image
            contours, hierarchy = cv2.findContours(look, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            #Create arrays for saving sections
            section = []
            trash = []
            #Search through all contours found
            for i in contours:                
                #Establish rectangles around any section found to find
                #dimensions/plot points                
                x,y,w,h = cv2.boundingRect(i)
                #Isolate each rectangle/section
                extractedImage = look[y:y+h, x:x+w]
                #Save any section which isn't too small
                if (w > 5 and h > 5):                    
                    section.append(extractedImage)
                #Keep track of sections which are too small
                else:
                    trash.append(extractedImage)
            #Display how many sections were found
            print("Detected",len(section),"sections of lawn.")
            #Show each saved section for simulation purposes
            for l in range (len(section)):
                print("Plot shows current detected section...")
                plt.imshow(section[l])
                plt.show()   
                q = str(input("Press any key to continue... [q to quit]: "))  
            print("")
            #Run the useBot function for each section
            for k in range (len(section)):
                useBot(k, section)                
            #End the program if q is ever entered
            q = str(input("Press 'q' to quit, any other key to run again..."))
            if (q == 'q'):                
                break
        except ValueError:
            print("Enter a valid choice, please.")
    print("Goodbye!")
main()    