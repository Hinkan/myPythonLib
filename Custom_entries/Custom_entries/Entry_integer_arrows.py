from tkinter import Entry, Button, IntVar


#TODO change the cursor when hovering the arrows
class Entry_integer_arrows(Entry):
    """
    Entry with buttons that increase/decreases the value, only works with integers
    Attributes:
        parentframe(Frame):parent frame
        variable:only works with intvar
        delta: stepsize for each button click, default 1
    """
    def __init__(self, parent, variable, delta=1):
        super().__init__(parent)
        self.i=variable
        #self=Frame(parentframe)
        self.button_depressed=False
        self.delta=delta
        e=Entry(self,textvariable=self.i,justify="c", width=10)
        b1=Button(self,text="<", cursor="arrow")
        b2=Button(self,text=">", cursor="arrow")
        b1.grid(row=0, column=0, sticky="e")
        e.grid(row=0, column=1)
        b2.grid(row=0, column=2, sticky="w")
        b1.bind("<ButtonPress-1>", self.onMouseDown_dec)
        b1.bind("<ButtonRelease-1>", self.onMouseUp_dec)
        b2.bind("<ButtonPress-1>", self.onMouseDown_inc)
        b2.bind("<ButtonRelease-1>", self.onMouseUp_inc)
        
    def decrement(self):
        self.i.set(self.i.get()-self.delta)

    def increment(self):
        self.i.set(self.i.get()+self.delta)
    
    def onMouseDown_dec(self, event):
        self.button_depressed=True
        self.delay=250
        self.decrease()

    def onMouseUp_dec(self, event):
        self.after_cancel(self.after_id)
        self.button_depressed=False
        
    def onMouseDown_inc(self, event):
        self.button_depressed=True
        self.delay=250
        self.increase()

    def onMouseUp_inc(self, event):
        self.after_cancel(self.after_id)
        self.button_depressed=False

    def increase(self):
        if self.button_depressed:
            self.increment()
            if self.delay>1:
                self.delay=int(self.delay*0.9)
            self.after_id = self.after(self.delay, self.increase)
    
    def decrease(self):
        if self.button_depressed:
            self.decrement()
            if self.delay>1:
                self.delay=int(self.delay*0.9)
            self.after_id = self.after(self.delay, self.decrease)


if __name__ == "__main__":
    from tkinter import Tk, Button
    root=Tk()
    root.geometry("300x400")
    txtvar=IntVar()
    Entry_integer_arrows(root,variable=txtvar).pack()
    Button(root, command=lambda: print(txtvar.get())).pack()

    root.mainloop()