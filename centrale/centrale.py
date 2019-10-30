from tkinter import Tk, Label, Button

class Centrale:
    def __init__(self, master):
        self.master = master

        master.title("Centrale")

        self.label = Label(master, text='Test')
        self.label.pack()

if __name__ == '__main__':
    root = Tk()
    
    centrale = Centrale(root)

    root.mainloop()