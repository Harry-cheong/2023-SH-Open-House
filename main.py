from tkinter import ttk
from tkinter import Tk
from functools import partial

# initialise screen
root = Tk()
style = ttk.Style()
style.theme_use('alt')

# fullscreen setup
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
root.geometry("%dx%d" % (w, h))
root.state("zoomed")
root.title("Robot GUI")

# configure grids
num_columns = 2 # left and right
num_rows = 18 # must be evenly divisible by number of buttons (curr. 3)
root.columnconfigure(tuple(range(num_columns)), weight=1)
root.rowconfigure(tuple(range(num_rows)), weight=1)

def from_rgb(rgb):
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'


# define code blocks
buttons = ['fwd', 'left', 'right']
button_key = {
    'fwd': "Move forward",
    'right': "Turn right",
    'left': "Turn left"
}
color_key = {
    "fwd": (0, 50, 50),
    "right": (50, 0, 0),
    "left": (0, 0, 50)
}

# configure all styles
# button
style.configure('insert.TButton', font=('Helvetica', 14), foreground='white', borderwidth=0)
for button in buttons:
    style.configure(f'{button}.insert.TButton', background=from_rgb(color_key[button]))
    style.map(f'{button}.insert.TButton', background=[('pressed', from_rgb([i+50 for i in color_key[button]])), ('hover', from_rgb([i+25 for i in color_key[button]]))])
style.configure('display.TButton', font=('Helvetica', 14), foreground='white', borderwidth=0)
for button in buttons:
    style.configure(f'{button}.display.TButton', background=from_rgb(color_key[button]))
    style.map(f'{button}.display.TButton', background=[('hover', from_rgb(color_key[button]))])
style.configure('start.display.TButton', background=from_rgb((50, 50, 50)))
style.map('start.display.TButton', background=[('hover', from_rgb((50, 50, 50)))])
style.configure('empty.display.TButton', font=('Helvetica', 14), background='#ddf', foreground='#edd', borderwidth=0)
style.map('empty.display.TButton', background=[('hover', '#ddf')])

# left background
style.configure('background.TLabel', font=("Helvetica", 14), background="#ddf", foreground="black", borderwidth=0, anchor="center")
style.map('background.TLabel', background=[('hover', '#ddf')])
style.configure('codeheader.TLabel', font=("Helvetica", 14, 'underline'), background="#ddf", foreground="black", borderwidth=0, anchor="center")
style.map('codeheader.TLabel', background=[('hover', '#ddf')])

# place buttons for inserting code blocks
seq = []
codeblocks = {}
def add_to_seq(cmd):
    seq.append(cmd)
    print(seq)

    codeblocks[len(seq)+3].destroy()
    btn = ttk.Button(root, text=button_key[cmd], style=f"{cmd}.display.TButton")
    codeblocks[len(seq)+3] = btn
    btn.grid(row=len(seq)+3, column=0, sticky="NSEW", padx=50, pady=0)

for count, button in enumerate(buttons):
    ttk.Button(root, text=button_key[button], style=f"{button}.insert.TButton", command=partial(add_to_seq, button)).grid(row=num_rows//len(buttons)*count, column=1, rowspan=num_rows//len(buttons), sticky="NSEW", padx=50, pady=50)

# display code sequence section
background = ttk.Label(root, style="background.TLabel")
background.grid(row=0, column=0, rowspan=num_rows, sticky="NSEW", padx=0, pady=0)
text = ttk.Label(root, text="Code", style="codeheader.TLabel")
text.grid(row=1, column=0, sticky="NEW", padx=50, pady=0)

btn_start = ttk.Button(root, text='Start', style="start.display.TButton")
btn_start.grid(row=3, column=0, sticky="NSEW", padx=50, pady=0)
for i in range(4, num_rows-1):
    btn = ttk.Button(root, text="", style="empty.display.TButton", state="disabled")
    codeblocks[i] = btn
    btn.grid(row=i, column=0, sticky="NSEW", padx=50, pady=0)

# end execution and display - listen for events (if any)
root.mainloop()

# TODO: add various styles for the different movement types
# TODO: link buttons to actual functionality
# TODO: grid placement - tkinter function
# TODO: link output