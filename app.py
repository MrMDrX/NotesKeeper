import sys
import bcrypt
from tkinter import *
from tkinter import messagebox
from  customtkinter import *
from PIL import Image
import pymongo

class UserModel:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["NotesKeeper"]
        self.collection = self.db["users"]

    def register_user(self, name, username, password):
        user_data = {"name": name, "username": username, "password": password}
        result = self.collection.insert_one(user_data)
        return result.inserted_id

    def login_user(self, username, password):
        user = self.collection.find_one({"username": username, "password": password})
        return user

class NoteModel:
    def __init__(self, user_id):
        self.notes_ids = []
        self.selected_index = 0
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["NotesKeeper"]
        self.collection = self.db["notes"]
        self.user_id = user_id

    def db_insert_note(self, title, note):
        note_data = {"title": title, "note": note, "user_id": self.user_id}
        result = self.collection.insert_one(note_data)
        return result.inserted_id

    def db_select_user_notes(self):
        notes = self.collection.find({"user_id": self.user_id})
        return notes

    def db_select_specific_note(self, note_id):
        note = self.collection.find_one({"_id": note_id})
        return note

    def db_update_note(self, title, note, note_id):
        query = {"_id": note_id}
        new_values = {"$set": {"title": title, "note": note}}
        self.collection.update_one(query, new_values)

    def db_delete_note(self, note_id):
        query = {"_id": note_id}
        self.collection.delete_one(query)

class NoteView:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.master.resizable(False, False)

        self.master.config(bg="#26242f")

        self.top_left = Frame(self.master)
        self.top_right = Frame(self.master)

        self.scroll_list = Scrollbar(self.top_left)
        self.scroll_list.pack(side=RIGHT, fill=Y)

        self.list_notes = Listbox(self.top_left, height=37, width=25, font="Helvetica 14")
        self.list_notes.bind('<<ListboxSelect>>', self.controller.on_select)
        self.list_notes.pack(side=TOP, fill=Y, padx=(10, 0), pady=(10, 10))

        self.scroll_list.config(command=self.list_notes.yview)
        self.list_notes.config(
            fg="#ffffff",
            yscrollcommand=self.scroll_list.set,
            cursor="hand2",
            background="#26242f",
            highlightbackground="grey",
            bd=0,
            selectbackground="#F7941D"
        )

        self.text_frame = Frame(self.top_right)
        self.note_title = Entry(self.text_frame, width=52, font="Helvetica 14")
        self.note_title.insert(END, "Title")
        self.note_title.config(background="#26242f", highlightbackground="grey", fg="#ffffff")
        self.note_title.pack(side=TOP, pady=(5, 5), padx=(0, 10))

        self.scroll_text = Scrollbar(self.text_frame)
        self.scroll_text.pack(side=RIGHT, fill=Y)

        self.note_text = Text(self.text_frame, height=34, width=53, font="Helvetica 14")
        self.note_text.pack(side=TOP, fill=Y, padx=(5, 0), pady=(0, 5))
        self.note_text.tag_config("tag_your_message", foreground="blue")
        self.note_text.insert(END, "Notes")

        self.scroll_text.config(command=self.note_text.yview)
        self.note_text.config(
            yscrollcommand=self.scroll_text.set,
            fg="#ffffff",
            background="#26242f",
            highlightbackground="grey"
        )

        self.text_frame.pack(side=TOP)

        self.button_frame = Frame(self.top_right, background="#26242f")
        self.photo_add = PhotoImage(file="images/add.png")
        self.photo_edit = PhotoImage(file="images/edit.png")
        self.photo_delete = PhotoImage(file="images/delete.png")
        self.photo_logout = PhotoImage(file="images/logout.png")

        self.btn_save = Button(
            self.button_frame,
            text="Add",
            command=self.controller.save_note,
            image=self.photo_add
        )

        self.btn_edit = Button(
            self.button_frame,
            text="Update",
            command=self.controller.update_note,
            state=DISABLED,
            image=self.photo_edit
        )

        self.btn_delete = Button(
            self.button_frame,
            text="Delete",
            command=self.controller.delete_note,
            state=DISABLED,
            image=self.photo_delete
        )

        self.btn_logout = Button(
            self.button_frame,
            text="Logout",
            command=self.controller.logout,
            image=self.photo_logout
        )

        self.btn_save.grid(row=0, column=1)
        self.btn_edit.grid(row=0, column=2)
        self.btn_delete.grid(row=0, column=3)
        self.btn_logout.grid(row=0, column=4)

        self.button_frame.pack(side=TOP)

        self.top_left.pack(side=LEFT)
        self.top_right.pack(side=RIGHT)

class NoteController:
    def __init__(self, master, user_id):
        self.model = NoteModel(user_id)
        self.view = NoteView(master, self)
        master.title("Notes Keeper")
        if (sys.platform.startswith('win')): 
            master.iconbitmap('images/logo.ico')
        else:
            logo = PhotoImage(file='images/logo.png')
            master.call('wm', 'iconphoto', master._w, logo)
        self.init_notes()

    def init_notes(self):
        notes = self.model.db_select_user_notes()
        for note in notes:
            self.view.list_notes.insert(END, note["title"])
            self.model.notes_ids.append(note["_id"])

    def save_note(self):
        title = self.view.note_title.get()
        note = self.view.note_text.get("1.0", END)

        inserted_id = self.model.db_insert_note(title, note)
        self.view.list_notes.insert(END, title)
        self.model.notes_ids.append(inserted_id)

        self.view.note_title.delete(0, END)
        self.view.note_text.delete('1.0', END)

    def update_note(self):
        title = self.view.note_title.get()
        note = self.view.note_text.get("1.0", END)
        note_id = self.model.notes_ids[self.model.selected_index]

        self.model.db_update_note(title, note, note_id)

        self.view.list_notes.delete(self.model.selected_index)
        self.view.list_notes.insert(self.model.selected_index, title)

        self.view.note_title.delete(0, END)
        self.view.note_text.delete('1.0', END)

    def delete_note(self):
        title = self.view.note_title.get()
        notes = self.view.note_text.get("1.0", END)

        if not title or not notes.rstrip():
            messagebox.showerror(title="ERROR!!!", message="Please select a note to delete")
            return

        result = messagebox.askquestion("Delete", "Are you sure you want to delete?", icon='warning')

        if result == 'yes':
            note_id = self.model.notes_ids[self.model.selected_index]
            self.model.db_delete_note(note_id)
            del self.model.notes_ids[self.model.selected_index]

            self.view.note_title.delete(0, END)
            self.view.note_text.delete('1.0', END)
            self.view.list_notes.delete(self.model.selected_index)

    def on_select(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.model.selected_index = index
        self.display_note()

    def display_note(self):
        self.view.note_title.delete(0, END)
        self.view.note_text.delete('1.0', END)

        note_id = self.model.notes_ids[self.model.selected_index]
        note = self.model.db_select_specific_note(note_id)

        self.view.note_title.insert(END, note["title"])
        self.view.note_text.insert(END, note["note"])

        self.view.btn_delete.config(state=NORMAL)
        self.view.btn_edit.config(state=NORMAL)

    def logout(self):
        self.view.master.destroy()
        welcome_controller = WelcomeController()

class RegisterModel:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["NotesKeeper"]
        self.collection = self.db["users"]

    def register_user(self, name, username, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data = {"name": name, "username": username, "password": hashed_password}
        result = self.collection.insert_one(user_data)
        return result.inserted_id

    def login_user(self, username, password):
        user = self.collection.find_one({"username": username, "password": password})
        return user

class RegisterView:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller

        master.geometry("600x400")
        master.resizable(False, False)

        lable = CTkLabel(
            master=self.master, text="Sign up for a new Account", font=('Century Gothic', 20))
        lable.pack(padx=50, pady=45)

        self.name_entry = CTkEntry(self.master, width=240, height=32, placeholder_text="Full Name")
        self.name_entry.pack(pady=12, padx=10)

        self.username_entry = CTkEntry(self.master, width=240, height=32, placeholder_text="Username")
        self.username_entry.pack(pady=12, padx=10)

        self.password_entry = CTkEntry(self.master, width=240, height=32, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=12, padx=10)

        self.register_button = CTkButton(self.master, width=240, height=32, text="Register", command=self.controller.register_user)
        self.register_button.pack(pady=12, padx=10)

class RegisterController:
    def __init__(self, master):
        self.model = RegisterModel()
        self.view = RegisterView(master, self)
        master.title("Register")
        if (sys.platform.startswith('win')): 
            master.iconbitmap('images/logo.ico')
        else:
            logo = PhotoImage(file='images/logo.png')
            master.call('wm', 'iconphoto', self.root._w, logo)

    def register_user(self):
        name = self.view.name_entry.get()
        username = self.view.username_entry.get()
        password = self.view.password_entry.get()

        if not name or not username or not password:
            messagebox.showerror(title="ERROR!!!", message="Please fill in all fields")
            return
        
        if len(username) <= 3 :
            messagebox.showerror(title="ERROR!!!", message="Username should be more than 3 characters")
            return
        
        if username.isdigit():
            messagebox.showerror(title="ERROR!!!", message="Username can't be all numeric")
            return

        if len(password) <= 5:
            messagebox.showerror(title="ERROR!!!", message="Password should be more than 5 characters")
            return

        if self.model.collection.find_one({"username": username}):
            messagebox.showerror(title="ERROR!!!", message="Username already exists. Please choose a new username")
            return

        inserted_id = self.model.register_user(name, username, password)

        self.view.master.destroy()
        note_controller = NoteController(Tk(), inserted_id)

class LoginModel:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["NotesKeeper"]
        self.collection = self.db["users"]

    def login_user(self, username, password):
        user = self.collection.find_one({"username": username})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return user
        return None

class LoginView:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller

        master.geometry("600x400")
        master.resizable(False, False)

        lable = CTkLabel(
            master=self.master, text="Log into your Account", font=('Century Gothic', 20))
        lable.pack(padx=50, pady=45)

        self.username_entry = CTkEntry(self.master, width=240, height=32, placeholder_text="Username")
        self.username_entry.pack(pady=12, padx=10)

        self.password_entry = CTkEntry(self.master, width=240, height=32, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=12, padx=10)

        self.login_button = CTkButton(self.master, width=240, height=32, text="Login", command=self.controller.login_user)
        self.login_button.pack(pady=12, padx=10)

class LoginController:
    def __init__(self, master):
        self.model = LoginModel()
        self.view = LoginView(master, self)
        master.title("Login")
        if (sys.platform.startswith('win')): 
            master.iconbitmap('images/logo.ico')
        else:
            logo = PhotoImage(file='images/logo.png')
            master.call('wm', 'iconphoto', master._w, logo)

    def login_user(self):
        username = self.view.username_entry.get()
        password = self.view.password_entry.get()

        if not username or not password:
            messagebox.showerror(title="ERROR!!!", message="Please fill in all fields")
            return

        user = self.model.login_user(username, password)

        if user:
            self.view.master.destroy()
            note_controller = NoteController(Tk(), user["_id"])
        else:
            messagebox.showerror(title="ERROR!!!", message="Invalid username or password")

class WelcomeView:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller

        self.master.geometry("600x400")
        self.master.resizable(False, False)

        lable = CTkLabel(
            master=self.master, text="Welcome to Notes Keeper", font=('Century Gothic', 24))
        lable.pack(padx=24, pady=24)

        self.welcome_image = CTkImage(Image.open("images/noteskeeper.png"), size=(128, 128))
        self.image_label = CTkLabel(self.master, text="", image=self.welcome_image)
        self.image_label.pack(pady=10)

        subtitle = CTkLabel(
            master=self.master, text="Your ultimate notes taking app", font=('Century Gothic', 16))
        subtitle.pack(padx=10, pady=10)

        self.login_button = CTkButton(self.master, text="Login", command=self.controller.open_login)
        self.login_button.pack(side="left", padx=(10, 5))

        self.register_button = CTkButton(self.master, text="Register", command=self.controller.open_register)
        self.register_button.pack(side="right", padx=(5, 10))

class WelcomeController:
    def __init__(self):
        self.root = CTk()
        self.root.title("NotesKeeper")
        if (sys.platform.startswith('win')): 
            self.root.iconbitmap('images/logo.ico')
        else:
            logo = PhotoImage(file='images/logo.png')
            self.root.call('wm', 'iconphoto', self.root._w, logo)
        self.view = WelcomeView(self.root, self)
        self.root.mainloop()

    def open_login(self):
        self.root.destroy()
        login_controller = LoginController(CTk())

    def open_register(self):
        self.root.destroy()
        register_controller = RegisterController(CTk())

if __name__ == "__main__":
    welcome_controller = WelcomeController()

'''
/**********************************************************
 **  ©Med0X All rights reserved to me @MrMdrX in Github  **
 **               https://mrmdrx.github.io               **
 *********************************************************/
 '''