import numpy as np
from matplotlib import pyplot as plt
from random import uniform
import queue


def func():
    x, k = 0, 0
    while x < 1:
        x += uniform(0, 1)
        k += 1
    return k


def optimize_plot(iteration, lim, multiplier, global_lim):
    if iteration < lim and iteration % multiplier == 0:
        return True
    elif lim < global_lim:
        return optimize_plot(iteration, lim * 2, multiplier * 2, global_lim)
    else:
        return False


# params
N = 50000  # Number of iterations
K = 7  # Maximum value of func() represented of the histogram
L = 20  # Number of elements for convergence chart
save = True
plot = True

# variables
res = 0  # Sum of all func() values
fd = []  # All func() values
last_ones = queue.Queue(L + 1)  # Last L func() values

# init
fig = plt.figure()
main_axes = fig.add_axes([0.1, 0.55, 0.85, 0.4])
hist_axes = fig.add_axes([0.1, 0.05, 0.35, 0.4])
convergence_axes = fig.add_axes([0.55, 0.05, 0.4, 0.4])

for i in range(N):
    f = func()
    if f < K:
        fd.append(f)

    res += f
    if i > 0:
        exp_here = res / i
        ratio_here = exp_here / np.exp(1)
        last_ones.put(exp_here)
        convergence_here = 0
        if i > L:
            prev_elem = last_ones.get()
            convergence_here = (exp_here/np.exp(1)) / (prev_elem/np.exp(1))
        if not plot:
            print(i, exp_here, ratio_here, convergence_here)
            continue
        plot_here = optimize_plot(i, 200, 1, N)
        save_here = optimize_plot(i, 100, 1, N) and save

        if plot_here or i == N - 1:
            main_axes.scatter(i, exp_here, color='red', s=3)
            main_axes.plot([i - 1, i], [np.exp(1), np.exp(1)], color='black', linewidth='1')
            main_axes.scatter(i, ratio_here, color='green', s=3)
            main_axes.plot([i - 1, i], [1, 1], color='black', linewidth='1')
            main_axes.set_title("Calculated e = {0:.10f}, Ratio to real e = {1:.10f}".format(exp_here, ratio_here))

            if save_here or i == N - 1:
                hist_axes.clear()
                hist_axes.hist(fd, range(1, K + 1), align='left', color='orange')
                hist_axes.set_title("Number of trials = {0}".format(i))

                convergence_axes.clear()
                convergence_axes.set_title("Convergence = {0:.5f}".format(convergence_here))
                convergence_axes.plot(range(len(last_ones.queue)), last_ones.queue)
                convergence_axes.plot([0, L], [np.exp(1), np.exp(1)], color='black')

        if save_here:
            plt.savefig('figures/fig{0:5}'.format(i))

if plot:
    plt.show()
