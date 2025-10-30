import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import tkinter as tk
from tkinter import ttk
from matplotlib.colors import ListedColormap, BoundaryNorm

def Schelling_Model(n, empty_ratio, pop1_ratio, pop2_ratio, \
                    pop3_ratio, threshold, pop1_des, pop2_des, pop3_des):
    
    size = n*n    
    npop1 = int(size*pop1_ratio)
    npop2 = int(size*pop2_ratio)
    npop3 = int(size*pop3_ratio)
    nempty = int(size - npop1 - npop2 - npop3)
    
    counter = 0 
    iterations = []
    pop1_agg = []
    pop2_agg = []
    pop3_agg = []
    
    rows = columns = n
    board = np.array([0]*nempty + [1]*npop1 + [2]*npop2 + [3]*npop3)
    random.shuffle(board)
    board = board.reshape((rows, columns))
    
    def neighbours(board, x, y):
        similar = 0
        total = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy                
                if 0 <= nx < columns and 0 <= ny < rows:
                        if board[nx, ny] == board[x, y]:
                            similar += 1
                        if board[nx, ny] != 0:
                            if dx!=0 and dy!=0:
                                total += 1
        return similar, total
    
    def steps(board, threshold):
        nonlocal pop1_des, pop2_des, pop3_des
        unhappy = []
        popfree_total = []
        for x in range(rows):
            for y in range(columns):

                if board[x, y] != 0:
                    similar, total = neighbours(board, x, y)
                    if board[x, y] == 1 and similar < threshold:
                        if similar/(total + 1) < pop1_des or total == 0:
                            unhappy.append((x,y))
                            popfree_total.append(board[x, y])
                    if board[x, y] == 2 and similar < threshold:
                        if similar/(total + 1) < pop2_des or total == 0:
                            unhappy.append((x,y))
                            popfree_total.append(board[x, y])
                    if board[x, y] == 3 and similar < threshold:
                        if similar/(total + 1) < pop3_des or total==0:
                            unhappy.append((x,y))
                            popfree_total.append(board[x, y])

        if not unhappy:
            return board, False, popfree_total
        
        for x, y in unhappy:
            empty_cells = list(zip(*np.where(board == 0)))
            if not empty_cells:
                break
            new_x, new_y = random.choice(empty_cells)
            board[new_x, new_y] = board[x, y]
            board[x, y] = 0
        return board, True, popfree_total

    def update(frame):
        nonlocal board, counter, iterations
        board, changed, popfree_total = steps(board, threshold)
        mat.set_data(board)
        pop1_free = (npop1 - popfree_total.count(1))/npop1
        pop2_free = (npop2 - popfree_total.count(2))/npop2
        pop3_free = (npop3 - popfree_total.count(3))/npop3   
        if counter < 300:
            counter += 1
            iterations.append(counter)
            pop1_agg.append((pop1_free))
            pop2_agg.append((pop2_free))
            pop3_agg.append((pop3_free))        
            line1.set_xdata(iterations)
            line1.set_ydata(pop1_agg)
            line2.set_xdata(iterations)
            line2.set_ydata(pop2_agg)
            line3.set_xdata(iterations)
            line3.set_ydata(pop3_agg)
        return [mat, line1, line2, line3]

    fig, (ax1, ax2) = plt.subplots(ncols = 2)

    custom_colors = ["#FFFFFF", "#FF0000", "#0000FF", "#00FF00", "#fde725"]
    cmap = ListedColormap(custom_colors)
    norm = BoundaryNorm(np.arange(-0.5, len(custom_colors), 1), cmap.N)
    
    mat = ax1.matshow(board, cmap=cmap, norm =norm)
    line1, = ax2.plot(iterations, pop1_agg, ".", color="#FF0000", label = "Population 1")
    line2, = ax2.plot(iterations, pop2_agg, ".", color="#0000FF", label = "Population 2")
    line3, = ax2.plot(iterations, pop3_agg, ".", color="#00FF00", label = "Populaion 3")
    
    anim = animation.FuncAnimation(fig, update, frames=200,\
        interval=200, blit=False)
    
    fig.anim = anim

    plt.suptitle('Schelling model for 3 populations')
    
    ax1.set_title("Board")

    ax2.relim()
    ax2.autoscale_view()    
    ax2.set_xlim(-10, 300)
    ax2.set_ylim(0, 1.1)
    ax2.grid()
    ax2.set_title("Agruppation of each population")
    ax2.set_xlabel("Iterations")
    ax2.set_ylabel("Agruppation (%)")
    ax2.legend(loc="best")
    plt.show()
    
def create_gui():
    root = tk.Tk()
    root.title("Parameters for the simulation of Schelling Model")
    
    params = {
        "n": 50, 
        "empty_ratio": 0.3,
        "pop1_ratio": 0.23,
        "pop2_ratio": 0.22,
        "pop3_ratio": 0.25,
        "threshold": 5,
        "pop1_des": 0.6,
        "pop2_des": 0.55,
        "pop3_des": 0.7,
    }
    
    def update_params():
        params["n"] = int(n_entry.get())
        params["empty_ratio"] = float(empty_ratio.get())
        params["pop1_ratio"] = float(pop1_ratio.get())
        params["pop2_ratio"] = float(pop2_ratio.get())
        params["pop3_ratio"] = float(pop3_ratio.get())
        params["threshold"] = int(threshold_entry.get())
        params["pop1_des"] = float(pop1_des.get())
        params["pop2_des"] = float(pop2_des.get())
        params["pop3_des"] = float(pop3_des.get())

    def run_model():
        update_params() 
        Schelling_Model(params["n"], \
            params["empty_ratio"], params["pop1_ratio"], params["pop2_ratio"],\
            params["pop3_ratio"], params["threshold"], params["pop1_des"],\
            params["pop2_des"], params["pop3_des"])

    frame = ttk.Frame(root, padding = "15")
    frame.grid(row = 0, column = 0, sticky = (tk.W, tk.E, tk.N, tk.S))
    
    ttk.Label(frame, text = "Ratio of empty cells").grid(column = 0, row = 0,\
            sticky = (tk.W))
    empty_ratio = ttk.Entry(frame, width = 7)
    empty_ratio.insert(0, str(params["empty_ratio"]))
    empty_ratio.grid(column = 1, row = 0, sticky = (tk.W, tk.E))
    
    ttk.Label(frame, text = "Ratio of population 1").grid(column = 0, row = 1,\
            sticky = (tk.W))
    pop1_ratio = ttk.Entry(frame, width = 7)
    pop1_ratio.insert(0, str(params["pop1_ratio"]))
    pop1_ratio.grid(column = 1, row = 1, sticky = (tk.W, tk.E))
    
    ttk.Label(frame, text = "Ratio of population 2").grid(column = 0, row = 2,\
            sticky = (tk.W))
    pop2_ratio = ttk.Entry(frame, width = 7)
    pop2_ratio.insert(0, str(params["pop2_ratio"]))
    pop2_ratio.grid(column = 1, row = 2, sticky = (tk.W, tk.E))
    
    ttk.Label(frame, text = "Ratio of population 3").grid(column = 0, row = 3,\
            sticky = (tk.W))
    pop3_ratio = ttk.Entry(frame, width = 7)
    pop3_ratio.insert(0, str(params["pop3_ratio"]))
    pop3_ratio.grid(column = 1, row = 3, sticky = (tk.W, tk.E))

    ttk.Label(frame, text = "Desired neighbours of population 1").grid(column = 2, row = 1,\
            sticky = (tk.W))
    pop1_des = ttk.Entry(frame, width = 7)
    pop1_des.insert(0, str(params["pop1_des"]))
    pop1_des.grid(column = 3, row = 1, sticky = (tk.W, tk.E))

    ttk.Label(frame, text = "Desired neighbours of population 2").grid(column = 2, row = 2,\
            sticky = (tk.W))
    pop2_des = ttk.Entry(frame, width = 7)
    pop2_des.insert(0, str(params["pop2_des"]))
    pop2_des.grid(column = 3, row = 2, sticky = (tk.W, tk.E))    

    ttk.Label(frame, text = "Desired neighbours of population 3").grid(column = 2, row = 3,\
            sticky = (tk.W))
    pop3_des = ttk.Entry(frame, width = 7)
    pop3_des.insert(0, str(params["pop3_des"]))
    pop3_des.grid(column = 3, row = 3, sticky = (tk.W, tk.E))
    
    ttk.Label(frame, text = "Threshold").grid(column = 0, row = 7, \
            sticky = (tk.W))
    threshold_entry = ttk.Entry(frame, width = 7)
    threshold_entry.insert(0, str(params["threshold"]))
    threshold_entry.grid(column = 1, row = 7, sticky = (tk.W, tk.E))
    
    ttk.Label(frame, text= "Size of the square board").grid(column = 2, row = 0, \
            sticky = (tk.W))
    n_entry = ttk.Entry(frame, width = 7)
    n_entry.insert(0, str(params["n"]))
    n_entry.grid(column = 3, row = 0, sticky = (tk.W, tk.E))
      
    run_button = ttk.Button(frame, text = "Execute simulation", \
            command = run_model)
    run_button.grid(column = 0, row = 8, columnspan = 4)
    
    root.mainloop()

create_gui()