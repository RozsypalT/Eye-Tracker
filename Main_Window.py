from tkinter import *
from tkinter.filedialog import askopenfilename


class Main_Window():

    def start(self):

        root = Tk()
        MainFrame = Frame(root, width=750, height=500)

        MainFrame.grid_propagate(0)
        MainFrame.grid()

        rows = 0
        while rows < 10:
            MainFrame.rowconfigure(rows, weight = 1)
            MainFrame.columnconfigure(rows, weight=1)
            rows +=1

        MainFrame.master.title('Image Chooser')

        bAddP = Button(MainFrame, text="Add Picture", fg='white', bg='black', command=openFile)
        bAddP.grid(row=1, column=0)

        bStart = Button(MainFrame, text="Start", fg='white', bg='black')
        bStart.config(height = 1, width=5)
        bStart.grid(row=8, column=2)

        bQuit = Button(MainFrame, text="Konec", fg='white', bg='black', command=MainFrame.quit)
        bQuit.grid(row=8, column=4)

        list = Listbox(MainFrame, width=80, height=20)
        list.grid(row=3, column=0, columnspan=9)

        label = Label(MainFrame, text='Loaded pictures: ')
        label.grid(row=2, column=0)

        root.mainloop()

        quit()


def openFile():
     name = askopenfilename(initialdir="C:/Users/", filetypes=(("Image File", "*.png"), ("Image File", "*.jpg")), title="Choose a file")





wi = Main_Window
wi.start(wi)