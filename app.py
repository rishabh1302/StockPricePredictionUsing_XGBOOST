import tkinter
from tkinter import ttk
from Window.utilities import *
#initializations

class GUI:
    def __init__(self, master):

        self.iconnum = tkinter.IntVar()
        self.master = master
        self.master.title('test')
        self.master.resizable(width=False, height=False)
        self.master.maxsize(500, 250)
        self.master.minsize(500, 250)
        self.test1 = tkinter.Radiobutton(master, text="test11111111", variable=self.iconnum,
                                 value=1, )
        self.test2 = tkinter.Radiobutton(master, text="test2", variable=0, value=2, )
        self.test3 = tkinter.Radiobutton(master, text="test3", variable=0, value=3, )
        self.test4 = tkinter.Radiobutton(master, text="test4", variable=0, value=4)
        self.test1.grid(row=2, columnspan=1)
        self.test2.grid(row=2, columnspan=2)
        self.test3.grid(row=3, column=1)
        self.test4.grid(row=3, column=0)

        self.Checker = tkinter.Radiobutton(master, text="test5", indicatoron=0, height=3, width=35,
                                   value=10, command=self.icon_switcher) #var=Selection)
        self.Turbo = tkinter.Radiobutton(master, text="test6", indicatoron=False, height=1, width=35,
                                 value=4, command=self.icon_switcher) #var#=Selection)

        self.Checker.grid(row=1)
        self.Turbo.grid(row=1, column=1,   )
        self.exitButton = tkinter.Button(master,text="Exit",command=self.disappear)
        self.exitButton.grid(row=2,column=3,)

    def disappear(self):
        self.test1.pack_forget() 

    def icon_switcher(self):
        print("Hello")

root = tkinter.Tk()

gui = GUI(root)

#add elements
# quitButton = ttk.Button(root, text="Exit",command = myQuit)
# quitButton.pack()

#run event loop
root.mainloop()
