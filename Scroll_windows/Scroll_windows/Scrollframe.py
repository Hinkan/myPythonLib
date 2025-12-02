from tkinter import Frame, Canvas, Scrollbar, Label
class ScrollFrame():
    """
    A frame with fixed size that can be scrolled
    Attributes:
        parent(frame):the parentframe
        border: if there should be border around the frame
        only_scroll_when_full: enables a less efficient scroll function that only scroll when the scroll frame is full of children
    """

    def __init__(self, parent, border=False, only_scroll_when_full=False) -> None:

        self.container=Frame(parent)#Contains the canvas
        if border:
            self.enable_border()
        self.only_scroll_when_full=only_scroll_when_full

        self.scrollcanvas=Canvas(self.container)#canvas that handles the repainting
        self.scrollcanvas.grid(row=1, column=0, sticky="nsew")

        self.scrollbar=Scrollbar(self.container, orient='vertical', command=self.scrollcanvas.yview)#add scrollbar
        self.scrollbar.grid(row=1, column=1, sticky='nsew')
        self.scrollcanvas['yscrollcommand']=self.scrollbar.set#no (), its set to a fucntion

        self.scrollframe=Frame(self.scrollcanvas)
        self.scrollcanvas.create_window(0,0,anchor="nw", window=self.scrollframe, tags="expand")
        self.rebind()#put into a separete function to be called from other places

    def set_label(self, label_text):
        Label(self.container, text=label_text).grid(row=0, column=0)
    def set_dimension(self, dim:tuple):
        self.scrollcanvas.config(width=dim[0],height=dim[1])
        self.scrollcanvas.create_window(0,0,anchor="nw", width=dim[0], window=self.scrollframe, tags="expand")


    def enable_border(self):
        self.container.configure(borderwidth=1, relief="groove")

    def scroll(self, event, widget):
        widget.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def scroll_when_full(self, event, widget):
        children=self.scrollframe.winfo_children()
        children_height=len(children)*children[0].winfo_height()
        container_height=self.container.winfo_height()
        if children_height>container_height:
            widget.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def final_scroll(self, event, widget, func):
        widget.bind_all("<MouseWheel>", func)


    def stop_scroll(self, event, widget):
        widget.unbind_all("<MouseWheel>")

    def move_to(self, target:float):
        """
        function to scroll to a place
        Parameter:
        target(float):0 is top, 1 is bottom
        """
        self.scrollcanvas.yview_moveto(target)

    def grid(self, **kwargs):
        self.container.grid(kwargs)

    def pack(self, **kwargs):
        self.container.pack(kwargs)

    def rebind(self):
        #When the cursor enters the scrollwindow bind the scrollwheel to the scroll function, unbind when it leaves
        #probably something like this in the scrollhandling of the treeview
        self.scrollframe.update_idletasks()
        self.scrollframe.bind('<Configure>', lambda e: self.scrollcanvas.configure(scrollregion=self.scrollcanvas.bbox('all')))
        self.scrollcanvas.config(scrollregion=self.scrollcanvas.bbox('all'))
        if self.only_scroll_when_full:
            self.scrollcanvas.bind("<Enter>", lambda event: self.final_scroll(event, self.scrollcanvas, lambda event: self.scroll_when_full(event, self.scrollcanvas)))
        else:
            self.scrollcanvas.bind("<Enter>", lambda event: self.final_scroll(event, self.scrollcanvas, lambda event: self.scroll(event, self.scrollcanvas)))
        self.scrollcanvas.bind("<Leave>", lambda event: self.stop_scroll(event, self.scrollcanvas))

if __name__ == "__main__":
    from tkinter import Tk, Button
    root=Tk()
    sf=ScrollFrame(root,True, only_scroll_when_full=True)
    #mylist=["item", "item", "item", "item", "item", "item", "item", "item", "item", "item", "item", "item", "item", "item", "item", "item", "item", "item" ]
    mylist=["item1", "item2"]
    for row, item in enumerate(mylist):         
            Label(sf.scrollframe, text=item).grid(row=row+1, column=0)
    sf.set_dimension((100,200))
    sf.pack()
    Button(root, text="scrolldown", command=lambda: sf.move_to(1)).pack()
    root.mainloop()