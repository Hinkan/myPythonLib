from tkinter import Toplevel, Label, Button, Frame, StringVar


if __name__=="__main__":
    from Scrollframe import ScrollFrame
else:
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
        query_return: the reurnvalue for yesno/yesnocancel, read from the mainfunction with a trace_add listener
    """
    
    def __init__(self, parent, shortstring=None, single_stringlist=None, multi_stringlist=None, callback=None, buttonbool=None, query_return:StringVar=None, title=None, width=250, height=400, scrollwidth=200, scrollheight=300)->Frame:
        self.window=Toplevel(parent)
        if title!=None:
            self.window.title(title)
        self.height=height
        self.width=width
        self.scrollwidth=scrollwidth
        self.scrollheight=scrollheight
        
        self.window.geometry(f"{self.width}x{self.height}")
        
        self.window.lift()
        self.callback=callback
        self.buttonbool=buttonbool
        self.query_return=query_return

        self.shortstring=shortstring
        self.single_stringlist=single_stringlist
        self.multi_stringlist=multi_stringlist


    def warning(self):
        Label(self.window, text=self.shortstring ).grid(row=0, column=0)
        sf=ScrollFrame(self.window)
        sf.set_dimension((self.scrollwidth, self.scrollheight))
        for row, item in enumerate(self.single_stringlist):
            Label(sf.scrollframe, text=item).grid(row=row, column=0)
        sf.container.grid(row=1, column=0)
        Button(self.window, text="OK", command=lambda: self.close()).grid(row=2, column=0)

    def askalternatives(self):
        Label(self.window, text=self.shortstring ).grid(row=0, column=0)
        sf=ScrollFrame(self.window)
        
        sf.set_dimension((self.scrollwidth, self.scrollheight))
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
        try:
            self.callback()
        except:
            print("Scrollabel_messagebox.askalternatives callback failed")
        self.window.destroy()

    def yesno(self):
        Label(self.window, text=self.shortstring ).grid(row=0, column=0, columnspan=2)
        sf=ScrollFrame(self.window)
        sf.set_dimension((self.scrollwidth, self.scrollheight))
        for row, item in enumerate(self.single_stringlist):         
            Label(sf.scrollframe, text=item).grid(row=row+1, column=0)

        sf.container.grid(row=1, column=0, columnspan=2, padx=(10,10))
        self.confirmbutton=Button(self.window, text="Yes", command=lambda:self.query_return.set("Yes"))
        self.confirmbutton.grid(row=3, column=0)
        self.confirmbutton=Button(self.window, text="No", command=lambda:self.query_return.set("No"))
        self.confirmbutton.grid(row=3, column=1)

    def yesnocancel(self):
        Label(self.window, text=self.shortstring ).grid(row=0, column=1)
        sf=ScrollFrame(self.window)
        
        sf.set_dimension((self.scrollwidth, self.scrollheight))
        
        for row, item in enumerate(self.single_stringlist):         
            Label(sf.scrollframe, text=item).grid(row=row+1, column=0)

        sf.container.grid(row=1, column=0, columnspan=3)
        self.confirmbutton=Button(self.window, text="Yes", command=lambda:self.query_return.set("Yes"))
        self.confirmbutton.grid(row=3, column=0)
        self.confirmbutton=Button(self.window, text="No", command=lambda:self.query_return.set("No"))
        self.confirmbutton.grid(row=3, column=1)

        self.confirmbutton=Button(self.window, text="Cancel", command=lambda:self.query_return.set("Cancel"))
        self.confirmbutton.grid(row=3, column=2)


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

if __name__ == "__main__":
    
    def print_query(retvalue):
        print(retvalue.get())
    
    
    import tkinter as tk
    root = tk.Tk()
    retvalue=StringVar()
    retvalue.trace_add("write", lambda *argz :print_query(retvalue))
    width=250
    height=270
    scrollwidth=200
    scrollheight=200
    sm=Scrollable_messagebox(root, "this is to test", ["one", "two", "three","one", "two", "three","one", "two", "three","one", "two", "three","one", "two", "three","one", "two", "three","one", "two", "three","one", "two", "three","one", "two", "three","one", "two", "three","one", "two", "three"], query_return=retvalue, width=width, height=height, scrollwidth=scrollwidth, scrollheight=scrollheight)
    sm.yesno()
    
    
    root.mainloop()