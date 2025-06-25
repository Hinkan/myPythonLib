from tkinter import Frame, Canvas, Scrollbar, Label

class ScrollFrame():
    """
    A frame with fixed size that can be scrolled
    Attributes:
        parent(frame):the parentframe
    """

    def __init__(self, parent, border=False) -> None:

        self.container=Frame(parent)#Contains the canvas
        if border:
            self.enable_border()

        self.scrollcanvas=Canvas(self.container)#canvas that handles the repainting
        self.scrollcanvas.grid(row=1, column=0, sticky="nsew")

        self.scrollbar=Scrollbar(self.container, orient='vertical', command=self.scrollcanvas.yview)#add scrollbar
        self.scrollbar.grid(row=1, column=1, sticky='nsew')
        self.scrollcanvas['yscrollcommand']=self.scrollbar.set

        self.scrollframe=Frame(self.scrollcanvas)
        self.scrollcanvas.create_window(0,0,anchor="nw", window=self.scrollframe, tags="expand")
        self.rebind()#put into a separete function to be called from other places

    def set_label(self, label_text):
        Label(self.container, text=label_text).grid(row=0, column=0)
    def set_dimension(self, dim:tuple):
        self.scrollcanvas.config(width=dim[0],height=dim[1])

    def enable_border(self):
        self.container.configure(borderwidth=1, relief="groove")
    def scroll(self, event, widget):
        widget.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def final_scroll(self, event, widget, func):
        widget.bind_all("<MouseWheel>", func)


    def stop_scroll(self, event, widget):
        widget.unbind_all("<MouseWheel>")

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
        self.scrollcanvas.bind("<Enter>", lambda event: self.final_scroll(event, self.scrollcanvas, lambda event: self.scroll(event, self.scrollcanvas)))
        self.scrollcanvas.bind("<Leave>", lambda event: self.stop_scroll(event, self.scrollcanvas))
