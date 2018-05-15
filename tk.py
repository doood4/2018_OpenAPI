from tkinter import *



def process():
    print("산기대")

window = Tk()
button = Button(window, text="클릭!",command=process)
button.pack()

window.mainloop()



