#Import Customtkinter
import tkinter.messagebox
from json import JSONDecodeError
import customtkinter
import json
import subprocess

#Import hashlib and set it
import hashlib

#Set color theme
appearance = customtkinter.set_appearance_mode("dark")
default_color = customtkinter.set_default_color_theme("green")

#A function that saves the user data in a dictionary
def saved_user_data():
    email = email_entry.get().lower().strip()
    if len(password_entry.get()) > 0 and len(email) > 0:
        hashed = hashlib.sha256(password_entry.get().encode()).hexdigest()
        try:
            with open("login_information.json", "r", encoding="utf-8") as f:
                login_information = json.load(f)
        except (FileNotFoundError, JSONDecodeError):
            login_information = {}

        if email in login_information:
            tkinter.messagebox.showerror(title="Error!", message="Account Already exists.")
        else:
            login_information[email] = [hashed]
            with open("login_information.json", "w", encoding="utf-8") as f:
                json.dump(login_information, f, indent=4)
            tkinter.messagebox.showinfo(title="Created", message="Your Account got created. Please click the button after 'send' to access the login screen")
    else:
        tkinter.messagebox.showerror(title="Error", message="No Input given!")


# A function that brings us to the login screen
def login_screen():
    root.withdraw()

    #A function to load the saved user data
    def load_saved_user_data():
        email = email_label_check_entry.get().lower().strip()
        if len(password_entry_check.get()) > 0 and len(email) > 0:
            hashed = hashlib.sha256(password_entry_check.get().encode()).hexdigest()
            try:
                with open("login_information.json", "r", encoding="utf-8") as f:
                    found_user = json.load(f)

                found_user_key = next((key for key in found_user if key.lower() == email), None)
                if found_user_key:
                    value_of_key = found_user[found_user_key]
                    if hashed == value_of_key[0]:
                        tkinter.messagebox.showinfo(title="Account found!", message="Great you can continue!")
                        with open("session.json", "w", encoding="utf-8") as session_file:
                            json.dump({"logged_in" : True, "user":email}, session_file)

                        window.destroy()
                        subprocess.run(["python", "Ban_Manager.py"])

                    else:
                        tkinter.messagebox.showerror(title="Error!", message="Wrong Password!")

            except (FileNotFoundError, JSONDecodeError):
                tkinter.messagebox.showerror(title="Error", message="File not found!")
        else:
            tkinter.messagebox.showerror(title="Error", message="No Input given!")

    #Some asthetic for the new window
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    #A new Window
    window = customtkinter.CTk()
    window.geometry("580x540")
    window.resizable(False, False)
    window.title("Login")

    # A frame to take the labels, entries and the button
    frame_login = customtkinter.CTkFrame(master=window, corner_radius=20, fg_color="#ece806")

    # Title label
    log_in = customtkinter.CTkLabel(frame_login, text="Login Site", text_color="black")
    log_in.configure(font=("Arial", 24, "bold"))
    log_in.pack()

    # Email label with input field and password label with input field
    email_label_check = customtkinter.CTkLabel(frame_login, text="Email", text_color="black")
    email_label_check.configure(font=("Arial", 16, "bold"))
    email_label_check_entry = customtkinter.CTkEntry(frame_login, placeholder_text="Enter Email", text_color="white", width=200)

    password_label_check = customtkinter.CTkLabel(frame_login, text="Password", text_color="black")
    password_label_check.configure(font=("Arial", 16, "bold"))
    password_entry_check = customtkinter.CTkEntry(frame_login, placeholder_text="Enter Password", text_color="white", width=200, show = "*")

    # A button to send the data to the save file
    send_data_button_check = customtkinter.CTkButton(frame_login, text="Send", text_color="black", fg_color="#ffffff",
                                               command=load_saved_user_data)
    send_data_button_check.configure(font=("Arial", 12, "bold"))

    # A button to switch to log-in
    register = customtkinter.CTkButton(frame_login, text="Go to Register", text_color="black", fg_color="#ffffff", command=lambda: [window.withdraw(), root.deiconify()])

    # pack them all in order
    email_label_check.pack()
    email_label_check_entry.pack()
    password_label_check.pack()
    password_entry_check.pack()
    send_data_button_check.pack()
    register.pack()

    frame_login.pack(padx=20, pady=100, fill="both", expand=True, anchor="center")

    for widgets in frame_login.winfo_children():
        widgets.pack_configure(padx=10, pady=8, )

    window.mainloop()


# Set a window
root = customtkinter.CTk()
root.geometry("580x540")
root.resizable(False, False)
root.title("Registration")

#A frame to take the labels, entries and the button
frame2 = customtkinter.CTkFrame(master=root, corner_radius=20, fg_color="#ece806")

#Title label
registration = customtkinter.CTkLabel(frame2, text="Registration site", text_color="black")
registration.configure(font=("Arial", 24,"bold"))
registration.pack()

#Email label with input field and password label with input field
email_label = customtkinter.CTkLabel(frame2, text="Email", text_color="black")
email_label.configure(font=("Arial", 16, "bold"))
email_entry = customtkinter.CTkEntry(frame2, placeholder_text="Enter Email", text_color="white", width=200)

password_label = customtkinter.CTkLabel(frame2, text="Password", text_color="black")
password_label.configure(font=("Arial", 16, "bold"))
password_entry = customtkinter.CTkEntry(frame2, placeholder_text="Enter Password", text_color="white", width=200, show = "*")

#A button to send the data to the save file
send_data_button = customtkinter.CTkButton(frame2, text="Send", text_color="black", fg_color="#ffffff", command=saved_user_data)
send_data_button.configure(font=("Arial", 12, "bold"))

#A button to switch to log-in
login_button = customtkinter.CTkButton(frame2,text="Go to Login",text_color="black", fg_color="#ffffff", command=login_screen)

#pack them all in order
email_label.pack()
email_entry.pack()
password_label.pack()
password_entry.pack()
send_data_button.pack()
login_button.pack()

frame2.pack(padx=20, pady = 100, fill = "both", expand = True,  anchor = "center")

for widget in frame2.winfo_children():
    widget.pack_configure(padx = 10, pady = 8, )

root.mainloop()