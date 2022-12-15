from tkinter import *
from tkinter import ttk
import AiVirtualMouseProject as ai

root = Tk()   



def get_slider_values(event):
    print(slider.get())
    


def play():
    v = slider.get()
    mouse=ai.AiMouse(v)
    root.destroy()
    # print("v=",v)
    mouse.run()  

root.geometry("400x300")
root.minsize(400, 300)

slider = Scale(root, from_=1, to=100, orient=HORIZONTAL, command=get_slider_values)
# slider.set(10)
slider.pack()

btn = Button(root, text="RUN", command=play)
btn.pack()

txt = Label(root, text="hello")
txt.pack()
# a=get_slider_values(SCROLL)
root.mainloop()




