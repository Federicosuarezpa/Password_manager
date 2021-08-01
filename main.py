import os

from pymongo import MongoClient
import secrets
import tkinter as tk
from tkinter import messagebox
import validators
from dotenv import load_dotenv

fields = 'Account', 'Url', 'New password', 'Your password'
load_dotenv()
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")


def insert_new_password(entries_values):
    try:
        data = []
        for entry in entries_values:
            data.append(entry[1].get())
        if len(data) >= 2:
            client = MongoClient(
                "mongodb+srv://PasswordManager:" + PASSWORD + "@cluster0.sld3b.mongodb.net/" + DATABASE + "?retryWrites"
                                                                                                          "=true&w "
                                                                                                          "=majority")
            password_manager = client.PasswordManager
            password = password_manager.password
            if data[2] == '':
                data[2] = secrets.token_urlsafe(15)
            if data[2] != '':
                info = password.find_one({"data.account": str(data[0]), "data.url": str(data[1])})
                if info is not None:
                    password.replace_one({"data.account": data[0], "data.url": data[1]},
                                         {"data.account": data[0], "data"
                                                                   ".url": data[1], "password": data[2]})
                else:
                    password_data = {
                        "data": {"account": str(data[0]), "url": str(data[1]), "password": str(data[2])}
                    }
                    valid_url = validators.url(data[1])
                    if valid_url:
                        password.insert_one(password_data)
                        messagebox.showinfo("Mensaje", "Contraseña guardada con éxito")
                    else:
                        messagebox.showerror("Url inválida", "Url no válida puede que te falte https://")
        else:
            messagebox.showerror("Error", "Faltan datos")
    except Exception as e:
        print(e)


def get_info(entries_values):
    try:
        data = []
        for entry in entries_values:
            data.append(entry[1].get())
        client = MongoClient(
            "mongodb+srv://PasswordManager:hpgldho2wQl2lKnv@cluster0.sld3b.mongodb.net/"
            "myFirstDatabase?"
            "retryWrites"
            "=true&w "
            "=majority")
        password_manager = client.PasswordManager
        password = password_manager.password
        info = password.find_one({"data.account": str(data[0]), "data.url": str(data[1])})
        return info
    except Exception as e:
        print(e)


def copy_password(root_elem, entries_values):
    try:
        info = get_info(entries_values)
        root_elem.clipboard_clear()
        root_elem.clipboard_append(info["data"]["password"])
        root_elem.update()
    except Exception as e:
        messagebox.showerror("Error", e)


def show_password(entries_values):
    try:
        info = get_info(entries_values)
        password_show.set(info["data"]["password"])
    except Exception as e:
        print(e)


def make_form(root_elem, fields_to_fill):
    entries_elems = []
    for idx, field in enumerate(fields_to_fill):
        row = tk.Frame(root_elem)
        lab = tk.Label(row, width=15, text=field, anchor='w')
        if idx != 3:
            ent = tk.Entry(row)
        elif idx == 2:
            ent = tk.Entry(row, show="*")
            ent.config(show="*")
        else:
            ent = tk.Entry(row, state='readonly', textvariable=password_show)
        if idx == 2:
            ent.config(show='*')
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries_elems.append((field, ent))
    return entries_elems


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Password Manager")
    password_show = tk.StringVar()
    entries = make_form(root, fields)
    root.bind('<Return>', (lambda event, e=entries: insert_new_password(e)))
    b1 = tk.Button(root, text='insert new password',
                   command=(lambda e=entries: insert_new_password(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b3 = tk.Button(root, text='Show password',
                   command=(lambda e=entries: show_password(e)))
    b3.pack(side=tk.LEFT, padx=5, pady=5)
    b4 = tk.Button(root, text='Copy password',
                   command=(lambda e=entries: copy_password(root, e)))
    b4.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = tk.Button(root, text='Quit', command=root.quit)
    b2.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()
