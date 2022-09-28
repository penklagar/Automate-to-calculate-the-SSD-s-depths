#loading the modules
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk

root = tk.Tk()
root.title('iMAGE ANALYZER')
#root.iconbitmap()
root.geometry("600x400")  # Size of the window

#create the Main Frame
main_frame = Frame(root)
main_frame.pack(fill= BOTH, expand=1)

#create a canvas
my_canvas = Canvas(main_frame)
my_canvas.pack(side =LEFT, fill =BOTH, expand=1)

#add a scrollbar to the canvas
my_scrollbar = ttk.scrollbar(main_frame, orient= VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

#configure the canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

#create another frame inside the canvas
second_frame = Frame(my_canvas)

#add that new frame to a window in the canvas
my_canvas.create_window((0,0), window=second_frame, anchor="nw")


my_font1=('times', 18, 'bold')
l1 = tk.Label(second_frame,text='Upload Files & display',width=30,font=my_font1)
l1.grid(row=1,column=1,columnspan=4)
b1 = tk.Button(second_frame, text='Import',
               width=15,command = lambda:upload_file())
b1.grid(row=2,column=20,columnspan=20)

b2 = tk.Button(second_frame, text='Select single',
               width=15,command = lambda:upload_file())
b2.grid(row=3,column=20,columnspan=20)
b3 = tk.Button(second_frame, text='Evaluate single',
               width=15,command = lambda:upload_file())
b3.grid(row=4,column=20,columnspan=20)
b4 = tk.Button(second_frame, text='Evaluate all',
               width=15,command = lambda:upload_file())
b4.grid(row=5,column=20,columnspan=20)

  
  
def upload_file():
    f_types = [('jpeg Files', '*.jpeg'),('jpg Files', '*.jpg'),
    ('PNG Files','*.png')]   # type of files to select
    filename = tk.filedialog.askopenfilename(multiple=True,filetypes=f_types)
    col=1 # start from column 1
    row=3 # start from row 3
    for f in filename:
        img=Image.open(f) # read the image file
        img=img.resize((300,300)) # new width & height
        img=ImageTk.PhotoImage(img)
        e1 =tk.Label(second_frame)
        e1.grid(row=row,column=col)
        e1.image = img
        e1['image']=img # garbage collection
        if(col==3): # start new line after third column
            row=row+1 # start wtih next row
            col=1    # start with first column
        else:       # within the same row
            col=col+1 # increase to next column

root.mainloop()  # Keep the window open
