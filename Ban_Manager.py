import json
import tkinter.messagebox
import sys
from json import JSONDecodeError

try:
    with open("session.json", "r", encoding="utf-8") as session_file:
        session_data = json.load(session_file)

    if not session_data.get("logged_in"):
        raise FileNotFoundError  # Falls "logged_in" nicht True ist, beenden

except (FileNotFoundError, json.JSONDecodeError):
    tkinter.messagebox.showerror("Fehler", "Kein gültiger Login! Bitte zuerst anmelden.")
    sys.exit()  # 🚫 Beendet das Programm sofort


import customtkinter as ctk

#set default values
ctk.set_appearance_mode("dark")

#create root
root = ctk.CTk()
root.geometry("920x620")
root.resizable(False, False)
root.title("Ban Manager")

#The main frame
ban_manager_frame = ctk.CTkFrame(master=root, fg_color="white", height = 1000, width= 300)

#A function to saves the banned user
def user_banned():
    username = user_name_entry.get()
    platform = platform_name_entry.get()

    if username and platform:
        try:
            with open("banned_user.json", "r", encoding="utf-8") as f:
                banned_user = json.load(f)

        except (FileNotFoundError, JSONDecodeError):
            banned_user = {}

        if username in banned_user:
            banned_user[username].append(platform)

        else:
            banned_user[username] = [platform]

        with open("banned_user.json", "w", encoding="utf-8") as f:
            json.dump(banned_user, f, indent=4)
    else:
        tkinter.messagebox.showerror(title="Error!", message="No valid input given.")

#A function which searches for the banned user
def search_banned_user():
    username = search_user_entry.get().lower().strip()
    if username:
        try:
            with open("banned_user.json", "r") as f:
                banned_user = json.load(f)

            key_of_user = next((key for key in banned_user if key.lower() == username), None)

            if key_of_user:
                value_of_user = banned_user[key_of_user]
                joinedvalue = ", ".join(value_of_user)
                tkinter.messagebox.showinfo(title="User found!", message=f"The User {key_of_user} was banned on: {joinedvalue}! ")
            else:
                tkinter.messagebox.showerror(title="Error!", message="User not found!")

        except(FileNotFoundError, JSONDecodeError):
            tkinter.messagebox.showerror(title="Error!", message="File not found.")

#Username
user_name = ctk.CTkLabel(ban_manager_frame, text="Username", font=("Arial", 20, "bold"), text_color="black")
user_name_entry = ctk.CTkEntry(ban_manager_frame, placeholder_text="Which User?", height= 45, width= 190)
user_name.grid(row = 0, column = 0)
user_name_entry.grid(row = 1, column = 0)

#Platform
platform_name = ctk.CTkLabel(ban_manager_frame, text="Platform", font=("Arial", 20, "bold"), text_color="black")
platform_name_entry = ctk.CTkEntry(ban_manager_frame, placeholder_text= "Which Platform?", height= 45, width= 190)
platform_name.grid(row = 0, column = 1)
platform_name_entry.grid(row = 1, column = 1)

#A button to save the banned user
send_button = ctk.CTkButton(ban_manager_frame, text="send", font=("Arial", 18, "bold"), height= 35, width=30, command=user_banned)
send_button.grid(row = 2, column = 0, columnspan = 2, sticky = "ew")

#Searchbar
search_user = ctk.CTkLabel(ban_manager_frame, text="Search", font=("Arial", 20, "bold"),height= 35, width=30 , text_color="black")
search_user_entry = ctk.CTkEntry(ban_manager_frame, placeholder_text="Write his Username", width= 300, height= 40)
search_user.grid(row = 3, column = 0, columnspan = 2)
search_user_entry.grid(row = 4, column = 0, columnspan = 2)

#A button to call the search function
search_button = ctk.CTkButton(ban_manager_frame, text="search",font=("Arial", 20, "bold"),height= 45, width=200, command=search_banned_user)
search_button.grid(row = 5, column = 0, columnspan = 2)

ban_manager_frame.pack(expand = True)

for widget in ban_manager_frame.winfo_children():
    widget.grid_configure(padx = 65, pady = 10)

#mainloop
root.mainloop()

