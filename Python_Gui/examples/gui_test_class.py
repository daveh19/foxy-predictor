from tkinter import *

class App:
  def __init__(self, master):
    frame = Frame(master)
    frame.pack()
    self.button = Button(frame, 
                         text="QUIT", fg="red",
                         command=quit)
    self.button.pack(side=LEFT)
    self.slogan = Button(frame,
                         text="Hello",
                         command=self.write_slogan)
    self.slogan.pack(side=LEFT)
    
    self.field = Canvas(frame, width=200, height=100)
    self.field.create_rectangle(50, 20, 150, 80, fill="#476042")
    self.field.create_rectangle(65, 35, 135, 65, fill="yellow")

    self.field.pack()
    
    self.variable = StringVar(frame)
    self.variable.set("one") # default value

#    self.options = OptionMenu(frame , self.variable, "one", "two", "three")
#    self.options.pack()

    self.options = OptionMenu(frame,  self.variable, "one", "two", "three")
    self.options.pack()
    
    
    self.choice = Label(frame, text="Your choice:")
    self.var1 = IntVar()
    self.check1 = Checkbutton(frame, text="YES", variable=self.var1)#.grid(row=0, sticky=W)
    self.check1.pack()
    self.var2 = IntVar()
    self.check2 = Checkbutton(frame, text="NO", variable=self.var2)#.grid(row=1, sticky=W)
    self.check2.pack()
    self.show = Button(frame, text='Show', command=self.var_states)#.grid(row=4, sticky=W, pady=4)
    self.show.pack()
    
  def write_slogan(self):
    #print("Tkinter is easy to use!")
    self.field.create_text(95, 50, text="Python")
    self.field.pack()
    
  def var_states(self):
    print("yes: %d,\n no: %d" % (self.var1.get(), self.var2.get()))
    
    
    

root = Tk()
app = App(root)

#w = Canvas(root)
#w.pack()


#w.create_line(0, 0, 50, 20, fill="#476042", width=3)
#w.create_line(0, 100, 50, 80, fill="#476042", width=3)
#w.create_line(150,20, 200, 0, fill="#476042", width=3)
#w.create_line(150, 80, 200, 100, fill="#476042", width=3)









root.mainloop()

