import os
from random import choices

import matplotlib.pyplot as plt
import seaborn as sns
from numpy import concatenate, linspace, sqrt, set_printoptions, array

from _models.data_keeper_model import DataKeeper
from _views.GUI.plotter import Plotter
from _views.GUI.printer import Printer
from _views.GUI.root_window import Application
from _views.helpers.string_formatter import PreformatArrayLikeData
from templates.EventSystem import Subscriber

initDots = [
    (50., 50.),
    (100., 50.),
    (50., 100.),
    (100., 100.)
]
newDots = [
    (55., 51.),
    (108., 47.),
    (45., 120.),
    (110., 120.)
]


class MainView(Subscriber):
    def __init__(self, event, dataPath=None):
        super().__init__(event)

        self.guiThread = None

        # Interface part
        self.app = Application(winWidth=600, winHeight=700)

        self.plotter = Plotter(self.app.gridElements.get((0, 0)), self.app.defaultColors)
        self.plotter.pack(expand=True, fill='both')

        self.printer = Printer(self.app.gridElements.get((1, 0)), self.app.defaultColors)
        self.printer.pack(expand=True, fill='both')
        # End of Interface part

        self.SvdData = None
        self.DataPath = None

        if dataPath is not None:
            self.ValidatePath(dataPath)
        else:
            raise TypeError("None cannot be considered a file path")

    def ValidatePath(self, pathStr):
        if os.path.isfile(pathStr):
            self.DataPath = pathStr
        else:
            raise FileNotFoundError

    @staticmethod
    def PlotVectors(vecs, cols, alpha=1):
        """
        Plot set of vectors.

        Parameters
        ----------
        vecs : array-like
            Coordinates of the vectors to plot. Each vectors is in an array. For
            instance: [[1, 3], [2, 2]] can be used to plot 2 vectors.
        cols : array-like
            Colors of the vectors. For instance: ['red', 'blue'] will display the
            first vector in red and the second in blue.
        alpha : float
            Opacity of vectors

        Returns:

        fig : instance of matplotlib.figure.Figure
            The figure of the vectors
        """
        plt.axvline(x=0, color='#A9A9A9', zorder=0)
        plt.axhline(y=0, color='#A9A9A9', zorder=0)

        for i in range(len(vecs)):
            if isinstance(alpha, list):
                alpha_i = alpha[i]
            else:
                alpha_i = alpha
            x = concatenate([[0, 0], vecs[i]])
            plt.quiver([x[0]],
                       [x[1]],
                       [x[2]],
                       [x[3]],
                       angles='xy', scale_units='xy', scale=1, color=cols[i],
                       alpha=alpha_i)

    def MatrixToPlot(self, matrix, vectorsCol=['#FF9A13', '#1190FF']):
        """
        Modify the unit circle and basis vector by applying a matrix.
        Visualize the effect of the matrix in 2D.

        Parameters
        ----------
        matrix : array-like
            2D matrix to apply to the unit circle.
        vectorsCol : HEX color code
            Color of the basis vectors

        Returns:

        fig : instance of matplotlib.figure.Figure
            The figure containing modified unit circle and basis vectors.
        """

        # Unit circle
        x = linspace(-1, 1, 100000)
        y = sqrt(1 - (x ** 2))

        # Modified unit circle (separate negative and positive parts)
        x1 = matrix[0, 0] * x + matrix[0, 1] * y
        y1 = matrix[1, 0] * x + matrix[1, 1] * y
        x1_neg = matrix[0, 0] * x - matrix[0, 1] * y
        y1_neg = matrix[1, 0] * x - matrix[1, 1] * y

        # Vectors
        u1 = [matrix[0, 0], matrix[1, 0]]
        v1 = [matrix[0, 1], matrix[1, 1]]

        self.PlotVectors([u1, v1], cols=[vectorsCol[0], vectorsCol[1]])

        plt.plot(x1, y1, 'g', alpha=0.5)
        plt.plot(x1_neg, y1_neg, 'g', alpha=0.5)

    @staticmethod
    def DisplayEntries(entries):
        print("\n\nThe object <entries> is type of: ", type(entries), '\n', entries, '\n')

    def StartView(self):
        print('\nApplication has started drawing {} UI'.format(type(self).__name__))
        # if self.guiThread in None:
        #     self.guiThread = threading.Thread(target=self.ReDrawGUI)
        #     self.guiThread.start()

    def ReDrawGUI(self):
        if isinstance(self.app, Application):
            self.app.mainloop()

    def EndView(self):
        print('\nEnd of Process')
        self.app.destroy()

    def RenderPlots(self):
        sns.set()
        set_printoptions(suppress=True)

        # Unit circle
        self.MatrixToPlot(array([[1, 0],
                                 [0, 1]]))
        plt.xlim(-1.1, 1.1)
        plt.ylim(-1.1, 1.1)
        plt.savefig(DataKeeper().root_dir+'/solution/plots/1.pdf')
        plt.show()
        print('Initial Unit circle - Done')

        self.MatrixToPlot(self.SvdData.get('V'))
        plt.xlim(-.25, .25)
        plt.ylim(-.25, .25)
        plt.savefig(DataKeeper().root_dir+'/solution/plots/2.pdf')
        plt.show()
        print('First transformation - Done')

        # self.MatrixToPlot(diag(self.SvdData.get('S')).dot(self.SvdData.get('V')))
        self.MatrixToPlot(self.SvdData.get('S').dot(self.SvdData.get('V')))
        # S[0: 8, :].dot(V)
        plt.xlim(-9, 9)
        plt.ylim(-9, 9)
        plt.savefig(DataKeeper().root_dir+'/solution/plots/3.pdf')
        plt.show()
        print('Second transformation - Done')

        self.MatrixToPlot(self.SvdData.get('U').dot(self.SvdData.get('S').dot(self.SvdData.get('V'))))
        plt.xlim(-4, 4)
        plt.ylim(-4, 4)
        plt.savefig(DataKeeper().root_dir+'/solution/plots/4.pdf')
        plt.show()
        print('Third transformation - Done')

    def Update(self):
        """Method is invoked whenever an <Event> State (the subscriber is subscribed to) has been changed"""
        try:
            self.DisplayEntries(self.Subscription.GetEntryByKey('csv_model_data'))
        except IndexError:
            print("TOO SOON! You have awaken me TOO SOON, Executus!")
            print("CSV is not ready yet!")

        try:
            self.SvdData = self.Subscription.GetEntryByKey('svd_model_data')
            print("\nThe Solution is:\n", self.SvdData.get('Solution'))
            print("\nError Value is: \n", self.SvdData.get('Error'), "\n\n")
            self.RenderPlots()
        except IndexError:
            print("TOO SOON! You have awaken me TOO SOON, Executus!")
            print("SVD is not ready yet")

        initDotsColor, newDotsColor = choices(self.app.defaultColorScheme, k=2)
        self.plotter.DisplayDots(initDots, initDotsColor)
        self.plotter.DisplayDots(newDots, newDotsColor, isFilled=False)
        self.printer.Print(PreformatArrayLikeData(array_like_data=initDots, array_name="Initial Dots"), initDotsColor)
        self.printer.Print("\n" + PreformatArrayLikeData(array_like_data=newDots, array_name="New Dots"), newDotsColor)
