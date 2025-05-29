from tkinter import Entry, Frame, Label
from tkinter import BooleanVar, StringVar, IntVar
class Entry_validate:
    """
    Entry which validates the characters entered
    Attributes:
        parent(frame): tkinter parent Frame
        dtype(str): what datatype to validate
        length(int): the length to validate
        orientation(str): h or v
    """
    def __init__(self, parent, dtype, length=None, lengthcompare=None, orientation="h"):
        '''
        Initialize entry with validation
        Parameters:
            parent(frame): tkinter parent Frame
            dtype(str): what datatype to validate
            length(int): the length to validate
            lengthcompare(literal):G:greather than, L:lesser than, E: equal, None 
            orientation(str): h or v
        '''
        self.supported_dtypes=["int", "float", "str"]
        self.parent=parent
        self.valid_bool=BooleanVar
        self.dtype=dtype
        self.length=length
        self.lengtcompare=lengthcompare

        self.result_string=StringVar()
        self.frame=Frame(parent)
        validation=(self.frame.register(self._validate))
        
        self.e=Entry(self.frame, validate="focusout", validatecommand=(validation, '%P'))
        self.l_val=Label(self.frame, textvariable=self.result_string, fg="red", width=15, anchor="w")
        if orientation=="h":
            self.e.grid(row=0, column=0)
            self.l_val.grid(row=0, column=1)
        else:
            self.e.grid(row=0, column=0)
            self.l_val.grid(row=1, column=0)
    
    def _validate(self, P):
        """
        Internal function to validate 
        Validates P is the correct datatype and correct length
        Parameters:
            P(str): value to validate
        """
        if len(P)==0:
            self.result_string.set("empty")
            self.valid_bool=False
            return False
        
        if self.dtype not in self.supported_dtypes:
            print("unsuported data type")
            self.valid_bool=False
            return False
        if self.dtype=="int":
            type_ok=True
            try:
                if not P.isnumeric():
                    type_ok=False
            except:
                type_ok=False
            if not type_ok:
                self.result_string.set("Wrong data type")
                self.valid_bool=False
                return False
        
        if self.dtype=="float" :
            type_ok=True
            try:
                float(P)
            except:
                type_ok=False

            if not type_ok:
                self.result_string.set("Wrong data type")
                self.valid_bool=False
                return False
        if self.lengtcompare !=None:
            if self.lengtcompare=="E":
                if self._comparelength(P, "L", self.length):
                    self.result_string.set("To short")
                    self.valid_bool=False
                    return False
                if len(P) > self.length:
                    self.result_string.set("To long")
                    self.valid_bool=False
                    return False
            if self.lengtcompare=="G":
                if not self._comparelength(P, "G", self.length):
                    self.result_string.set("To short")
                    self.valid_bool=False
                    return False
            if self.lengtcompare=="L":
                if not self._comparelength(P, "L", self.length):
                    self.result_string.set("To Long")
                    self.valid_bool=False
                    return False
                    
        self.result_string.set("")
        self.valid_bool=True
        return True
    
    def get(self):
        """
        Get the value from Entry if the value is valid
        """
        self._validate(self.e.get())
        if self.valid_bool:
            return self.e.get()
        else:
            return None
    def grid(self, **kwargs):
        self.frame.grid(kwargs)

    def pack(self, **kwargs):
        self.frame.pack(kwargs)
    
    def _comparelength(self, P, comparetype, comparelength):
        if comparetype =="E":
            if len(P)==comparelength:
                return True
            else:
                return False
        elif comparetype =="G":
            if len(P)>comparelength:
                return True
            else:
                return False
        elif comparetype =="L":
            if len(P)< comparelength:
                return True
            else:
                return False
        else:
            print("unknown comparetype in Entry validate")
            return False
        



if __name__ == "__main__":
    
    entrylist=[]

    def readentry():
        for etn in entrylist:
            print(f"e1:{etn.get()}")
                  
     



    from tkinter import Tk, Button
    root=Tk()
    root.geometry("300x400")
    #
    #Entry_validate(root, "str", 5, "G").pack()
    #Entry_validate(root, "str", 5, "L").pack()
    #Entry_validate(root, "str", 5, "E").pack()
    #Entry_validate(root, "int", None, None).pack()
    e1=Entry_validate(root, "int")
    e2=Entry_validate(root, "int")
    entrylist=[e1,e2]
    e1.pack()
    e2.pack()
    Button(root, text="read entries", command=readentry).pack()


    root.mainloop()