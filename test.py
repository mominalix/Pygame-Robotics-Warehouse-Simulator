import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
style.use('fivethirtyeight')

fig, axs = plt.subplots(2,2)

def animate(i):
    graph_data1 = open('Graphs\R1.txt','r').read()
    graph_data2 = open('Graphs\R2.txt', 'r').read()
    graph_data3 = open('Graphs\R3.txt', 'r').read()
    graph_data4 = open('Graphs\R4.txt', 'r').read()
    lines1 = graph_data1.split('\n')
    lines2 = graph_data2.split('\n')
    lines3 = graph_data3.split('\n')
    lines4 = graph_data4.split('\n')
    xs1 = []
    xs2 = []
    xs3 = []
    xs4 = []
    ys1 = []
    ys2 = []
    ys3 = []
    ys4 = []

    for line1, line2, line3, line4 in zip(lines1, lines2, lines3, lines4):
        if len(line1) > 1:
            x, y = line1.split(',')
            xs1.append(float(x))
            ys1.append(float(y))
        if len(line2) > 1:
            x, y = line2.split(',')
            xs2.append(float(x))
            ys2.append(float(y))
        if len(line3) > 1:
            x, y = line3.split(',')
            xs3.append(float(x))
            ys3.append(float(y))
        if len(line4) > 1:
            x, y = line4.split(',')
            xs4.append(float(x))
            ys4.append(float(y))

    axs[0, 0].clear()
    axs[0, 0].plot(xs1, ys1)
    axs[0, 0].set_title('Robot 1')
    axs[0, 0].set(xlabel='Iterations',ylabel='Energy')
    axs[1, 0].clear()
    axs[1, 0].plot(xs2, ys2)
    axs[1, 0].set_title('Robot 2')
    axs[1, 0].set(xlabel='Iterations', ylabel='Energy')
    axs[0, 1].clear()
    axs[0, 1].plot(xs3, ys3)
    axs[0, 1].set_title('Robot 3')
    axs[0, 1].set(xlabel='Iterations', ylabel='Energy')
    axs[1, 1].clear()
    axs[1, 1].plot(xs4, ys4)
    axs[1, 1].set_title('Robot 4')
    axs[1, 1].set(xlabel='Iterations', ylabel='Energy')


ani = animation.FuncAnimation(fig, animate, interval=1)
plt.subplots_adjust(hspace=0.3)
plt.show()

