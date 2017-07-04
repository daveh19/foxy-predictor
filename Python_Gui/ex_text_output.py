import tkinter as tk

def cbc(id, tex):
    return lambda : callback(id, tex)

def callback(id, tex):
    s = 'At {} f is {}\n'.format(id, 2)
    tex.insert(tk.END, s)
    tex.see(tk.END)             # Scroll if necessary
    
def deleteStuff(tex): 
    tex.delete(1.0, tk.END)
    
def kill(tex): 
    return lambda: deleteStuff(tex) 
    

top = tk.Tk()
tex = tk.Text(master=top) # text part 
tex.pack(side=tk.RIGHT)
bop = tk.Frame() #button part 
bop.pack(side=tk.LEFT)
for k in range(1,10):
    tv = 'Say {}'.format(k)
    b = tk.Button(bop, text=tv, command=cbc(k, tex))
    b.pack()

tk.Button(bop, text='Exit', command=top.destroy).pack()
tk.Button(bop, text = 'Clear', command = kill(tex)).pack()
top.mainloop()


 
