from PIL import Image, ImageFilter
import numpy as np
import random
import math
import os.path

IMGSIZE = 100
imgType = np.zeros((IMGSIZE, IMGSIZE), dtype = np.int)


# The class that makes each circle with the user inputs
class Circle:
    
        def __init__(self, a, b, d):
                # X coordinate of the stripe in the image.
                self.x = 0
                # Y coordinate of the stripe in the image.
                self.y = 0
                # X-intercept of the stripe in the image.
                self.a = a
                # Y-intercept of the stripe in the image.
                self.b = b
                # The radius^2 of the stripe in the image.
                self.d = d
                # Current pixel used as a (x, y) tuple.
                self.pixel = None
                # List of pixels in this stripe
                self.pixel_list = list()
                # Used to prevent a different x having the same y value
                self.prev_y = IMGSIZE - 1
                # Used to prevent a different y having the same x value
                self.prev_x = 0


        # The equation to get the y value of the circle from the given x
        def vertical_circle(self):
                try:
                        self.y = math.sqrt(self.d - pow((self.x + self.a),
                                                        2))- self.b
                        self.pixel = (self.x, self.y)
                except:
                        return None


        # The equation to get the x value of the circle from the given y
        def horizontal_circle(self):
                try:
                        self.x = math.sqrt(self.d - pow((self.y + self.b),
                                                        2)) - self.a
                        self.pixel = (self.x, self.y)
                except:
                        return None


        # Draws the top and the bottom of the circle
        def draw_circle_vertical(self):
            
                for self.x in range(0,IMGSIZE):
                
                        # Gets the y value for the circle
                        self.vertical_circle()

                        # Skip if there is no corresponding y value or if
                        # the y values are repeating
                        if self.y == None:
                                continue
                        if round(self.y,5) == round(self.prev_y,5):
                                continue

                        # Set previous to check for duplicates
                        self.prev_y = self.y
                        
                        # Ask Sam about how he derived this equation
                        y2 = self.y - 2 * (self.y + self.a)
                        
                        # Append the pixel that is part of the circle
                        self.pixel_list.append(self.pixel)
                        imgType[self.x][int(self.y)] = 1
                        
                        
                        if y2 > 99 or y2 < 0:
                            continue
                        
                        # Update the pixel and add it to the pixel list
                        self.pixel = (self.x, y2)
                        self.pixel_list.append(self.pixel)
                        imgType[self.x][int(y2)] = 1


        # Draws the two sides of the circle
        def draw_circle_horizontal(self):

                for self.y in range(0, 100):

                        # Gets the x value for the circle
                        self.horizontal_circle()

                        # Skip if there is no corresponding y value or if
                        # the y values are repeating
                        if self.x == None:
                                continue
                        if round(self.x,5) == round(self.prev_x,5):
                                continue

                        # Set previous to check for duplicates
                        self.prev_x = self.x
                        x2 = self.x - 2 * (self.x + self.a)

                        # Append the pixel that is part of the circle
                        self.pixel_list.append(self.pixel)
                        imgType[int(self.x)][self.y] = 1

                        if x2 > 99 or x2 < 0:
                                continue

                        # Update the pixel and add it to the pixel list
                        self.pixel = (x2, self.y)
                        self.pixel_list.append(self.pixel)
                        imgType[int(x2)][self.y] = 1


        # Outputs the circles made into files
        def print_circle(self):
                img = Image.new('RGB', (IMGSIZE, IMGSIZE), 'white')
                toSave = img.load()
                for i in range(IMGSIZE):
                        for j in range(IMGSIZE):
                                toSave[i, j] = imgType[i][j] * 200

                # If the file name exists, create a new image
                save_num = 0
                while (os.path.isfile('Sample' + str(save_num) +'.png')):
                    save_num += 1
                img.save('Sample' + str(save_num) + '.png')


        # Used to get the list of coordinates the circle has
        def get_pixel_list(self):
                return self.pixel_list


# Carries a list of circles' pixels into its ownarray
class Circle_List:
    
    def __init__(self, name):
            # List of circles making up the stripe in the image set
            self.circles = list()
            # Name of the list in the graph.
            self.name = name
        
            # Adds circles to its list
            def add_circles(self, pixel_list):
                    self.circles.append(pixel_list)
        
            # Access individual circles within the list
            def get_circles(self):
                    return self.circles
