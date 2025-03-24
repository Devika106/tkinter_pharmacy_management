
import tkinter as tk
from tkinter import ttk,messagebox
from tkinter import *
import pymysql

# Connect to mysql Database
db = pymysql.connect(
    host="localhost",
    user="root",
    password="Devika@22",
    database="pharmacy_db",

)
cursor = db.cursor()



def add_medicine():
    name = name_var.get()
    quantity = quantity_var.get()
    price = price_var.get()
    expiry_date = expiry_var.get()

    if name and quantity and price and expiry_date:
        query = "INSERT INTO medicines (name, quantity, price, expiry_date) VALUES (%s, %s, %s, %s)"
        values = (name, quantity, price, expiry_date)
        cursor.execute(query, values)
        db.commit()
        messagebox.showinfo("Success", "Medicine added successfully.")
        clear_fields()
        view_medicines()
    else:
        messagebox.showwarning("Warning", "All fields are required!")


# Function to clear input fields
def clear_fields():
    name_var.set("")
    quantity_var.set("")
    price_var.set("")
    expiry_var.set("")



def view_medicines():
    cursor.execute("SELECT * FROM medicines")
    rows = cursor.fetchall()
    medicine_list.delete(*medicine_list.get_children())
    for row in rows:
        medicine_list.insert('', tk.END, values=row)


def delete_medicine():
    selected = medicine_list.selection()
    if selected:
        medicine_id = medicine_list.item(selected[0])['values'][0]
        cursor.execute("DELETE FROM medicines WHERE id = %s", (medicine_id,))
        db.commit()
        messagebox.showinfo("Success", "Medicine deleted successfully.")
        view_medicines()
    else:
        messagebox.showwarning("Warning", "No medicine selected.")



def update_medicine():
    selected = medicine_list.selection()
    if selected:
        medicine_id = medicine_list.item(selected[0])['values'][0]
        name = name_var.get()
        quantity = quantity_var.get()
        price = price_var.get()
        expiry_date = expiry_var.get()

        if name and quantity and price and expiry_date:
            query = "UPDATE medicines SET name=%s, quantity=%s, price=%s, expiry_date=%s WHERE id=%s"
            values = (name, quantity, price, expiry_date, medicine_id)
            cursor.execute(query, values)
            db.commit()
            messagebox.showinfo("Success", "Medicine updated successfully.")
            clear_fields()
            view_medicines()
        else:
            messagebox.showwarning("Warning", "All fields are required!")
    else:
        messagebox.showwarning("Warning", "No medicine selected.")



def select_medicine(event):
    selected = medicine_list.selection()
    if selected:
        medicine = medicine_list.item(selected[0])['values']
        name_var.set(medicine[1])
        quantity_var.set(medicine[2])
        price_var.set(medicine[3])
        expiry_var.set(medicine[4])



root = tk.Tk()
root.title("Pharmacy Management System")
root.geometry("1000x400")
root.configure(bg='skyblue')

name_var = tk.StringVar()
quantity_var = tk.StringVar()
price_var = tk.StringVar()
expiry_var = tk.StringVar()

tk.Label(root, text="Medicine_Name :",bg="skyblue").grid(row=0, column=0)
tk.Entry(root, textvariable=name_var,bg="lavender").grid(row=0, column=1)

tk.Label(root, text="Quantity :",bg="skyblue").grid(row=1, column=0)
tk.Entry(root, textvariable=quantity_var,bg="lavender").grid(row=1, column=1)

tk.Label(root, text="Price :",bg="skyblue").grid(row=2, column=0)
tk.Entry(root, textvariable=price_var,bg="lavender").grid(row=2, column=1)

tk.Label(root, text="Expiry Date (YYYY-MM-DD) :",bg="skyblue").grid(row=3, column=0)
tk.Entry(root, textvariable=expiry_var,bg="lavender").grid(row=3, column=1)

tk.Button(root, text="Add Medicine", command=add_medicine,fg="blue",bg="pink").grid(row=4, column=0, pady=10)
tk.Button(root, text="Update Medicine", command=update_medicine,fg="blue",bg="pink").grid(row=4, column=1)
tk.Button(root, text="Clear", command=clear_fields,fg="blue",bg="pink").grid(row=4, column=2)

medicine_list = ttk.Treeview(root, columns=("ID", "Name", "Quantity", "Price", "Expiry Date"), show="headings",)
medicine_list.heading("ID", text="ID")
medicine_list.heading("Name", text="Name")
medicine_list.heading("Quantity", text="Quantity")
medicine_list.heading("Price", text="Price")
medicine_list.heading("Expiry Date", text="Expiry Date")
medicine_list.bind("<Double-1>", select_medicine)
medicine_list.grid(row=5, column=0, columnspan=3,)

tk.Button(root, text="Delete Medicine", command=delete_medicine,fg="blue",bg="pink").grid(row=6, column=0, columnspan=3)

view_medicines()

root.mainloop()
