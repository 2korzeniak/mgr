import warnings
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")


# Klasa do tworzenia spersonalizowanych wykresów
class CustomDelayPlots:
    def __init__(self, s_x=11, s_y=5, nrows=1, ncols=1):
        sns.set_style("white")
        sns.set_context("notebook", font_scale=1.2, rc={"lines.linewidth": 2.5})
        self.fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(s_x, s_y))
        if nrows == 1 and ncols == 1:
            self.axs = np.reshape(axs, (1, -1))
        elif nrows == 1:
            self.axs = np.reshape(axs, (1, -1))
        elif ncols == 1:
            self.axs = np.reshape(axs, (-1, 1))

    # Ustawianie zakresów
    def set_xlim(self, lim_down, lim_up):
        self.axs[self.ix, self.iy].set_xlim([lim_down, lim_up])

    def set_ylim(self, lim_down, lim_up):
        self.axs[self.ix, self.iy].set_ylim([lim_down, lim_up])

    def set_xlabel(self, label, fontsize):
        self.axs[self.ix, self.iy].set_xlabel(label, fontsize=fontsize)

    def set_ylabel(self, label, fontsize):
        self.axs[self.ix, self.iy].set_ylabel(label, fontsize=fontsize)

    # Aktualizacja pozycji
    def update_position(self, ix, iy):
        self.ix, self.iy = ix, iy

    # Definiowanie stylu wykresu
    def def_style(self):
        self.axs[self.ix, self.iy].spines['top'].set_visible(False)
        self.axs[self.ix, self.iy].spines['right'].set_visible(False)
        self.axs[self.ix, self.iy].yaxis.grid(color='grey', linestyle=':')
        self.axs[self.ix, self.iy].xaxis.grid(color='grey', linestyle=':')
        self.axs[self.ix, self.iy].tick_params(axis='both', which='major', labelsize=10, size=5)

    # rysowanie wykresu
    def draw_custom_plot(self, x, y, color='blue', line_style='-', line_width=1, marker=None, label=''):
        if marker:
            marker_facecolor, marker, marker_size = marker[:]
            self.axs[self.ix, self.iy].plot(x, y, color=color, linestyle=line_style, linewidth=line_width,
                                            marker=marker, label=label, markerfacecolor=marker_facecolor,
                                            markersize=marker_size)
        else:
            self.axs[self.ix, self.iy].plot(x, y, color=color, linestyle=line_style, linewidth=line_width, label=label)
        self.fig.autofmt_xdate()

    # rysowanie wykresu data
    def draw_custom_plot_date(self, x, y, color='lightblue', linestyle='-', linewidth=1, markeredge=False, label=''):
        marker_edgewdth = 1 if markeredge else 0
        self.axs[self.ix, self.iy].plot_date(x, y, color='lightblue', markeredgecolor='grey',
                                             markeredgewidth=marker_edgewdth, label=label)

    # rysowanie wykresu scatter
    def cust_scatter(self, x, y, color='lightblue', markeredge=False, label=''):
        marker_edgewdth = 1 if markeredge else 0
        self.axs[self.ix, self.iy].scatter(x, y, color=color,  edgecolor='grey', linewidths=marker_edgewdth,
                                           label=label)

    # Rysowanie legendy
    def draw_legend(self, location='upper right'):
        legend = self.axs[self.ix, self.iy].legend(loc=location, shadow=True, facecolor='green', frameon=True)
        legend.get_frame().set_facecolor('grey')

    # zapis do pliku
    def save_file(self, name):
        self.fig.savefig(name)
