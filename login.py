import mysql.connector
from tkinter import *
from tkinter import messagebox
from subprocess import call
import sys 
from PIL import ImageTk, Image


def Ok():
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="asddatabase")
    mycursor = mysqldb.cursor()
    uname = e1.get()
    password = e2.get()
 
    sql = "select permissions from user where username = %s and password = %s"
    mycursor.execute(sql, [(uname), (password)])
    results = mycursor.fetchall()
    if results:
        res = int(''.join(map(str, results[0])))
        if  res == 1:
            root.destroy()
            call(["python", "table.py"])
        elif res == 2:
            root.destroy()
            call(["python", "mananger.py"])
        elif res == 3:
            root.destroy()
            call(["python", "warden.py"])
            
    else :
        messagebox.showinfo("","Incorrent Username and Password")
        return False
 
 
 
root = Tk()
root.title("Student Housing System")
bg = Image.open('background.png')
bg.thumbnail((950, 600))
root.resizable(0,0)
width,height = bg.size
bg = ImageTk.PhotoImage(bg)
global e1
global e2
canvas = Canvas(root, width=width, height=height, bd=0, highlightthickness=0)
canvas.pack(fill=BOTH, expand=True)
canvas.create_image(0, 0, image=bg, anchor='nw')
Label(root, text="Student Housing System",font=("Arial", 23, "bold"), bg="#a1060f").place(x=50,y=0,width=841,height=81)
Label(root, text="UserName", bg="#a1060f").place(x=250,y=160,width=70,height=25)
Label(root, text="Password", bg="#a1060f").place(x=250,y=220,width=70,height=25)
 
e1 = Entry(root)
e1.place(x=345,y=150,width=268,height=38)
 
e2 = Entry(root)
e2.place(x=345,y=219,width=268,height=38)
e2.config(show="*")
 
Button(root, text="Login", command=Ok ,height = 2, width = 13).place(x=400,y=310,width=157,height=41)
root.mainloop()
