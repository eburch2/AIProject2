
# coding: utf-8

# In[4]:

def hill_climb(function_to_optimize, step_size, xmin, xmax, ymin, ymax):
    #create start values

    x = uniform(xmin, xmax)
    y = uniform(ymin, ymax)
    
    cached_x = x
    cached_y = y
    
    adjacent_values = []
    old_min = sys.maxsize
    new_min = old_min
    
    # creates an adjacency grid of tuples (x,y) filling in the order: BL, BC, BR, ML, MC, MR, TL, TC, TR
    # B-> bottom, M-> middle, T-> top, L-> left, C-> center, R-> right
    # Note: MC is the center of the grid and considered our current x,y point
    
    done = False
    while (done is False):
    
        for cols in range(-1, 2):
            for rows in range(-1, 2):
                next_x = x + step_size*rows
                next_y = y + step_size*cols
                if (xmin < next_x < xmax and ymin < next_y < ymax): # if tuple is in range
                    next_z = function_to_optimize(next_x, next_y)
                    adjacent_values.append(next_z)
                    if (next_z < new_min):
                        new_min = next_z
                        cached_x = next_x
                        cached_y = next_y
                        x_coords.append(next_x)
                        y_coords.append(next_y)
                        z_coords.append(new_min)
                    
        # checks if we're at the local min, otherwise we can keep moving            
        if (new_min == old_min):
            done = True
        else:
            old_min = new_min
            x = cached_x
            y = cached_y
        #print(adjacent_values)
        #print("min: " + repr(old_min))
        #print("x: " + repr(cached_x))
        #print("y: " + repr(cached_y) + "\n")
        adjacent_values = []
            
    return old_min


# In[30]:

def hill_climb_random_restart(function_to_optimize, step_size, num_restarts, xmin, xmax, ymin, ymax):
    global_min = sys.maxsize
    
    # runs for the first time, when num_restarts = 0 same as hill_climb.
    global_min = hill_climb(function_to_optimize, step_size, xmin, xmax, ymin, ymax)
    
    for restarts in range(0, num_restarts):
        local_min = hill_climb(function_to_optimize, step_size, xmin, xmax, ymin, ymax)
        if (local_min < global_min):
            global_min = local_min
        #print(local_min)
        #print(global_min)
    return global_min


# In[67]:

def simulated_annealing(function_to_optimize, step_size, max_temp, xmin, xmax, ymin, ymax):
    
    current_temp = max_temp
    last_node = ( uniform(xmin, xmax), uniform(ymin, ymax) )
    cached_min = sys.maxsize
   
    while (current_temp > 0):
        next_node = ( uniform(xmin, xmax), uniform(ymin, ymax) )
        next_min = function_to_optimize(next_node[0], next_node[1])
        P = get_probability_of_move(function_to_optimize, current_temp, last_node, next_node)
        
        if (uniform(0, 1) < P):
            if (next_min < cached_min):
                cached_min = next_min
            #print("accepted! with P = " + repr(P))
            last_node = next_node
            x_coords.append(next_node[0])
            y_coords.append(next_node[1])
            z_coords.append(next_min)
        #else:
            #print("denied with P = " + repr(P))
        current_temp -= step_size
        
    return cached_min


# In[7]:

def get_probability_of_move(function_to_optimize, T, tupleA, tupleB):
    # P(move) = e^ ((f(B) - f(A)) / T)
    prob = math.e**(function_to_optimize(tupleB[0], tupleB[1]) - function_to_optimize(tupleA[0], tupleA[1]) / T)
    return prob


# In[8]:

def get_function(x, y):
    r = math.sqrt(x**2 + y**2)
    func = (math.sin(x**2 + 3*(y**2)) / (0.1 + r**2)) + (x**2 + 5*(y**2))*(math.exp(1-(r**2)) / 2)
    return func


# In[9]:

def get_x_coords():
    return x_coords


# In[10]:

def get_y_coords():
    return y_coords


# In[11]:

def get_z_coords():
    return z_coords


# In[12]:

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

def graph():
    
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    
    ax.scatter(get_x_coords(), get_y_coords(), get_z_coords(), zdir='z', c='r')
        
    #plt.plot(get_x_coords(), get_y_coords(), 'ro')
    
    X = np.arange(-2.5, 2.5, 0.1)
    Y = np.arange(-2.5, 2.5, 0.1)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X**2 + Y**2)
    Z = (np.sin(X**2 + 3*(Y**2)) / (0.1 + R**2)) + (X**2 + 5*(Y**2))*(np.exp(1-(R**2)) / 2)
    ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
    
    plt.show()


# In[52]:

def main():
    print(simulated_annealing(get_function, 0.1, 20, -2.5, 2.5, -2.5, 2.5))


# In[68]:

import math
import sys
from random import uniform

# global variables so we can graph our path
x_coords = []
y_coords = []
z_coords = []

main()
graph()


# In[15]:




# In[54]:




# In[ ]:




# In[ ]:



