from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from subprocess import call
from PIL import ImageTk, Image

window = Tk()
window.title('Acommodation system')
window.resizable(0,0)
window['background'] = '#a1060f'
bg = Image.open('LargeFooter.png')
bg.thumbnail((1040, 600))
width,height = bg.size
bg = ImageTk.PhotoImage(bg)


mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="asddatabase")
mycursor = mysqldb.cursor()

def logout():
    window.destroy()
    call(["python", "login.py"])

logoutFrame = Frame(window,width = 100, bg = '#a1060f')
logoutFrame.pack(expand=False, anchor=E)
refresh_button = Button(logoutFrame,text="Logout", command=logout)
refresh_button.pack(side=RIGHT)
def search():
    query = search_entry.get()
    if str(query) == "":
        messagebox.showwarning(
        title='No record', message='Please input valid search')
    else:
        selections = []
        for child in table.get_children():
            # compare strings in  lower cases.

            if str(query.lower()) in str(table.item(child)['values']).lower():
                selections.append(child)

        table.selection_set(selections)



search_frame = Frame(window, width=200,bg = '#a1060f')
search_frame.pack(expand=False, anchor=CENTER)
search_entry = Entry(search_frame)
search_button = Button(search_frame, text="Search", command=search)
search_entry.pack(side=RIGHT, padx=20)
search_button.pack(side=RIGHT)

table_frame = Frame(window)
table_frame.pack()

# scrollbar
table_scroll = Scrollbar(table_frame, orient='vertical')
table_scroll.pack(side=RIGHT, fill=Y)

table = ttk.Treeview(
    table_frame, yscrollcommand=table_scroll.set, xscrollcommand=table_scroll.set)


table.pack()

table_scroll.config(command=table.yview)
table_scroll.config(command=table.xview)

table['columns'] = ('Lease_Number', 'Hall_Name', 'Hall_Number',
                    'Room_Number', 'Student_Name', 'Occupancy_Status', 'Cleaning_Status','Rent_Rate')

# format our column
table.column("#0", width=0,  stretch=NO)
table.column("Lease_Number", anchor=CENTER, width=120, )
table.column("Hall_Name", anchor=CENTER, width=120)
table.column("Hall_Number", anchor=CENTER, width=120)
table.column("Room_Number", anchor=CENTER, width=120)
table.column("Student_Name", anchor=CENTER, width=140, stretch=YES)
table.column("Occupancy_Status", anchor=CENTER, width=120)
table.column("Cleaning_Status", anchor=CENTER, width=120)
table.column("Rent_Rate", anchor=CENTER, width = 120)

# Create Headings
table.heading("#0", text="", anchor=CENTER)
table.heading("Lease_Number", text="Lease Number", anchor=CENTER)
table.heading("Hall_Name", text="Hall Name", anchor=CENTER)
table.heading("Hall_Number", text="Hall Number", anchor=CENTER)
table.heading("Room_Number", text="Room Number", anchor=CENTER)
table.heading("Student_Name", text="Student Name", anchor=CENTER)
table.heading("Occupancy_Status", text="Occupancy Status", anchor=CENTER)
table.heading("Cleaning_Status", text="Cleaning Status", anchor=CENTER)
table.heading("Rent_Rate", text = "Rent Rate", anchor= CENTER)


def getdetails(roomnumber):
    a1 = []
    a1.append(roomnumber)
    sql = """select leasenumber from lease where roomid = %s;"""
    mycursor.execute(sql,(roomnumber,))
    results = mycursor.fetchall()
    if len(results) == 0:
        a1.append("N/A")
    else: 
        res = int(''.join(map(str, results[0])))
        a1.append(res)
        results.clear
    sql = """select hallid from room where roomid = %s;"""
    mycursor.execute(sql,(roomnumber,))
    results = mycursor.fetchall()
    res = int(''.join(map(str, results[0])))
    a1.append(res) 
    results.clear

    sql = """select hallname from hall where hallid = %s"""
    hallid = a1[2]
    mycursor.execute(sql, (hallid,))
    results = mycursor.fetchall()
    a1.append(results[0])
    results.clear

    sql = "select occupancy from room where roomid = %s"
    mycursor.execute(sql, [(a1[0])])
    results = mycursor.fetchall()
    a1.append(results[0]) 
    results.clear

    sql = "select cleaning from room where roomid = %s"
    mycursor.execute(sql, [(a1[0])])
    results = mycursor.fetchall()
    a1.append(results[0]) 
    results.clear

    if a1[1] == "N/A":
        a1.append("N/A")
        a1.append("N/A")
    else:
        sql = "select name from student where leasenumber = %s"
        mycursor.execute(sql, [(a1[1])])
        results = mycursor.fetchall()
        a1.append(results[0]) 
        results.clear
        sql = "select RentRate from lease where leasenumber = %s"
        mycursor.execute(sql, [(a1[1])])
        results = mycursor.fetchall()
        a1.append(results[0]) 
        results.clear
        
    return a1

sql = mycursor.execute("select roomid from room")
results = mycursor.fetchall()
test = [i[0] for i in results]
x = 0

for i in range (len(test)):
    sql = getdetails(test[i]) 
    table.insert(parent='', index='end', iid=x, text='',
                 values=(sql[1], sql[3], sql[2], sql[0], sql[6], sql[4], sql[5],sql[7]))
    x+= 1



table.pack()
frame = Frame(window)
frame.pack(pady=20)

# labels
LeaseNumber = Label(frame, text="Lease Number")
LeaseNumber.grid(row=0, column=1)

HallName = Label(frame, text="Hall Name")
HallName.grid(row=0, column=0)

HallNumber = Label(frame, text="Hall Number")
HallNumber.grid(row=0, column=2)

RoomNumber = Label(frame, text="Room Number")
RoomNumber.grid(row=0, column=3)

StudentName = Label(frame, text="Student Name")
StudentName.grid(row=0, column=4)

OccupancyStatus = Label(frame, text="Occupancy Status")
OccupancyStatus.grid(row=0, column=5)

CleaningStatus = Label(frame, text="Cleaning Status")
CleaningStatus.grid(row=0, column=6)

RentRate = Label(frame, text = "Rent Rate")
RentRate.grid(row = 0, column = 7)
# Entry boxes
LeaseNumber_entry = Entry(frame)
LeaseNumber_entry.configure(state="disabled")
LeaseNumber_entry.grid(row=1, column=1)

HallName_entry = Entry(frame)
HallName_entry.configure(state="disabled")
HallName_entry.grid(row=1, column=0)

HallNumber_entry = Entry(frame)
HallNumber_entry.grid(row=1, column=2)

RoomNumber_entry = Entry(frame)
RoomNumber_entry.grid(row=1, column=3)

StudentName_entry = Entry(frame)
StudentName_entry.grid(row=1, column=4)

RentRate_entry = Entry(frame)
RentRate_entry.grid(row = 1, column = 7)

OccupancyStatus_entry = ttk.Combobox(
    frame, values=['Occupied', 'Unoccupied'])  
OccupancyStatus_entry.grid(row=1, column=5)

CleaningStatus_entry = ttk.Combobox(
    frame, values=['Clean', 'Dirty', 'offline'],
     background="gray74",)
CleaningStatus_entry.configure(state='disabled')
CleaningStatus_entry.grid(row=1, column=6)

# Select Record
def select_record():
    # clear entry boxes

    LeaseNumber_entry.configure(state="normal")
    LeaseNumber_entry.delete(0, END)
    LeaseNumber_entry.configure(state="disabled")
    HallName_entry.configure(state="normal")
    HallName_entry.delete(0, END)
    HallName_entry.configure(state="disabled")
    HallNumber_entry.delete(0, END)
    RoomNumber_entry.delete(0, END) 
    StudentName_entry.delete(0, END)
    OccupancyStatus_entry.configure(state = "normal")
    OccupancyStatus_entry.delete(0, END)
    RentRate_entry.delete(0,END)
    CleaningStatus_entry.configure(state='normal') 
    CleaningStatus_entry.delete(0,END)
    CleaningStatus_entry.configure(state='disabled')
    
    global TempLeaseNum 
    global TempHallId
    global TempRoomID

    # grab record
    selected = table.focus()
    # grab record values
    values = table.item(selected, 'values')

    # output to entry boxes
    OccupancyStatus_entry.configure(state = "normal")
    OccupancyStatus_entry.insert(0, values[5])
    OccupancyStatus_entry.configure(state = "readonly")
    LeaseNumber_entry.configure(state="normal")
    LeaseNumber_entry.insert(0, values[0])
    LeaseNumber_entry.configure(state="disabled")
    HallName_entry.configure(state="normal")
    HallName_entry.insert(0, values[1])
    HallName_entry.configure(state="disabled")
    HallNumber_entry.insert(0, values[2])
    RoomNumber_entry.insert(0, values[3])
    StudentName_entry.insert(0, values[4])

    CleaningStatus_entry.configure(state='normal') 
    CleaningStatus_entry.insert(0, values[6])
    CleaningStatus_entry.configure(state='disabled')
    RentRate_entry.insert(0,values[7])
    TempHallId = HallNumber_entry.get()
    TempLeaseNum = LeaseNumber_entry.get()
    TempRoomID = RoomNumber_entry.get()
# save Record
def update_record():
    selected = table.focus()
    # save new data
    if LeaseNumber_entry.get() and HallName_entry.get() and HallNumber_entry.get() and RoomNumber_entry.get() and StudentName_entry.get() and OccupancyStatus_entry.get() and CleaningStatus_entry.get() and RentRate_entry.get():
        table.item(selected, text="", values=(LeaseNumber_entry.get(),
                                              HallName_entry.get(), HallNumber_entry.get(),
                                              RoomNumber_entry.get(), StudentName_entry.get(),
                                              OccupancyStatus_entry.get(), CleaningStatus_entry.get(),RentRate_entry.get()))
        LNum = LeaseNumber_entry.get()
        Hname = HallName_entry.get()
        HNumber = HallNumber_entry.get()
        RNumber = RoomNumber_entry.get()
        SName = StudentName_entry.get()
        SName = SName.strip("\{}")
        OStatus = OccupancyStatus_entry.get()
        Cstatus = CleaningStatus_entry.get()
        Rrate = RentRate_entry.get()
        Rrate = Rrate.strip("£")
        z = True
        try: 
            Rrate = int(Rrate)
        except:
            messagebox.showwarning(
            title='No record', message='Please only enter an integer under rent rate')
            for row in table.get_children():
                    table.delete(row)
            sql = mycursor.execute("select roomid from room")
            results = mycursor.fetchall()
            test = [i[0] for i in results]
            x = 0
    
            for i in range (len(test)):
                sql = getdetails(test[i]) 
                table.insert(parent='', index='end', iid=x, text='',
                            values=(sql[1], sql[3], sql[2], sql[0], sql[6], sql[4], sql[5],sql[7]))
                x+= 1
            z = False
        if z == True:
            z = isinstance(Rrate,int)
            print(z)
            print(Rrate)
            y = SName
            y.replace(' ','').isalpha()
            if all(x.isalpha() or x.isspace() for x in y) and z == True:
                z = str(Rrate)
                TempRrate = '£' + z
                if TempLeaseNum == "N/A":
                    sql = mycursor.execute("select leasenumber from lease")
                    results = mycursor.fetchall()
                    test = [i[0] for i in results]
                    x = len(test) - 1
                    LNum = test[x] + 1
                    sql = "insert into lease (leasenumber, roomid, hallid, RentRate) values (%s,%s,%s,%s)"
                    mycursor.execute(sql,(LNum,RNumber,HNumber,TempRrate,))
                    mysqldb.commit()
                    sql = "insert into student (name,leasenumber) values (%s,%s)"
                    mycursor.execute(sql,(SName,LNum,))
                    mysqldb.commit()
                    LeaseNumber_entry.delete(0, END)
                    HallName_entry.delete(0, END)
                    HallNumber_entry.delete(0, END)
                    RoomNumber_entry.delete(0, END)
                    StudentName_entry.delete(0, END)
                    OccupancyStatus_entry.delete(0, END)
                    CleaningStatus_entry.delete(0, END)
                    RentRate_entry.delete(0,END)
                    messagebox.showinfo(title='Update Record', message='Record updated.')
                    table.selection_set()
                    selected = None

                else: 
                    sql = "update lease set leasenumber = %s where roomid = %s"
                    mycursor.execute(sql,(LNum,TempRoomID,))
                    mysqldb.commit()

                    sql = "update hall set hallid = %s, hallname = %s where hallid = %s"
                    mycursor.execute(sql,(HNumber,Hname,TempHallId,))
                    mysqldb.commit()

                    sql = "update room set roomid = %s, occupancy = %s, cleaning = %s where roomid = %s"
                    mycursor.execute(sql,(RNumber,OStatus,Cstatus,TempRoomID,))
                    mysqldb.commit()

                    sql = "update student set name = %s where leasenumber = %s"
                    mycursor.execute(sql,(SName,TempLeaseNum))

                    sql = "update lease set RentRate = %s where leasenumber =%s"
                    mycursor.execute(sql,(TempRrate,TempLeaseNum))
                
                    mysqldb.commit()
            # clear entry boxes
                    LeaseNumber_entry.delete(0, END)
                    HallName_entry.delete(0, END)
                    HallNumber_entry.delete(0, END)
                    RoomNumber_entry.delete(0, END)
                    StudentName_entry.delete(0, END)
                    OccupancyStatus_entry.delete(0, END)
                    CleaningStatus_entry.delete(0, END)
                    RentRate_entry.delete(0,END)
                    messagebox.showinfo(title='Update Record', message='Record updated.')
                    table.selection_set()
                    selected = None
                for row in table.get_children():
                    table.delete(row)
                sql = mycursor.execute("select roomid from room")
                results = mycursor.fetchall()
                test = [i[0] for i in results]
                x = 0
        
                for i in range (len(test)):
                    sql = getdetails(test[i]) 
                    table.insert(parent='', index='end', iid=x, text='',
                                values=(sql[1], sql[3], sql[2], sql[0], sql[6], sql[4], sql[5],sql[7]))
                    x+= 1
            else:
                
                messagebox.showwarning(
                title='No record', message='Please only input a string for Student Name')
                for row in table.get_children():
                    table.delete(row)
                sql = mycursor.execute("select roomid from room")
                results = mycursor.fetchall()
                test = [i[0] for i in results]
                x = 0
        
                for i in range (len(test)):
                    sql = getdetails(test[i]) 
                    table.insert(parent='', index='end', iid=x, text='',
                                values=(sql[1], sql[3], sql[2], sql[0], sql[6], sql[4], sql[5],sql[7]))
                    x+= 1
    else:
        messagebox.showwarning(
            title='No record', message='Please choose a record to update')
            
def delete_record():
    selected = table.focus()
    if LeaseNumber_entry.get() and HallName_entry.get() and HallNumber_entry.get() and RoomNumber_entry.get() and StudentName_entry.get() and OccupancyStatus_entry.get() and CleaningStatus_entry.get() and RentRate_entry.get():
        table.item(selected, text="", values=(LeaseNumber_entry.get(),
                                            HallName_entry.get(), HallNumber_entry.get(),
                                            RoomNumber_entry.get(), StudentName_entry.get(),
                                            OccupancyStatus_entry.get(), RentRate_entry.get()))
        
    

        res = messagebox.askokcancel(title='Delete Confirmation',
                                    message='Are you sure you want to delete that record?')

        if res:
            Lnum = LeaseNumber_entry.get()
            RNum = RoomNumber_entry.get()
            table.delete(selected)

            sql = "delete from lease where leasenumber = %s"
            mycursor.execute(sql,(Lnum,))
            mysqldb.commit()
            sql = "update room set occupancy = 'Unoccupied', cleaning = 'Offline' where roomid = %s"
            mycursor.execute(sql,(RNum,))
            mysqldb.commit()

            for row in table.get_children():
                table.delete(row)
            sql = mycursor.execute("select roomid from room")
            results = mycursor.fetchall()
            test = [i[0] for i in results]
            x = 0
            for i in range (len(test)):
                sql = getdetails(test[i]) 
                table.insert(parent='', index='end', iid=x, text='',
                            values=(sql[1], sql[3], sql[2], sql[0], sql[6], sql[4], sql[5],sql[7]))
                x+= 1
    else:
        messagebox.showwarning(
        title='No record', message='Please choose a record to delete')

# Buttons
buttons_frame = Frame(window)
buttons_frame.pack(anchor=CENTER)
select_button = Button(
    buttons_frame, text="Select Record", command=select_record)
select_button.pack( side=RIGHT)

refresh_button = Button(
    buttons_frame, text="Update Record", command=update_record)
refresh_button.pack(side=RIGHT)

delete_button = Button(
    buttons_frame, text="Delete Record", command=delete_record)
delete_button.pack(side=RIGHT)

canvas = Canvas(window, width=width, height=height, bd=0, highlightthickness=0)
canvas.pack(fill=BOTH, expand=True)
canvas.create_image(0, 0, image=bg, anchor='nw')

window.mainloop()
