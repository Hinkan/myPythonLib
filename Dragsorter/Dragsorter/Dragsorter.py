from tkinter import Tk, Canvas, Frame, font

class Dragsorter():
    def __init__(self, window, drag_list,callback=None, width=600, height=400, canvascolor="white", itemcolor='#E4E4E4', x_cord=15, y_cord=15):
        """
            A canvas with a row of entries which can be dragged and sorted
            Parameters:
                window(Frame):parent frame
                drag_list(list[str]):the list with the names that should be sorted
                callback:function to be called when a new row has been built
                width(int):width of the canvas
                height(int):height of the canvas
                x_cord(int):the start pixel of the sorted row
                y_cord(int):the pixel height of the sorted row
        """
        self.frame=Frame(window)
        self.drag_list=drag_list
        self.callback=callback
        self.width=width
        self.height=height
        self.canvascolor=canvascolor
        self.itemcolor=itemcolor
        self.canvas=Canvas(self.frame, width=self.width, height=self.height, bg=self.canvascolor, highlightbackground="black")
        self.canvas.grid(row=0, column=0)
        self.list_items=[]
        self.global_y=y_cord
        self.rowstart=x_cord
        self.font=font.nametofont("TkDefaultFont")#get the default font used, used to make the labelsizes automatically
        self._populate_item_list()#create the items

        self.canvas.bind( "<Button-1>", self._select_on_press)
        self.canvas.bind( "<B1-Motion>", self._movewrapper)
        self.canvas.bind( "<ButtonRelease-1>", self._deselect_on_release)


    def _populate_item_list(self):
        '''
        Build the initail list at creation
        '''
        for name in self.drag_list:
            self._add_item(name=name)
        self._build_row()#aligns the items in a row


    def update_draglist(self, new_list):
        '''
        Updates the drag_list
        Parameters:
            param new_list: list to overwrite the old list
        '''
        for item in self.list_items:#destroys the old items 
            item.destroy()

        self.drag_list=new_list#resets attributes 
        self.list_items=[]
        self._populate_item_list()#populates with the new list


    def _add_item(self, name, x_padding=10, x_min=40):
        '''Adds a _canvasitem to self.list_items
        Parameters:
            name(str):name of the item
            x_padding(int): padding to add some extra space before the name text 
        '''
        
        name_width=self.font.measure(name)+x_padding#with of the name+padding
        if name_width<x_min:
            name_width=x_min
        citem=_canvasitem(self.canvas,name, width=name_width, color=self.itemcolor)
        self.list_items.append(citem)
        
    def get(self):
        '''
        returns the list of names of the items current order
        '''
        return [item.name for item in self.list_items]
    
    def _select_on_press(self, event):
        '''
        selects the clicked item, if any
        '''
        for item in self.list_items:
            if item.in_area(event.x, event.y):
                self.selected_item=item#select item to move
                break#skip checking the items when one is found
    
    def _deselect_on_release(self, event):
        '''
        Deselect the selected item, moving it into the list, sorting it
        '''
        newx=event.x#get the cords where item is released
        self.selected_item.move(newx, self.global_y)#move the item to row y cord
        self._sort_order()#sort the itemlist based on x_cord
        self._build_row()#build the row
        self.selected_item=None#deselct item to move
                    
    def _movewrapper(self, event):
        '''
        allows moving the selected item around while inside the canvas
        '''
        if self.selected_item!= None:
            if 0<event.x and event.x<self.canvas.winfo_width()-self.selected_item.width-3:#-3 makes sure the border is within the canvas
                if 0<event.y and event.y<self.canvas.winfo_height()-self.selected_item.height-3:
                    self.selected_item.move(event.x,event.y)

    def _sort_order(self):
        '''
        Sorts the list of item based on their x cordinate
        '''
        self.list_items.sort(key=lambda x: x.x0)#sort based on x cord
    
    def _build_row(self):
        '''
        Moves  all the items to fit snuggly into a row, order is based on list_items
        '''
        x=self.rowstart
        for item in self.list_items:
            item.move(x, self.global_y)
            x+=item.width
        
        if self.callback!=None:
            self.callback()

    def grid(self, **kwargs):
        self.frame.grid(kwargs)

    def pack(self, **kwargs):
        self.frame.pack(kwargs)

#TODO add fontsize
class _canvasitem():
    def __init__(self,canvas, name, x0=10, y0=10, width=50, height=15, textoffset=5, color='#E4E4E4')->None:
        '''
        Only intended to be used with dragsroter

        Parameters:
            canvas: a parent canvas to house the items
            name: The name of the item, will also be displayed as text and the items value
            x0: X cordinate of top left corner
            y0: Y cordinate of top left corner
            width: The width of the item
            height: The height of the item
            textoffset: The distance from the edge to the text
            color: The color of the item
        '''
        self.name=name 
        self.x0=x0
        self.y0=y0
        self.canvas=canvas
        self.width=width
        if height==None:
            self.height=15
        else:
            self.height=height
        self.textoffset=textoffset
        x0=self.x0
        y0=self.y0
        x1=x0+self.width
        y1=y0+self.height
        
        self.rect=self.canvas.create_rectangle(x0, y0, x1, y1, tags=self.name, fill=color)#Create the rectangle
        self.text=self.canvas.create_text(x0+self.textoffset,y0, text=self.name)#create the text
        
    def move(self, x, y):
        '''
        Moves the item to the x,y cordinates
        :param x: x cord
        :param y: y cord
        '''
        self.x0=x
        self.y0=y
        self.canvas.moveto(self.rect, x,y)
        self.canvas.moveto(self.text, x+self.textoffset,y)
    
    def in_area(self, x,y)->bool:
        '''
        Is the cordinate x,y within the borders of the item
        :param x: x cord
        :param y: y cord
        :return: true if with  border
        :rtype: bool
        '''
        if self.x0<x and x<self.x0+self.width:#if within x 
            if self.y0<=y and y<=self.y0+self.height:#if within y
                return True
            else:
                return False
        else:
            return False

    def destroy(self):
        '''
        Destroys the item
        '''
        self.canvas.delete(self.rect)
        self.canvas.delete(self.text)


if __name__ == "__main__":
    def callback():
        print("callbback")
    root=Tk()
    drag_list=["oneone", "two", "three", "a much longer string to test how it will handle it"]
    ds=Dragsorter(root, drag_list,callback=callback, width=400,height=200)
    ds.frame.pack()
    newlist=["one", "twotwo", "lastone"]
    ds.update_draglist(newlist)
    


    root.mainloop()