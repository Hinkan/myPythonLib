# Custom_entries
These should work as the tkinter Entry widget but with added functionality
## Usage
Grab the [package](Custom_entries\dist\custom_entries-0.1.0.tar.gz) and install it with pip.

## Entry_integer_arrows
adds arrows at the edges of the Entry wdget to quickly increase/decrease the value, only works for integers.

### Parameters
parentframe(Frame): parent frame 

textvariable(IntVar): tkinter.IntVar

delta(Int): (default=1) the step size

### Example

```Python
from tkinter import Tk, IntVar

from Custom_entries import Entry_integer_arrows

root=Tk()
root.geometry("200x200")
i_var=IntVar(root, 5)
entry_arrows=Entry_integer_arrows(root, i_var, delta=2)

entry_arrows.pack()

root.mainloop()

```

## Entry_validate
functions as tkinter.Entry but validates the data when the the widget is left

### Parameters
parent(frame): tkinter parent Frame

dtype(literal): what datatype to validate, supports "int", "float" and "str", note that numbers can be strings

length(int):(default=None) the length to validate

comaprison(literal):(default=None)"G":greather than, "L":lesser than, "E": equal

list_prohibited(list): a list of values that is prohibited

orientation(literal):(default "h") should the error message be to the left("h") or below("v") the entry

error_color(literal):(default="red") uses tkinter foreground colors

### Example
from tkinter import Tk, Button

from Custom_entries import Entry_validate

root=Tk()
root.geometry("300x400")

Entry_validate(root, "str", 5, "G").pack()#string longer than 5 characters
Entry_validate(root, "str", 5, "L").pack()#string shorter than 4 characters
Entry_validate(root, "str", 5, "E").pack()#string exactly 5 characters
Entry_validate(root, "int", None, None).pack()#int any length
Entry_validate(root, "float", None, None).pack()#float any length
Entry_validate(root, "int",list_prohibited=[1,2,3]).pack()#int any length, not 1,2 or 3
Entry_validate(root, "float",list_prohibited=[1.0,2.0,3.5], error_color="blue").pack()#float any length, not 1.0, 2.0, 3.5, blue text
Entry_validate(root, "str",3, "E", list_prohibited=["foo", "bar"], orientation="v").pack()#str, exactly 3 characters, not "foo" or bar, error message below entry

root.mainloop()