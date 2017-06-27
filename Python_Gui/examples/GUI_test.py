try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = tk.Label(master, text="This is our first GUI!")
        self.label.pack()

#        self.greet_button = tk.Button(master, text="Greet", command=self.greet)
#        self.greet_button.pack()

        self.close_button = tk.Button(master, text="Close", command=master.quit)
        self.close_button.pack()
#        
#        self.mb = tk.Menubutton(master, text='condiments')
#        self.mb.grid()

#        self.mb.menu = tk.Menu(self.mb, tearoff=0)
#        self.mb['menu'] = self.mb.menu

#        self.mayoVar  = tk.IntVar()
#        self.ketchVar = tk.IntVar()
#        self.mb.menu.add_checkbutton(label='mayo', variable=self.mayoVar)
#        self.mb.menu.add_checkbutton(label='ketchup', variable=self.ketchVar)
#        self.mb.pack()
        
        self.inp1 = tk.Label(master, text="First Name")
        self.inp1.grid(row=0, column = 0)
        self.inp1.pack()
        #self.inp2 = tk.Label(master, text="Last Name")#.grid(row=1)

        self.e1 = tk.Entry(master)
        self.e1.grid(row=0, column=1)
        self.e1.pack()
        #e2 = tk.Entry(master)

       
#        e2.grid(row=1, column=1)

        
    def greet(self):
        print("Greetings!")

root = tk.Tk()
my_gui = MyFirstGUI(root)
root.mainloop()



