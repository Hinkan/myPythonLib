from tkinter import Entry, Frame, Label
from tkinter import BooleanVar, StringVar

class Entry_validate:
    """
    Entry which validates the characters entered
    Attributes:
        parent(frame): tkinter parent Frame
        dtype(str): what datatype to validate
        length(int): the length to validate
        comparison(literl):what comparison should be done with the length
        list_prohibited(list): a list of values that is prhibited, returns falsee
        orientation(str): h or v
    """
    def __init__(self, parent, dtype, length=None, comparison=None, list_prohibited=[], orientation="h"):
        '''
        Initialize entry with validation
        Parameters:
            parent(frame): tkinter parent Frame
            dtype(str): what datatype to validate
            length(int): the length to validate
            comaprison(literal):G:greather than, L:lesser than, E: equal, None 
            orientation(str): h or v
        '''
        self.supported_dtypes=["int", "float", "str"]
        self.parent=parent
        self.valid_bool=BooleanVar
        self.dtype=dtype
        self.length=length
        self.comparison=comparison
        self.list_prohibited=list_prohibited

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
        P_typecast=None
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
            else:
                P_typecast=int(P)
        
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
            else:
                P_typecast=float(P)
        if self.comparison !=None:
            if self.comparison=="E":
                if self._comparelength(P, "L", self.length):
                    self.result_string.set("To short")
                    self.valid_bool=False
                    return False
                if len(P) > self.length:
                    self.result_string.set("To long")
                    self.valid_bool=False
                    return False
            if self.comparison=="G":
                if not self._comparelength(P, "G", self.length):
                    self.result_string.set("To short")
                    self.valid_bool=False
                    return False
            if self.comparison=="L":
                if not self._comparelength(P, "L", self.length):
                    self.result_string.set("To Long")
                    self.valid_bool=False
                    return False

        if P_typecast in self.list_prohibited:
            self.result_string.set("Value prohibited")
            self.valid_bool=False
            return False       
        self.result_string.set("")
        self.valid_bool=True
        return True
    
    def get(self):
        """
        Get the value from Entry if the value is valid, othevise returns None
        """
        self._validate(self.e.get())
        if self.valid_bool:
            if self.dtype=="int":
                return int(self.e.get())
            elif self.dtype=="float":
                return float(self.e.get())
            else:
                return self.e.get()
        else:
            return None
    def set_error(self, error_string):
        """
        a wrapper to manually set the error code
        """
        self.result_string.set(error_string)
    
    def _comparelength(self, P, comparetype, comparelength):
        '''
            Compare the length of P with comparelength using comparetype
            Parameters:
            P: string, int, float
            comparetype(literal): G:greather than, L:lesser than, E: equal, None 
            comparelength(int): the length to validate
        '''
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
        
    def grid(self, **kwargs):
        self.frame.grid(kwargs)

    def pack(self, **kwargs):
        self.frame.pack(kwargs)

    def config(self, **kvargs):#TODO should b
        try:
            self.e.config(**kvargs)
        except:
            print("faield")

if __name__ == "__main__":
    
    entrylist=[]

    def readentry():
        for etn in entrylist:
            print(f"e1:{etn.get()}")
                  
     



    from tkinter import Tk, Button
    root=Tk()
    root.geometry("300x400")
    #
    Entry_validate(root, "str", 5, "G").pack()
    Entry_validate(root, "str", 5, "L").pack()
    Entry_validate(root, "str", 5, "E").pack()
    Entry_validate(root, "int", None, None).pack()
    
    Entry_validate(root, "float", None, None).pack()
    Entry_validate(root, "int", None, None).pack()
    
    Entry_validate(root, "int",list_prohibited=[1,2,3]).pack()
    
    Entry_validate(root, "float",list_prohibited=[1.0,2.0,3.5]).pack()
    
    Entry_validate(root, "float",3, "G").pack()
    #e1=Entry_validate(root, "int")
    #e2=Entry_validate(root, "int", list_prohibited=[1,2,3])
    #entrylist=[e1,e2]
    #e1.pack()
    #e2.pack()
    Button(root, text="read entries", command=readentry).pack()


    root.mainloop()