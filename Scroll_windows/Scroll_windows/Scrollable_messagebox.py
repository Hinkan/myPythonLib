from tkinter import Toplevel, Label, Button, Frame
from Scroll_windows.Scrollframe import ScrollFrame
class Scrollable_messagebox():
    """
    Messagebox with scrollable part for
    Attributes:
        parent(Frame):parent frame
        shortstring(string):the first label
        single_stringlist(list[str]):list of strings,
        multi_stringlist(list[list[str]]):Each item in list is a lsit of alternatives for buttin of alternatives
        callback(function):
    """
    
    def __init__(self, parent, shortstring=None, single_stringlist=None, multi_stringlist=None, callback=None, buttonbool=None)->Frame:
        self.window=Toplevel(parent)
        
        self.window.geometry("250x400")
        self.window.lift()
        self.callback=callback
        self.buttonbool=buttonbool

        self.shortstring=shortstring
        self.single_stringlist=single_stringlist
        self.multi_stringlist=multi_stringlist


    def warning(self):
        Label(self.window, text=self.shortstring ).grid(row=0, column=0)
        sf=ScrollFrame(self.window)
        sf.set_dimension((200,300))
        for row, item in enumerate(self.single_stringlist):
            Label(sf.scrollframe, text=item).grid(row=row, column=0)
        sf.container.grid(row=1, column=0)
        Button(self.window, text="OK", command=lambda: self.close()).grid(row=2, column=0)

    def askalternatives(self):
        Label(self.window, text=self.shortstring ).grid(row=0, column=0)
        sf=ScrollFrame(self.window)
        sf.set_dimension((200,300))
        self.returnlist=self.single_stringlist.copy()
        self.buttonarray=self.multi_stringlist.copy()

        for row, tup in enumerate(zip(self.single_stringlist, self.multi_stringlist)):
            item=tup[0]
            alternatives=tup[1]
            Label(sf.scrollframe, text=item).grid(row=row+1, column=0)
            for column, alt in enumerate(alternatives):
                b=Button(sf.scrollframe, text=alt, command=lambda row=row,column=column, x=alt, original=item: self.set_returnlist(row, column, x, original))
                self.buttonarray[row][column]=b
                b.grid(row=row+1, column=column+1)
        sf.container.grid(row=1, column=0)
        self.confirmbutton=Button(self.window, text="Bekräfta", command=self.callback_and_close)
        self.confirmbutton.grid(row=3, column=0)
    
    def callback_and_close(self):
        self.callback()
        self.window.destroy()

    def yesno(self):
        pass

    def yesnocancel(self):
        pass

    def close(self):
        self.window.destroy()

    def set_returnlist(self, row, column, value, original):
        self.returnlist[row]=[original, value]
        for c in self.buttonarray[row]:
            c.config(relief="raised")
        self.buttonarray[row][column].config(relief="sunken")
    
    def confirm_pressed(self):#not used?
        self.buttonbool.set(True)

    def get_returnlist(self):
        return self.returnlist
    
    def config_command(self, newcommand):
        self.confirmbutton.config(command=newcommand)