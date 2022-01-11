import tkinter
import pygame
import math

from tkinter import *
from tkinter import messagebox



# Priority queue is used to store the chidren (next step to be taken) based on distance - lower the distance higher the priority
from queue import PriorityQueue
from pygame import display

from pygame.constants import KEYDOWN

pygame.init();

# Width and Height of the display screen is specified
WIDTH = HEIGHT = 960;

# Here we are setting the display size of the windows with specified width and height
WIN = pygame.display.set_mode((WIDTH, HEIGHT));

# Here we are setting the current window caption
pygame.display.set_caption("A* path finding algorithm - ABHISHEK R MANAS - 1RV20CS005")

# Here we are going to specify the colours that we will be using in our pygame

BLUE   = 		(52,1,91);  # unvisited node
GREEN  = 	(121,3,172);  # visited node
NGREEN = 	(121,84,182);  # neigbour node
SBLUE  = (0,0,255);  # start node
ERED   = (255,0,0);    # end node
BLACK  = 	(80,80,80);      # brick node
YELLOW = (255,205,0);  # path node
WHITE  = (0,0,0);    # grid line colour

#----------------------------------------------------------START OF Node CLASS----------------------------------------------------------#



# Node class 
# going to hold the information about the Node's position (row and column in which it is present in the grid) and colour of the node
# going to hold the dimension of itself
# must keep track of its neighbours
# with respect to colour of the node - 
# we can identify whether it is a barrier or the start node or the end node or a general node in the path
class Node:
    def __init__ (self, row, col, width, total_rows):
        # row and col specifies the coordinates of the node
        self.row = row;
        self.col = col;

        # to store the information about the width of the current node
        self.width = width;

        # just by knowing the coordinates we cannot create a block
        # to create a block (node) at given coordinate - we should know the width of each block
        # row * width and col * width gives the end position of the node along x and y axis
        self.x = row * width; 
        self.y = col * width;

        # To indicate that node has not yet been visited
        self.color = BLUE;

        # in order to store the information about the neighbours - we use a list
        self.neighbours = [];

        self.total_rows = total_rows;

    # To get the position of a node we create a method called get_position()
    def get_position(self):
        return self.row, self.col;


#-----------------------------------------------------CHECKING-----------------------------------------------------#

    # To check if the node is visited or not and return true if visited
    def is_visited(self):
        return (self.color == GREEN);
    
    # To find the neighbouring nodes that can be visited in te next step**** we use is_neighour() method
    def is_neighbour(self):
        return (self.color == NGREEN);

    # To find if the node is a barrier we use is_barrier() method
    def is_barrier(self):
        return (self.color == BLACK);

    # To find if the node is a start node we use is_start() method
    def is_start(self):
        return (self.color == SBLUE);
    
    # To find if the node is a end node we use is_end() method
    def is_end(self):
        return (self.color == ERED);

#--------------------------------------------------------END--------------------------------------------------------#


#------------------------------------CHANGE THE COLOR => CHANGE THE STATE OF NODE-----------------------------------#

    # To reset the colour of the node to the BLUE (unvisited)
    def reset(self):
        self.color = BLUE;
    
    # To make the node as visited - change its color to GREEN
    def make_visited(self):
        self.color = GREEN;
    
    # To make the node as neighbour - change its color to NGREEN
    def make_neighbour(self):
        self.color = NGREEN;
    
    #To make the node as start node - change its color to SBLUE
    def make_start(self):
        self.color = SBLUE;
    
    # To make the node as end node - change its color to ERED
    def make_end(self):
        self.color = ERED;
    
    # To make the node as barrier node - change its color to BLACK
    def make_barrier(self):
        self.color = BLACK;
    
    # To make the node as path node - change its color to YELLOW
    def make_path(self):
        self.color = YELLOW;

#--------------------------------------------------------END--------------------------------------------------------#

    # draw() method - to draw the node on the screen (window)
    def draw(self, win):
        pygame.draw.ellipse(win, self.color, (self.x, self.y, self.width/0.9, self.width/0.9));
    
        

    # To update the neighbours of current node
    def update_neighbour(self, grid):
        self.neighbours = [];

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbours.append(grid[self.row - 1][self.col]);

        if self.row < self.total_rows-1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbours.append(grid[self.row + 1][self.col]);
        
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier(): # LEFT
            self.neighbours.append(grid[self.row][self.col-1]);
        
        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_barrier(): # RIGHT
            self.neighbours.append(grid[self.row][self.col+1]);
        
        if self.row < self.total_rows-1 and self.col < self.total_rows-1 and not grid[self.row+1][self.col+1].is_barrier() and not grid[self.row][self.col+1].is_barrier() and not grid[self.row + 1][self.col].is_barrier(): # SE
            self.neighbours.append(grid[self.row+1][self.col+1]);
        
        if self.row > 0 and self.col < self.total_rows-1 and not grid[self.row-1][self.col+1].is_barrier() and not grid[self.row-1][self.col].is_barrier() and not grid[self.row][self.col+1].is_barrier(): # NE
            self.neighbours.append(grid[self.row-1][self.col+1]);
        
        if self.row < self.total_rows-1 and self.col > 0 and not grid[self.row+1][self.col-1].is_barrier() and not grid[self.row + 1][self.col].is_barrier() and not grid[self.row][self.col-1].is_barrier(): # SW
            self.neighbours.append(grid[self.row+1][self.col-1]);
        
        if self.row > 0 and self.col > 0 and not grid[self.row-1][self.col-1].is_barrier() and not grid[self.row - 1][self.col].is_barrier() and not grid[self.row][self.col-1].is_barrier(): # NE
            self.neighbours.append(grid[self.row-1][self.col-1]);
        

    # To compare which node has less the distance to reach the goal
    def __lt__(self, other):
        return False;

#----------------------------------------------------------END OF Node CLASS----------------------------------------------------------#



#--------------------------------------------------------HEURISTIC FUNCTION--------------------------------------------------------#

# To create the heuristic function 
# The A* algorithm uses a heuristic function to help decide which path to follow next. 
# The heuristic function provides an estimate of the minimum cost between a given node and the target node.

# we are going to make use of manhattan distance technique - where we find the shortest "L" from node to goal
# p1 and p2 are the points of the form (x, y)

def h(p1, p2):
    x1, y1 = p1;
    x2, y2 = p2;
    return math.sqrt(math.pow((x2 - x1),2) + math.pow((y2 - y1),2));

#--------------------------------------------------------END OF HEURISTIC FUNCTION--------------------------------------------------------#



#--------------------------------------------------------PATH CONSTRUCTION FUNCTION--------------------------------------------------------#
list = [];
def path_construct(came_from, current, draw, start):
    
    while current in came_from:
        current = came_from[current];
        y, x =current.get_position();
        list.append((x,y));
        if(current != start):
            current.make_path();
        draw();
    
    list.reverse();
    print(list);

#--------------------------------------------------------END OF PATH CONSTRUCTION FUNCTION--------------------------------------------------------#



#--------------------------------------------------------START OF A* ALGO FUNCTION--------------------------------------------------------#

def algorithm(draw, grid, start, end):
    count = 0;

    # Here neighbour_queue is is the Priorit queue - in which the neighbours are inserted based on the priority
    neighbour_queue = PriorityQueue(); 

    # F = g + h
    # for start node - F value = 0 as it is the first node
    # count is used to know whether same cost paths are present from different nodes to the next step
    # if count > 1 - then different paths are present (same cost)
    # then we are going to chose that path which came first
    neighbour_queue.put((0, count, start)); 
    
    # This is a set - which is used to keep track of the path of the ancestors
    came_from = {};

    # Initially the g score of all the nodes be infinity as we don't know where to go
    # List comprehension is used for initilaization
    g_score = {node: float("inf") for row in grid for node in row}
    # For the start node the g_score value will be 0
    g_score[start] = 0;

    # Initially the f score of all the nodes be infinity as we don't know where to go
    # List comprehension is used for initilaization
    f_score = {node: float("inf") for row in grid for node in row}
    # For the start node the f_score value will be equal to heuristic value
    # It gives an estimate****** of the distance between the start and the end nodes
    f_score[start] = h(start.get_position(), end.get_position());

    # We maintain a hash to keep track of all the items which are present in the queue and items which are not present in the priority queue
    neighbour_queue_hash = {start};

    # This algorithm is going to run until the neighbour_queue is not empty

    while not neighbour_queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
        
        current = neighbour_queue.get()[2] # to get the current node - index 2 has the node information (pop out)

        neighbour_queue_hash.remove(current); # removing the current node from the hash 

        if current == end:
            # if current node that we removed is the end node - it means that we have found the shortest path
            path_construct(came_from, current, draw, start);
            end.make_end();
            return True;
        
        # Now we have to consider the neighbours of each node
        for neighbour in current.neighbours:
            temp_g_score = g_score[current]+1; # as the neighbour is 1 node ahead or behind the current node
            
            if temp_g_score < g_score[neighbour]: 
                # if the g_score of currently shotest node + 1 is less than the g_score of the neigbour 
                # it means we found a better neighbour 
                # simple logic is that we are trying to find the best path to get to every single node 
                # and from there we can target out towards our goal and find the optimal path

                came_from[neighbour] = current;     # we came from the current node to the neighbour node
                g_score[neighbour] = temp_g_score;  # update the g_score of the neighbour
                f_score[neighbour] = temp_g_score + h(neighbour.get_position(), end.get_position()); 

                # now we must add tis neighbour into the hash
                if neighbour not in neighbour_queue_hash:
                    count += 1;
                    neighbour_queue.put((f_score[neighbour], count, neighbour)); # add the neighbour info into the queue
                    neighbour_queue_hash.add(neighbour); # add the neighbour into the hash
                    neighbour.make_neighbour();

        
        draw();

        if current != start:
            current.make_visited();

    
    return False;

#--------------------------------------------------------END OF A* ALGO FUNCTION--------------------------------------------------------#



#--------------------------------------------------------MAKE GRID FUNCTION--------------------------------------------------------#

# To construct the grid we use make_grid() function:

def make_grid(rows, width):
    grid = []; # list which stores the rows

    gap = width // rows; # floor division to get the size of each node

    for i in range(rows):
        grid.append([]); # each row has another list to store column nodes
        for j in range(rows):
            node = Node(i, j, gap, rows);
            grid[i].append(node);
    
    return grid;

#--------------------------------------------------------END OF GRID FUNCTION--------------------------------------------------------#



#--------------------------------------------------------DRAW GRID LINE FUNCTION--------------------------------------------------------#

def draw_grid(win, rows, width):
    gap = width // rows;

    # To draw horizonral lines
    for i in range(rows):
        pygame.draw.line(win, WHITE, (0, i*gap), (width, i*gap));
    # To draw vertical lines
        for j in range(rows):
            pygame.draw.line(win, WHITE, (j*gap, 0), (j*gap, width));

#--------------------------------------------------------END OF DRAW GRID LINE FUNCTION--------------------------------------------------------#



#---------------------------------------------------ACTUAL DRAW FUNCTION--------------------------------------------------------#

# grid is passed from main function - after creating the grid using make_grid()
def drawing(win, grid, rows, width):
    win.fill(BLUE); # fill the entire screen with BLUE color

    for row in grid:
        for node in row:
            node.draw(win); # present in Node class 
    
    draw_grid(win, rows, width); # we have drawn the grid lines 

    pygame.display.update(); #update the display after creating the grids

#-------------------------------------------------END OF ACTUAL DRAW FUNCTION--------------------------------------------------------#



#-----------------------------------------------TO GET POSITION OF CLICKED POINT--------------------------------------------------------#

def get_mouse_clicked_pos(pos, rows, width):
    gap = width // rows;

    x, y = pos;

    row = x // gap;
    col = y // gap;

    return row, col;

#--------------------------------------------------------END--------------------------------------------------------#



#---------------------------------------------------MAIN FUNCTION--------------------------------------------------------#

def main(win, width):
    ROWS = 60;
    grid = make_grid(ROWS, width);

    start = None;
    end = None;

    run = 1;
    started = 0;

    while run:
        drawing(win, grid, ROWS, width);
        for event in pygame.event.get(): # get events from the queue

            # To check if the user is trying to quit the window - if yes make run = false - which terminates the loop
            if event.type == pygame.QUIT:
                run = 0;
            
            # Once we start the algorithm - in order to avoid user to enter anything other than quit 
            if started:
                continue;
                
            # To add functionality to the mouse clicks 
        
            # if left button is pressed - we must create the start node, end node and barrier node
            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos();
                row, col = get_mouse_clicked_pos(pos, ROWS, width);
                node = grid[row][col];
                
                if(node != start and node != end):
                    node.make_barrier();
            
            if event.type == KEYDOWN:
                if event.key == pygame.K_s:
                    if not start and node != end:
                        start = node;
                        start.make_start();

                elif event.key == pygame.K_e:
                    if not end and node != start:
                        end = node;
                        end.make_end();
                

                elif event.key == pygame.K_SPACE and start:
                    for row in grid:
                        for node in row:
                            node.update_neighbour(grid);

                    # If the end point is not found - then show the warning 
                    if not end and start: 
                            root = tkinter.Tk();
                            root.withdraw();
                            messagebox.showwarning("Warning", "No end point found");
                            root.destroy();
                            break;
                    
                    # call the algorithm
                    success = algorithm(lambda : drawing(win, grid, ROWS, width), grid, start, end);

                    # If the Algorithm is successful then display success message
                    if success == True:
                        root = tkinter.Tk();
                        root.withdraw();
                        messagebox.showinfo("Success", "Shortest path found");
                        root.destroy();
                    
                    # If the Algorithm fails then display error message
                    if success == False:
                        root = tkinter.Tk();
                        root.withdraw();
                        messagebox.showwarning("Warning", "Path not found due to an obtacle");
                        root.destroy();
                        start = None;
                        end = None;
                        grid = make_grid(ROWS, width);
                        
                
                elif event.key == pygame.K_r:
                        start = None;
                        end = None;
                        grid = make_grid(ROWS, width);


            

            # if Right button is pressed - we must reset the node to unvisited
            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos();
                row, col = get_mouse_clicked_pos(pos, ROWS, width);
                node = grid[row][col];
                node.reset();

                if(node == start):
                    start = None;

                elif(node == end):
                    end = None;

    pygame.quit(); # It closes the window
#--------------------------------------------------------END OF MAIN FUNCTION--------------------------------------------------------#
\

main(WIN, WIDTH); # call the main function

#--------------------------------------------------------END--------------------------------------------------------#