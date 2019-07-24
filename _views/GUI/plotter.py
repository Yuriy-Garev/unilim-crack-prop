import tkinter as tk


class Plotter(tk.Canvas):
    def __init__(self, parent, defaultColors=None, **props):
        super().__init__(parent)
        self.config(background=defaultColors.get("defaultDarkBg"), bd=0, highlightthickness=0, relief='flat')
        self.dotsRadius = 4
        self.canvasSize = parent.winfo_toplevel().GridElementSpace
        self.config(width=self.canvasSize[0], height=self.canvasSize[1])
        if "isGrid" in props and props.get("isGrid") is True:
            if "gridTick" in props:
                self.gridTick = props.get("gridTick")
            else:
                self.gridTick = 20
            self.DrawGrid(gridTick=self.gridTick, gridColor=defaultColors.get("defaultGridLine"))

        if "isGrid" in props and props.get("isGrid") is True:
            if "subGridTick" in props:
                self.subGridTick = props.get("subGridTick")
            else:
                self.subGridTick = 20
            self.DrawGrid(gridTick=self.subGridTick, gridColor=defaultColors.get("defaultSubGridLine"))

    def DisplayDots(self, dotsArray, dotsColor, isFilled=True):
        if dotsArray is not None:
            for dot in dotsArray:
                x, y = dot
                self.DrawDot(x, y, radius=self.dotsRadius, color=dotsColor, fill=isFilled)
        else:
            print(ValueError("Received None instead of <array-like> object"))

    def DrawGrid(self, gridTick, gridColor):
        width, height = self.canvasSize
        hGridLinesCount = int(height / gridTick)
        vGriLinesCount = int(width / gridTick)

        for i in range(1, hGridLinesCount):
            self.tag_lower(
                self.create_line(0, i * gridTick, width, i * gridTick,
                                 fill=gridColor)
            )

        for i in range(1, vGriLinesCount):
            self.tag_lower(
                self.create_line(i * gridTick, 0, i * gridTick, height,
                                 fill=gridColor)
            )

    def DrawDot(self, center_x, center_y, radius, color, fill=True):
        x1 = center_x - radius
        y1 = center_y - radius
        x2 = center_x + radius
        y2 = center_y + radius
        if fill:
            self.create_oval(x1, y1, x2, y2, fill=color, outline='')
        else:
            radius -= 1
            self.create_oval(x1, y1, x2, y2, fill='', outline=color)