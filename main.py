import json
import os
import random
import string
import sys
from tkinter import *
from tkinter import messagebox

import pyperclip

######################    Used lines below here for make an .exe file with pyinstaller ####################


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
####################

# Generator #


def generate_password():
    letters = string.ascii_letters
    numbers = string.digits
    symbols = string.punctuation

    num_letters = random.randint(8, 10)
    num_numbers = random.randint(2, 4)
    num_symbols = random.randint(2, 4)

    password_list = []

    password_list = [random.choice(letters) for _ in range(num_letters)]
    password_list += [random.choice(numbers) for _ in range(num_numbers)]
    password_list += [random.choice(symbols) for _ in range(num_symbols)]

    random.shuffle(password_list)

    password = ''.join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    

#* Search Function # 


def search_func():
    name = website_entry.get().title()
    try:
        with open('data.json', mode='r') as data_file:
            data = json.load(data_file)
            
    except FileNotFoundError:
        messagebox.showerror(title='Error', message='No Data File Found.')
        
    else:
        for key in data.keys():
            if name == key:
                email = data[key]['email']
                password = data[key]['password']
                messagebox.showinfo(title='Info', message=f'Email: {email}\nPassword: {password}' )
                pyperclip.copy(password)
            else:
                messagebox.showinfo(title='Info', message='No details for the website exists.')


# * Getting entries and create(or append) a data file.


def get_texts():
    name = website_entry.get().title()
    email = user_entry.get().lower()
    password = password_entry.get()
    data_json = {
        name: {
            'email': email,
            'password': password,
        }
    }

    if name == '' or email == '' or password == '':
        messagebox.showerror(title='Error', message='Please don\'t leave any empty fields.')

    else:
        want_continue = messagebox.askyesno(
            title=name, message=f'These are the details: \n\nWebsite: {name} \nEmail: {email} \nPassword: {password} \n ')

        if want_continue:
            try:
                with open('data.json', mode='r') as data_file:
                    data = json.load(data_file)

            except FileNotFoundError:
                with open('data.json', mode='w') as data_file:
                    json.dump(data_json, data_file, indent=4)

            else:
                data.update(data_json)
                with open('data.json', mode='w') as data_file:
                    json.dump(data, data_file, indent=4)

            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# * UI

window = Tk()
#window.minsize(width=660, height=484)
window.title('Password Manager by YS')
window.config(padx=50, pady=50)

canvas = Canvas(width=256, height=256)
lock_photo = PhotoImage(file=resource_path('logo.png'))
canvas.create_image(130, 128, image=lock_photo)
canvas.grid(column=1, row=0)

# * Label

website = Label(text='Website:', pady=5, padx=10)
website.grid(column=0, row=1)

user = Label(text='Email/Username:', pady=5, padx=10)
user.grid(column=0, row=2)

password = Label(text='Password:', pady=5, padx=10)
password.grid(column=0, row=3)

# * Entry

website_entry = Entry(width=41)
website_entry.grid(column=1, row=1, columnspan=2, sticky='W', pady=5)
website_entry.focus()

user_entry = Entry(width=35)
user_entry.grid(column=1, row=2, columnspan=2, sticky='EW')

password_entry = Entry(width=41)
password_entry.grid(column=1, row=3, sticky='W')

# * Button

gen_pass = Button(text='Generate Password', highlightthickness=0, command=generate_password)
gen_pass.grid(column=2, row=3, sticky='EW')

add_button = Button(text='Add', width=35, command=get_texts, highlightthickness=0)
add_button.grid(column=1, row=4, pady=5, columnspan=2, sticky='EW')

search_button = Button(text='Search', highlightthickness=0, command=search_func)
search_button.grid(column=2, row=1, sticky='EW')


window.mainloop()
