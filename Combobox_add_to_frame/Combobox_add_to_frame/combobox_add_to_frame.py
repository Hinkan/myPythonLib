from tkinter import Frame, StringVar, Label, Button
from tkinter.ttk import Combobox

class combobox_add_to_frame:
    def __init__(self, parent, list_selected, list_options):
        self.frame=Frame(parent)
        self.var_selected=StringVar()
        self.list_selected=list_selected
        self.cbox=Combobox(self.frame, textvariable=self.var_selected, values=list_options)
        self.cbox.bind("<<ComboboxSelected>>", self._update_list)
        self.cbox.grid(row=0, column=0, columnspan=2)
    
    def get_list_selected(self):
        return self.list_selected

    def _update_list(self, event):
        if self.var_selected.get() in self.list_selected:
            pass#allready in list
        else:
            self.list_selected.append(self.var_selected.get())
        self._redraw()
        
    def _redraw(self):
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

