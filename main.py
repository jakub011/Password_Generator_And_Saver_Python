from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def random_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
               'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for l in range(randint(8, 10))]
    password_list.extend([choice(symbols) for s in range(randint(2, 4))])
    password_list.extend([choice(numbers) for n in range(randint(2, 4))])
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.delete(0, "end")
    password_entry.insert(0,password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_name.get()
    email = email_username.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                file_contents = data_file.read()
                if len(file_contents) == 0:
                    data = {}
                else:
                    data = json.loads(file_contents)
        except FileNotFoundError:
            data = {}

        data.update(new_data)

        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)

        website_name.delete(0, "end")
        password_entry.delete(0, "end")

def find_password():
    website = website_name.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
        website_data = data[website]
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    except KeyError:
        messagebox.showinfo(title="Error", message="No details for the website exists")
    else:
        messagebox.showinfo(title=website, message=f"Email: {website_data['email']} \nPassword: {website_data['password']}")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_icon = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_icon)
canvas.grid(column=1, row=0)

label1 =  Label(text="Website:")
label1.grid(row=1, column=0)

label2 =  Label(text="Email/Username:")
label2.grid(row=2, column=0)

label3 =  Label(text="Password:")
label3.grid(row=3, column=0)

website_name = Entry(width=21)
website_name.grid(row=1, column=1)
website_name.focus()

email_username = Entry(width=35)
email_username.grid(row=2, column=1, columnspan=2)
email_username.insert(END, string="email@email.com")

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

button_search = Button(text="Search", width=14, command=find_password)
button_search.grid(row=1, column=2)

button_generate = Button(text="Generate Password", command=random_password)
button_generate.grid(row=3, column=2)

button_add = Button(text="Add", width=35, command=save)
button_add.grid(row=4, column=1, columnspan=2)

window.mainloop()
