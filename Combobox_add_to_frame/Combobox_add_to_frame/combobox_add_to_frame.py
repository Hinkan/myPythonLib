from tkinter import Frame, StringVar, Label, Button
from tkinter.ttk import Combobox
from Scroll_windows import ScrollFrame

#TODO possibility to resize

class combobox_add_to_frame:
    """
    Combobox that adds the selected items to a list below the combobox
    Attributes:
    """
    def __init__(self, parent, list_selected, list_options, scrollable=False):
        '''Parameters:
            parent(Frame):parent frame
            list_selected:the values added thorugh the combobox
            list_options:The values for the combobox
        '''
        self.scrollable=scrollable
        self.frame=Frame(parent)
        self.var_selected=StringVar()
        self.list_selected=list_selected
        self.cbox=Combobox(self.frame, textvariable=self.var_selected, values=list_options)
        self.cbox.bind("<<ComboboxSelected>>", self._update_list)
        self.cbox.grid(row=0, column=0, columnspan=2)
        if self.scrollable:
            self.sf=ScrollFrame(self.frame)
            self.sf.set_dimension((200,50))
            self.sf.grid(row=1, column=0, columnspan=2)
    
    def get_list_selected(self):
        return self.list_selected

    def _update_list(self, event):
        if self.var_selected.get() in self.list_selected:
            pass#allready in list
        else:

            self.list_selected.append(self.var_selected.get())
        self._redraw()
        
    def _redraw(self):
        if self.scrollable:
            a=self.sf.scrollframe.winfo_children()
            print(a)
            for child in self.sf.scrollframe.winfo_children():
                child.destroy()
            for row, sel in enumerate(self.list_selected):
                rowframe=Frame(self.sf.scrollframe)
            
                l1=Label(rowframe, text=sel)
                b1=Button(rowframe, text="X", command=lambda value=sel: self._delete_selected(value))
                l1.grid(row=row+1, column=0, sticky="w")
                b1.grid(row=row+1,column=1, sticky="e", padx=(10,0))
                rowframe.pack(anchor="e")
        else:
            for child in self.frame.winfo_children()[1:]:
                child.destroy()
            for row, sel in enumerate(self.list_selected):
                l1=Label(self.frame, text=sel)
                b1=Button(self.frame, text="X", command=lambda value=sel: self._delete_selected(value))
                l1.grid(row=row+1, column=0)
                b1.grid(row=row+1,column=1)


    def _delete_selected(self, sel):
        idx=self.list_selected.index(sel)
        self.list_selected.pop(idx)
        self._redraw()

    def grid(self, **kwargs):
        self.frame.grid(kwargs)

    def pack(self, **kwargs):
        self.frame.pack(kwargs)

if __name__ == "__main__":
    from tkinter import Tk, Button
    root=Tk()
    root.geometry("300x400")

    selected=[]
    values=["one", "two", "three"]

    cb=combobox_add_to_frame(root, selected, values, scrollable=True)
    cb.pack()

    Button(root, text="read", command=lambda: print(selected)).pack()


    root.mainloop()
