import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def create_table():
    conn = sqlite3.connect('phonebook.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  phone TEXT NOT NULL,
                  comment TEXT)''')
    conn.commit()
    conn.close()

def insert_data(name, phone, comment):
    conn = sqlite3.connect('phonebook.db')
    c = conn.cursor()
    c.execute("INSERT INTO contacts (name, phone, comment) VALUES (?, ?, ?)", (name, phone, comment))
    conn.commit()
    conn.close()
    update_table()

def update_table(search_text=""):
    for row in tree.get_children():
        tree.delete(row)
    
    conn = sqlite3.connect('phonebook.db')
    c = conn.cursor()
    if search_text:
        c.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ? OR comment LIKE ?", 
                  ('%' + search_text + '%',) * 3)
    else:
        c.execute("SELECT * FROM contacts")
    rows = c.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=(row[1], row[2], row[3], row[0]))
    conn.close()

def submit():
    name = entry_name.get()
    phone = entry_phone.get()
    comment = entry_comment.get()
    if name and phone:
        insert_data(name, phone, comment)
        entry_name.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        entry_comment.delete(0, tk.END)
        add_contact_popup.destroy()
    else:
        messagebox.showerror("Error", "Please enter both name and phone")

def open_add_contact_popup():
    global add_contact_popup, entry_name, entry_phone, entry_comment

    add_contact_popup = tk.Toplevel()
    add_contact_popup.title("Add New Contact")

    label_name = tk.Label(add_contact_popup, text="Name:")
    label_name.grid(row=0, column=0, padx=5, pady=5)
    entry_name = tk.Entry(add_contact_popup)
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    label_phone = tk.Label(add_contact_popup, text="Phone:")
    label_phone.grid(row=1, column=0, padx=5, pady=5)
    entry_phone = tk.Entry(add_contact_popup)
    entry_phone.grid(row=1, column=1, padx=5, pady=5)

    label_comment = tk.Label(add_contact_popup, text="Comment:")
    label_comment.grid(row=2, column=0, padx=5, pady=5)
    entry_comment = tk.Entry(add_contact_popup)
    entry_comment.grid(row=2, column=1, padx=5, pady=5)

    submit_button = tk.Button(add_contact_popup, text="Add Contact", command=submit)
    submit_button.grid(row=3, column=0, columnspan=2, pady=10)

def open_edit_contact_popup():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a contact to edit")
        return
    
    contact_values = tree.item(selected_item[0], "values")
    contact_id = contact_values[3]  # ID is stored in the hidden 4th column

    global edit_contact_popup, entry_edit_name, entry_edit_phone, entry_edit_comment

    def save_edit():
        name = entry_edit_name.get()
        phone = entry_edit_phone.get()
        comment = entry_edit_comment.get()
        if name and phone:
            conn = sqlite3.connect('phonebook.db')
            c = conn.cursor()
            c.execute("UPDATE contacts SET name = ?, phone = ?, comment = ? WHERE id = ?", (name, phone, comment, contact_id))
            conn.commit()
            conn.close()
            update_table()
            edit_contact_popup.destroy()
        else:
            messagebox.showerror("Error", "Please enter both name and phone")

    conn = sqlite3.connect('phonebook.db')
    c = conn.cursor()
    c.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
    contact = c.fetchone()
    conn.close()

    edit_contact_popup = tk.Toplevel()
    edit_contact_popup.title("Edit Contact")

    label_name = tk.Label(edit_contact_popup, text="Name:")
    label_name.grid(row=0, column=0, padx=5, pady=5)
    entry_edit_name = tk.Entry(edit_contact_popup)
    entry_edit_name.grid(row=0, column=1, padx=5, pady=5)
    entry_edit_name.insert(0, contact[1])

    label_phone = tk.Label(edit_contact_popup, text="Phone:")
    label_phone.grid(row=1, column=0, padx=5, pady=5)
    entry_edit_phone = tk.Entry(edit_contact_popup)
    entry_edit_phone.grid(row=1, column=1, padx=5, pady=5)
    entry_edit_phone.insert(0, contact[2])

    label_comment = tk.Label(edit_contact_popup, text="Comment:")
    label_comment.grid(row=2, column=0, padx=5, pady=5)
    entry_edit_comment = tk.Entry(edit_contact_popup)
    entry_edit_comment.grid(row=2, column=1, padx=5, pady=5)
    entry_edit_comment.insert(0, contact[3])

    save_button = tk.Button(edit_contact_popup, text="Save", command=save_edit)
    save_button.grid(row=3, column=0, columnspan=2, pady=10)

def delete_contact():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a contact to delete")
        return

    contact_values = tree.item(selected_item[0], "values")
    contact_id = contact_values[3]  # ID is stored in the hidden 4th column

    conn = sqlite3.connect('phonebook.db')
    c = conn.cursor()
    c.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()
    update_table()

def search_contacts(*args):
    search_text = search_var.get()
    update_table(search_text)

# Create the main window
root = tk.Tk()
root.title("Phonebook Application")
root.geometry("800x600")

# Create frame for buttons
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=20)

# Create Add, Edit, and Delete buttons
add_contact_button = tk.Button(frame_buttons, text="Add Contact", command=open_add_contact_popup)
add_contact_button.grid(row=0, column=0, padx=5)

edit_contact_button = tk.Button(frame_buttons, text="Edit Contact", command=open_edit_contact_popup)
edit_contact_button.grid(row=0, column=1, padx=5)

delete_contact_button = tk.Button(frame_buttons, text="Delete Contact", command=delete_contact)
delete_contact_button.grid(row=0, column=2, padx=5)

# Create frame for search
frame_search = tk.Frame(root)
frame_search.pack(pady=10)

search_var = tk.StringVar()
search_var.trace("w", search_contacts)
label_search = tk.Label(frame_search, text="Search:")
label_search.pack(side=tk.LEFT, padx=5)
entry_search = tk.Entry(frame_search, textvariable=search_var)
entry_search.pack(side=tk.LEFT, padx=5)

# Create table frame
frame_table = tk.Frame(root)
frame_table.pack(pady=20)

columns = ("Name", "Phone", "Comment")
tree = ttk.Treeview(frame_table, columns=columns, show='headings')
tree.heading("Name", text="Name")
tree.heading("Phone", text="Phone")
tree.heading("Comment", text="Comment")
tree.pack()

# Initialize the database
create_table()
update_table()

# Run the main loop
root.mainloop()
