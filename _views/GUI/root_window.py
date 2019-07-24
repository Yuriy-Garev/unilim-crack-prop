import tkinter as tk

from templates.helpers.clamp_value import ClampPositive as clamp


class Application(tk.Tk):
    def __init__(self, appTitle='Application', winWidth=None, winHeight=None):
        tk.Tk.__init__(self)
        if winWidth is None:
            self.winWidth = int(self.winfo_screenwidth() / 2)
        else:
            self.winWidth = winWidth

        if winHeight is None:
            self.winHeight = int(self.winfo_screenheight())
        else:
            self.winHeight = winHeight

        self.title(appTitle)
        self.resizable(0, 0)
        self.RaiseAboveAll()
        self.geometry("{}x{}".format(self.winWidth, self.winHeight))
        self.grid()
        self.currentGridSize = None
        self.gridElements = None
        self.ResetGrid(1, 1)
        self.defaultColors = {
            "defaultText": "#edffff",
            "defaultDarkBg": "#151515",
            "defaultSemiDarkBg": "#212121",
            "defaultGridLine": "#474747",
            "defaultSubGridLine": "#2e2e2e"
        }

        self.defaultColorScheme = ["#427ec7",
                                   "#ff8530",
                                   "#1db955",
                                   "#d4d4d2",
                                   "#fe2f53",
                                   "#c2e988",
                                   "#ac7965",
                                   "#7dcbc4",
                                   "#c88fec",
                                   "#ffcc63",
                                   "#f98c68",
                                   "#ff4d32",
                                   "#80a8ff",
                                   "#f26092",
                                   "#ffcd00"
                                   ]

        self.SetWindowAlpha(0.95)

    def SetWindowAlpha(self, alpha):
        alpha = clamp(alpha, 1)
        self.attributes("-alpha", alpha)

    def ResetWindowAlpha(self):
        self.attributes("-alpha", 1)

    def RaiseAboveAll(self):
        self.lift()
        self.attributes('-topmost', 1)
        self.attributes('-topmost', 0)

    @property
    def GridElementSpace(self):
        width = int(self.winWidth / self.currentGridSize[0])
        height = int(self.winHeight / self.currentGridSize[1])
        return tuple([width, height])

    def ResetGrid(self, rows, cols):
        gridRows = 0
        gridColumns = 0
        oldGridSize = self.currentGridSize

        while gridRows < rows:
            self.rowconfigure(gridRows, weight=1)
            gridRows += 1

        while gridColumns < cols:
            self.columnconfigure(gridColumns, weight=1)
            gridColumns += 1

        self.currentGridSize = (gridColumns, gridRows)

        if self.gridElements is None:
            self.gridElements = {}
            for i in range(gridRows):
                for j in range(gridColumns):
                    self.gridElements.update({(i, j): self.AddGridElement(i, j)})
        else:
            for i in range(gridRows):
                for j in range(gridColumns):
                    if i in range(oldGridSize[1]) and j in range(oldGridSize[0]):
                        self.gridElements.update({(i, j): self.UpdateGridElement(i, j)})
                    else:
                        self.gridElements.update({(i, j): self.AddGridElement(i, j)})

    def AddGridElement(self, row, col):
        width, height = self.GridElementSpace
        frame = tk.Frame(self, width=width, height=height, bd=0, highlightthickness=0, relief='flat')
        frame.grid(row=row, column=col, sticky=tk.N + tk.S + tk.E + tk.W)
        return frame

    def UpdateGridElement(self, row, col):
        width, height = self.GridElementSpace
        self.gridElements.get((row, col)).config(width=width, height=height)
        return self.gridElements.get((row, col))

# def main():
#     app = Application(winHeight=700)
#     app.mainloop()  # Wait for events
#     exit(0)
#
#
# if __name__ == '__main__':
#     main()
