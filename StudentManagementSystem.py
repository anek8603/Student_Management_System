import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
import pymysql

# Main Window
win = tk.Tk()
win.geometry("1350x700+0+0")
win.title("Student Management System")

# Title Label
title_label = tk.Label(
    win,
    text="Student Management System",
    font=("Times New Roman", 30, "bold"),
    bd=12,
    relief=tk.GROOVE
)
title_label.pack(side=tk.TOP, fill=tk.X)

# Detail Frame
detail_frame = tk.LabelFrame(
    win,
    text="Enter Details",
    font=("Arial", 20, "bold"),
    bd=12,
    relief=tk.GROOVE,
    bg="lightgrey",
    labelanchor='n'
)
detail_frame.place(x=20, y=90, width=420, height=575)

# Data Frame
data_frame = tk.Frame(win, bd=12, bg="lightgray", relief=tk.GROOVE)
data_frame.place(x=455, y=90, width=1040, height=575)

# Variables
roll_no = tk.StringVar()
name = tk.StringVar()
course = tk.StringVar()
dob = tk.StringVar()
gender = tk.StringVar()
contact = tk.StringVar()
email = tk.StringVar()
address = tk.StringVar()
search_by = tk.StringVar()

# Student Detail Fields
tk.Label(detail_frame, text="Roll No.", font=('Arial', 15), bg="lightgrey").grid(row=0, column=0, sticky="w")
tk.Entry(detail_frame, bd=7, font=('Arial', 15), textvariable=roll_no).grid(row=0, column=1)

tk.Label(detail_frame, text="Name", font=('Arial', 15), bg="lightgrey").grid(row=1, column=0, sticky="w")
tk.Entry(detail_frame, bd=7, font=('Arial', 15), textvariable=name).grid(row=1, column=1)

tk.Label(detail_frame, text="Course", font=('Arial', 15), bg="lightgrey").grid(row=2, column=0, sticky="w")
tk.Entry(detail_frame, bd=7, font=('Arial', 15), textvariable=course).grid(row=2, column=1)

tk.Label(detail_frame, text="D.O.B", font=('Arial', 16), bg="lightgrey").grid(row=3, column=0, sticky="w")
dob_ent = DateEntry(detail_frame, font=('Arial', 16), width=18, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
dob_ent.grid(row=3, column=1)

tk.Label(detail_frame, text="Gender", font=('Arial', 14), bg="lightgrey").grid(row=4, column=0, sticky="w")
gender_ent = ttk.Combobox(detail_frame, font=('Arial', 14), state='readonly', values=["Male", "Female", "Others"], textvariable=gender)
gender_ent.current(0)
gender_ent.grid(row=4, column=1)

tk.Label(detail_frame, text="Contact", font=('Arial', 15), bg="lightgrey").grid(row=5, column=0, sticky="w")
tk.Entry(detail_frame, bd=7, font=('Arial', 15), textvariable=contact).grid(row=5, column=1)

tk.Label(detail_frame, text="Email Id", font=('Arial', 15), bg="lightgrey").grid(row=6, column=0, sticky="w")
tk.Entry(detail_frame, bd=7, font=('Arial', 15), textvariable=email).grid(row=6, column=1)

tk.Label(detail_frame, text="Address", font=('Arial', 15), bg="lightgrey").grid(row=7, column=0, sticky="w")
tk.Entry(detail_frame, bd=7, font=('Arial', 15), textvariable=address).grid(row=7, column=1)

# Functions
def fetch_data():
    conn = pymysql.connect(host="localhost", user="root", password="", database="sms1")
    curr = conn.cursor()
    curr.execute("SELECT * FROM data")
    rows = curr.fetchall()
    if rows:
        student_table.delete(*student_table.get_children())
        for row in rows:
            student_table.insert('', tk.END, values=row)
    conn.close()

def add_func():
    if roll_no.get() == '' or name.get() == '' or course.get() == '':
        messagebox.showerror("Error!", "Please fill all the fields!")
    else:
        conn = pymysql.connect(host="localhost", user="root", password="", database="sms1")
        curr = conn.cursor()
        curr.execute("INSERT INTO data VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                     (roll_no.get(), name.get(), course.get(), dob_ent.get(), gender.get(), contact.get(), email.get(), address.get()))
        conn.commit()
        conn.close()
        fetch_data()
        messagebox.showinfo("Success", "Record added successfully!")

def get_cursor(event):
    cursor_row = student_table.focus()
    content = student_table.item(cursor_row)
    row = content['values']
    if row:
        roll_no.set(row[0])
        name.set(row[1])
        course.set(row[2])
        dob_ent.set_date(row[3])
        gender.set(row[4])
        contact.set(row[5])
        email.set(row[6])
        address.set(row[7])

def clear():
    roll_no.set("")
    name.set("")
    course.set("")
    dob_ent.set_date("01/01/2000")  # Or use any default valid date
    gender.set("Male")  # Reset to default selected gender
    contact.set("")
    email.set("")
    address.set("")

def update_func():
    conn = pymysql.connect(host="localhost", user="root", password="", database="sms1")
    curr = conn.cursor()
    curr.execute("UPDATE data SET name=%s, course=%s, dob=%s, gender=%s, contact=%s, email=%s, address=%s WHERE rollno=%s",
                 (name.get(), course.get(), dob_ent.get(), gender.get(), contact.get(), email.get(), address.get(), roll_no.get()))
    conn.commit()
    conn.close()
    fetch_data()
    clear()
    messagebox.showinfo("Updated", "Record updated successfully!")

def delete_func():
    if roll_no.get() == "":
        messagebox.showerror("Error", "Please select a record to delete!")
        return
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
    if confirm:
        conn = pymysql.connect(host="localhost", user="root", password="", database="sms1")
        curr = conn.cursor()
        curr.execute("DELETE FROM data WHERE rollno=%s", (roll_no.get(),))
        conn.commit()
        conn.close()
        fetch_data()
        clear()
        messagebox.showinfo("Deleted", "Record deleted successfully!")

def search_func():
    if search_by.get() == "":
        messagebox.showerror("Error", "Please select a search category!")
        return

    search_column_map = {
        "Roll No.": "rollno",
        "Name": "name",
        "Course": "course",
        "D.O.B": "dob",
        "Contact": "contact"
    }

    search_col = search_column_map.get(search_by.get())
    search_term = simpledialog.askstring("Search", f"Enter {search_by.get()} to search:")

    if search_term:
        conn = pymysql.connect(host="localhost", user="root", password="", database="sms1")
        curr = conn.cursor()
        query = f"SELECT * FROM data WHERE {search_col} LIKE %s"
        curr.execute(query, (f"%{search_term}%",))
        rows = curr.fetchall()
        student_table.delete(*student_table.get_children())
        for row in rows:
            student_table.insert('', tk.END, values=row)
        conn.close()

# Buttons
btn_frame = tk.Frame(detail_frame, bg="lightgrey", bd=10, relief=tk.GROOVE)
btn_frame.place(x=18, y=390, width=342, height=120)

tk.Button(btn_frame, bg="lightgrey", text="Add", bd=7, font=("Arial", 13), width=15, command=add_func).grid(row=0, column=0)
tk.Button(btn_frame, bg="lightgrey", text="Update", bd=7, font=("Arial", 13), width=15, command=update_func).grid(row=0, column=1)
tk.Button(btn_frame, bg="lightgrey", text="Delete", bd=7, font=("Arial", 13), width=15, command=delete_func).grid(row=1, column=0)
tk.Button(btn_frame, bg="lightgrey", text="Clear", bd=7, font=("Arial", 13), width=15, command=clear).grid(row=1, column=1)

# Search Frame
search_frame = tk.Frame(data_frame, bg="lightgrey", bd=10, relief=tk.GROOVE)
search_frame.pack(side=tk.TOP, fill=tk.X)

tk.Label(search_frame, text="Search", bg="lightgrey", font=("Arial", 14)).grid(row=0, column=0)
search_in = ttk.Combobox(search_frame, font=("Arial", 14), state="readonly", textvariable=search_by)
search_in['values'] = ("Roll No.", "Name", "Course", "D.O.B", "Contact")
search_in.grid(row=0, column=1)

tk.Button(search_frame, text="Search", font=("Arial", 13), bd=9, width=14, bg="lightgrey", command=search_func).grid(row=0, column=2)
tk.Button(search_frame, text="Show All", font=("Arial", 13), bd=9, width=14, bg="lightgrey", command=fetch_data).grid(row=0, column=3)

# Table Frame
main_frame = tk.Frame(data_frame, bg="lightgray", bd=11, relief=tk.GROOVE)
main_frame.pack(fill=tk.BOTH, expand=True)

y_scroll = tk.Scrollbar(main_frame, orient=tk.VERTICAL)
x_scroll = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL)

student_table = ttk.Treeview(main_frame, columns=("Roll No.", "Name", "Course", "D.O.B", "Gender", "Contact", "Email id", "Address"),
                             yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

y_scroll.config(command=student_table.yview)
x_scroll.config(command=student_table.xview)

y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
student_table.pack(fill=tk.BOTH, expand=1)

student_table.heading("Roll No.", text="Roll No.")
student_table.heading("Name", text="Name")
student_table.heading("Course", text="Course")
student_table.heading("D.O.B", text="D.O.B")
student_table.heading("Gender", text="Gender")
student_table.heading("Contact", text="Contact")
student_table.heading("Email id", text="Email id")
student_table.heading("Address", text="Address")
student_table['show'] = 'headings'

student_table.column("Roll No.", width=100)
student_table.column("Name", width=150)
student_table.column("Course", width=100)
student_table.column("D.O.B", width=100)
student_table.column("Gender", width=100)
student_table.column("Contact", width=120)
student_table.column("Email id", width=150)
student_table.column("Address", width=200)

fetch_data()
student_table.bind("<ButtonRelease-1>", get_cursor)

# Main loop
win.mainloop()
