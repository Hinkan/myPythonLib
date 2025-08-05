from tkinter import Frame, Entry, Button
class Entry_integer_arrows:
    """
    Entry with buttons that increase/decreases the value, only works with integers
    Attributes:
        parentframe(Frame):parent frame
        textvariable:only works with intvar
        delta: stepsize for each button click, default 1
    """
    def __init__(self, parentframe, textvariable, delta=1):
        self.i=textvariable
        self.frame=Frame(parentframe)
        self.button_depressed=False
        self.delta=delta
        e=Entry(self.frame,textvariable=self.i,justify="c", width=10)
        b1=Button(self.frame,text="<")
        b2=Button(self.frame,text=">")
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
        self.frame.after_cancel(self.after_id)
        self.button_depressed=False
        
    def onMouseDown_inc(self, event):
        self.button_depressed=True
        self.delay=250
        self.increase()

    def onMouseUp_inc(self, event):
        self.frame.after_cancel(self.after_id)
        self.button_depressed=False

    def increase(self):
        if self.button_depressed:
            self.increment()
            if self.delay>1:
                self.delay=int(self.delay*0.9)
            self.after_id = self.frame.after(self.delay, self.increase)
    
    def decrease(self):
        if self.button_depressed:
            self.decrement()
            if self.delay>1:
                self.delay=int(self.delay*0.9)
            self.after_id = self.frame.after(self.delay, self.decrease)

    def grid(self, **kwargs):
        self.frame.grid(kwargs)

    def pack(self, **kwargs):
        self.frame.pack(kwargs)