from tkinter import *
from PIL import ImageTk, Image

# Create an instance of tkinter window
win = Tk()

# Define the geometry of the window
win.geometry('1024x600')

frame = Frame(win, width=1024, height=600)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)

img = Image.open('media/images/logo-tri.png')
resized_image = img.resize((600,600), Image.ANTIALIAS)
new_image = ImageTk.PhotoImage(resized_image)

# Create a Label Widget to display the text or Image
label = Label(frame, image = new_image)
label.pack()

win.mainloop()

