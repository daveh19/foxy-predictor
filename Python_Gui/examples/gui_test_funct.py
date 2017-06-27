import tkinter as tk 

master = tk.Tk()

def var_states():
   print("male: %d,\nfemale: %d" % (var1.get(), var2.get()))

#select data: 
tk.Label(master, text="data 2 use:").grid(row=0)
var1 = tk.IntVar()
tk.Checkbutton(master, text="data1", variable=var1).grid(column = 0, row=1, sticky = tk.W)
var2 = tk.IntVar()
tk.Checkbutton(master, text="data2", variable=var2).grid(column = 0, row=2, sticky = tk.W)
var3 = tk.IntVar()
tk.Checkbutton(master, text="data3", variable=var3).grid(column = 0, row=3, sticky = tk.W)
var4 = tk.IntVar()
tk.Checkbutton(master, text="data4", variable=var4).grid(column = 0, row=4, sticky = tk.W)
var5 = tk.IntVar()
tk.Checkbutton(master, text="data5", variable=var5).grid(column = 0, row=5, sticky = tk.W)




tk.Button(master, text='Quit', command=master.quit).grid(column = 2, row=1)
tk.Button(master, text='Show', command=var_states).grid(column = 2, row=2)

tk.mainloop()



