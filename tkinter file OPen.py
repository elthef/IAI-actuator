from tkinter import filedialog
from tkinter import *
import csv

data = []
root = Tk()
filename =  filedialog.asksaveasfilename(defaultextension="",initialdir = "./",title = "Select file",
                                         filetypes = [
                                             ("text files","*.txt"),
                                             ("csv","*.csv")
                                             ],
                                         )
data =  [[],[]]
data[0].append(4)
data[0].append(8)
data[1].append(18)
data[1].append(1)
data[1].append(51)
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)
    # writer.writerow(["SN", "Name", "Contribution"])
    # writer.writerow([1, "Linus Torvalds", "Linux Kernel"])
    # writer.writerow([2, "Tim Berners-Lee", "World Wide Web"])
    # writer.writerow([3, "Guido van Rossum", "Python Programming"])
