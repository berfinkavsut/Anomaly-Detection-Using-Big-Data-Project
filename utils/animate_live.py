import matplotlib.pyplot as plt
import matplotlib  as mpl
import numpy as np

class AnimateLive:

    def __init__(self, time_limits=10, ax_num=2, x_labels=None, y_labels=None, plot_type='scat', color = "C3"):

        self.time_limits = time_limits
        plt.ion()

        w = int(round(ax_num/2))
        h = int(round(ax_num/w))

        self.fig, ax = plt.subplots(w, h, sharex=False, sharey=False, figsize=(18,12))
        self.ax = ax.flatten()
        self.plot_type = plot_type
        if plot_type is 'line':
            self.lines = [axis.plot([], [], color)[0] for index, axis in enumerate(self.ax)]
        if plot_type is 'scat':
            self.cmap = mpl.cm.magma_r
            self.norm = mpl.colors.Normalize(vmin=0,vmax=1)
            self.lines = [axis.scatter([], [], cmap=self.cmap, norm=self.norm ) for index, axis in enumerate(self.ax)]

        self.fig.canvas.draw()

        if x_labels is not None:
            for i in range(len(self.ax)):
                self.ax[i].set_xlabel(x_labels[i])



        if y_labels is not None:
            for i in range(len(self.ax)):
                self.ax[i].set_ylabel(y_labels[i])
                self.ax[i].set_ylim([0, 1])

        self.values = [[0] for i in range(len(self.ax))]
        self.time = [-1]



    def update_data(self, new_data, time_increment):
        values = self.values
        time = self.time

        time.append(time[-1] + time_increment)

        for i, value in enumerate(new_data):
            values[i].append(value)

    def update_graph(self):
        fig = self.fig
        ax = self.ax
        values = self.values
        time = self.time
        time_limits = self.time_limits
        plot_type = self.plot_type
        lines = self.lines
        cmap = self.cmap
        norm = self.norm

        for i, value in enumerate(values):

            if plot_type is 'line':
                lines[i].set_data(time, value)
            if plot_type is 'scat':
                lines[i].set_offsets(np.vstack((time, value)).T)
                lines[i].set_color(cmap(norm(value)))

            try:
                ax[i].set_xlim([time[-1] - time_limits, time[-1]])
                if max(value[-time_limits:]) > ax[i].get_ylim()[1]:
                    new_min = min(value[-time_limits:])
                    new_max = max(value[-time_limits:])
                    ax[i].set_ylim([new_min-abs(new_min)*0.2, new_max+abs(new_max)*0.2])
            except:
                continue

        fig.canvas.draw()
        plt.pause(.1)
