from tkinter import Tk, Label

root = Tk()

# First label
label1 = Label(root, text="Label 1", bg="lightblue")
label1.pack(side="left", padx=10, pady=10)

# Second label
label2 = Label(root, text="Label 2", bg="lightgreen")
label2.pack(side="right", padx=10, pady=10)

root.mainloop()

def prints():
    print("rushikesh")
