from tkinter import ttk
from tkinter import Tk

# initialise screen
root = Tk()

# fullscreen setup
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
root.geometry("%dx%d" % (w, h))
root.state("zoomed")
root.title("Robot GUI")

# style a sample button
style = ttk.Style()
button_1 = ttk.Button(root, text='Sample Button 1')
style.theme_use('alt')
style.configure('TButton', font=('Helvetica', 14), background='#000', foreground='white', borderwidth=0, bordercolor="purple", lightcolor="blue", darkcolor="red")
style.map('TButton', background=[('pressed', '#444'), ('hover', '#222')])
button_1.pack()

# end execution and display - listen for events (if any)
root.mainloop()

# TODO: add various styles for the different movement types
# TODO: link buttons to actual functionality
# TODO: grid placement - tkinter function
# TODO: link output