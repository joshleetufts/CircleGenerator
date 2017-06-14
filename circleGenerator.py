from PIL import Image, ImageFilter
import matplotlib.cm as cm
import numpy as np
import random
import math
import os.path


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                Global Variables and Arrays

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# The dimension of our image
IMGSIZE = 100

# The initial condition of our image
UNVISITED = 0

# The backbone of each image drawn
imgType = np.zeros((IMGSIZE, IMGSIZE), dtype = np.int)

# The values that each pixel has in our 100x100 image
shadedPlot = np.zeros((IMGSIZE, IMGSIZE), dtype = np.int)




"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                      Classes

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# The class that makes each circle with the user inputs
class Circle:
    
        def __init__(self):
                # X coordinate of the stripe in the image.
                self.x = 0
                # Y coordinate of the stripe in the image.
                self.y = 0
                # X-intercept of the stripe in the image.
                self.a = 0
                # Y-intercept of the stripe in the image.
                self.b = 0
                # The radius^2 of the stripe in the image.
                self.d = 0
                # Current pixel used as a (x, y) tuple.
                self.pixel = None
                # List of pixels in this stripe
                self.pixel_list = list()
                # Used to prevent a different x having the same y value
                self.prev_y = IMGSIZE - 1
                # Used to prevent a different y having the same x value
                self.prev_x = 0
                # The list of circles that consists of all the pixels of that circle
                self.circle_list = list()

        def draw_circles(self, a, b, d):
                # X-intercept of the stripe in the image.
                self.a = a
                # Y-intercept of the stripe in the image.
                self.b = b
                # The radius^2 of the stripe in the image.
                self.d = d

                self.circle_list = []

                self.draw_circle_horizontal()

                self.draw_circle_vertical()

                self.add_circles()


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
                        self.pixel = (int(self.x), int(self.y))
                        self.pixel_list.append(self.pixel)
                        imgType[int(self.x)][int(self.y)] = 1
                        
                        
                        if y2 > 9 or y2 < 0:
                            continue
                        
                        # Update the pixel and add it to the pixel list
                        self.pixel = (int(self.x), int(y2))
                        self.pixel_list.append(self.pixel)
                        imgType[int(self.x)][int(y2)] = 1


        # Draws the two sides of the circle
        def draw_circle_horizontal(self):

                for self.y in range(0, IMGSIZE):

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
                        self.pixel = (int(self.x), int(self.y))
                        self.pixel_list.append(self.pixel)
                        imgType[int(self.x)][int(self.y)] = 1

                        if x2 > 9 or x2 < 0:
                                continue

                        # Update the pixel and add it to the pixel list
                        self.pixel = (int(x2), int(self.y))
                        self.pixel_list.append(self.pixel)
                        imgType[int(x2)][int(self.y)] = 1


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

        # Makes a list of pixel_lists and empties out the pixel_list
        def add_circles(self):
                self.circle_list.append(self.pixel_list)

        # Used to get the list of coordinates the circle has
        def get_circle_list(self):
                return self.circle_list

        def clear_pixels(self):
                self.circle_list = []
                self.pixel_list = []



# The class that allots the values to the pixels
class Graph:
        def __init__(self, all_points):
                # All the points (nodes)
                self.nodes = all_points
                # Distance upon which the two points meet
                self.meeting = 0
                # Index of each start and goal
                self.index = 0
                # Number of times to BFS
                self.end = 0

        # Make each pixel value carry a shade value


        # Set the map to hold ones if part of the circle list
        def set_new_plot(self, circle_list):
                # Checks if all points in the circle have been initialized
                counter = 0
                # The points where
                starting_points = []
                print len(circle_list)
                for k in range(len(circle_list)):
                        for i in range(IMGSIZE):
                                for j in range(IMGSIZE):
                                        if (i, j) in circle_list[k]:
                                                shadedPlot[i][j] = 1
                                                counter += 1
                                                starting_points.append((i, j))

                                        # Double break to get to next circle
                                        if counter == len(circle_list[k]):
                                                break
                        return starting_points


        # Append all surrounding neighbors
        def add_neighbors(self, neighbors, distance):
                new_neighbors = []
                for count in range(len(neighbors)):
                        for i in [-1, 0, 1]:
                                for j in [-1, 0, 1]:
                                        x, y = neighbors[count][0], neighbors[count][1]
                                        if ((i != 0 and j != 0)
                                            and (x + i, y + j) in self.nodes
                                            and shadedPlot[x + i][y + j] == UNVISITED):
                                                shadedPlot[x + i][y + j] = distance
                                                new_neighbors.append((x + i, y + j))
                return new_neighbors


        # The breath first search to get the values of each color
        def bfs(self, circles):
                neighbors = []
                next_neighbors = []
                neighbors = self.set_new_plot(circles)
                print shadedPlot
                self.print_all_circles()

                done = False
                curr = 2
                while not done:
                        # Add new neighbors with new distance
                        next_neighbors = self.add_neighbors(neighbors, curr)
                        neighbors = next_neighbors
                        next_neighbors = []

                        # No more neighbors to add
                        if len(neighbors) == 0:
                                print shadedPlot
                                self.shade()
                                done = True
                        curr += 1


        # Prints the backbone of our circle picture
        def print_all_circles(self):
                img = Image.new('RGB', (IMGSIZE, IMGSIZE), 'white')
                toSave = img.load()
                for i in range(IMGSIZE):
                        for j in range(IMGSIZE):
                                toSave[i, j] = shadedPlot[i][j] * 200

                # If the file name exists, create a new image
                save_num = 0
                while os.path.isfile('Sample' + str(save_num) + '.png'):
                        save_num += 1
                img.save('Sample' + str(save_num) + '.png')


        # Shades the color of the picture
        def shade(self):
                min_shade, max_shade = 1, np.max(shadedPlot)
                mid = max_shade / 2

                # Reverse the values to fit the coolwarm color map
                for i in range(IMGSIZE):
                        for j in range(IMGSIZE):
                                if shadedPlot[i, j] <= mid:
                                        shadedPlot[i, j] = mid + abs(mid - shadedPlot[i, j])
                                elif shadedPlot[i, j] > mid:
                                        shadedPlot[i, j] = mid - abs(shadedPlot[i, j] - mid)

                img = Image.new('RGB', (IMGSIZE,IMGSIZE), 'white')
                toSave = img.load()
                for x in range(IMGSIZE):
                        for y in range(IMGSIZE):
                                norm_tup = cm.coolwarm(shadedPlot[x, y])
                                rgb_colors = (int(norm_tup[0]*255), int(norm_tup[1]*255), int(norm_tup[2]*255))
                                toSave[x, y] = rgb_colors
                img = img.filter(ImageFilter.BLUR)
                save_num = 0
                while (os.path.isfile('Color' + str(save_num) + '.png')):
                        save_num += 1
                img.save('Color' + str(save_num) + '.png')


        """
            def find_all_distances(self, circles, image):
                    self.bfs(circles, image)

                    for (i, j) in range(self.nodes):
                            # Only show the distances that overlapped
                            if image[i][j] != circles:
                                    print " ".join(image[i][j])
        """



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                Main that runs our classes

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# Set up the
allPts = []
for i in range(0, IMGSIZE):
        for j in range(0, IMGSIZE):
                allPts.append((i, j))

# Set up the classes
circle = Circle()
graph_bfs = Graph(allPts)

# Set the x-intercepts
for i in range (15, 30, 15):

        # Set the y-intercepts
        for j in range(15, 30, 15):

                # Set the radius
                for radius in range(4000, 16000, 4000):
                        circle.draw_circles(i, j, radius)

                # Draw the circles
                circle.print_circle()

                # Draw the graphs
                graph_bfs.bfs(circle.get_circle_list())

                # Reinitialize the shading board to 0
                shadedPlot = np.zeros((IMGSIZE, IMGSIZE), dtype=np.int)

                # Reinitialize the board to 0
                imgType = np.zeros((IMGSIZE, IMGSIZE), dtype=np.int)



















