import tkinter as tk


class Printer(tk.Text):
    def __init__(self, parent, defaultColors=None):
        super().__init__(parent)
        self.__txt = None
        self.__defaultTextColor = defaultColors.get("defaultSemiDarkBg")
        scrollbar = tk.Scrollbar(parent)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=self.yview)
        self.config(yscrollcommand=scrollbar.set, padx=10, pady=10, wrap='word',
                    bg=defaultColors.get("defaultSemiDarkBg"),
                    bd=0, highlightthickness=0, relief='flat')

    @property
    def PrintableObject(self):
        if self.__txt is None:
            return ""
        else:
            return self.__txt

    @PrintableObject.setter
    def PrintableObject(self, string=None):
        if string is None:
            self.__txt = str(TypeError("Object type is None"))
        elif not isinstance(string, str):
            try:
                self.__txt = str(string)
            except [ValueError, TypeError]:
                print("The object {} of type {} is not convertible to str".format(id(string), type(string)))
                self.__txt = "<Missing text>"
        else:
            self.__txt = string

    @PrintableObject.deleter
    def PrintableObject(self):
        self.__txt = None

    def RestPrinter(self):
        self.delete(0.0, 'end')
        del self.PrintableObject

    def Print(self, text=None, color=None):
        if color is None:
            tag_name = "color-" + self.__defaultTextColor
        else:
            tag_name = "color-" + color

        if self.__txt is None:
            self.__txt = text
        elif self.__txt is not None and isinstance(self.__txt, str):
            self.__txt += text

        self.tag_configure(tag_name, font='bold_font', foreground=color)
        self.insert('end', text, tag_name)