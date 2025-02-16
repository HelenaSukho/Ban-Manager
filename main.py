# Today we are programming an Application where we store the data of somebody we banned in Discord or Twitch.
# We can later on search for his name in the Application and look if he is in the ban list

# Import needed elements
import tkinter as tk
from tkinter import messagebox
import json

# We first create a root window
root = tk.Tk()
root.resizable(False, False)
root.title("Ban-Manager")
root.configure(bg="white")


# A function that creates a dictionary in which the Platform of the User and the Username gets nested.
def banned_user_list():
    platform = platform_of_banned_user_entry.get()
    username = username_of_banned_user_entry.get().strip()
    if username and platform:
        try:
            with open("banned_users.json", "r", encoding="utf-8") as f:
                banned_users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            banned_users = {}

        if username in banned_users:
            banned_users[username].append(platform)
        else:
            banned_users[username] = [platform]

        with open("banned_users.json", "w", encoding="utf-8") as f:
            json.dump(banned_users, f, indent=4)
    else:
        tk.messagebox.showerror(title="Error!", message="Either username or platform or both are empty!")


# Now we need a function that prints out the searched user if he is banned or not
def user_banned_or_not():
    username = banned_user_search.get().strip().lower()
    if username:
        try:
            with open("banned_users.json", "r", encoding="utf-8") as f:
                found_users = json.load(f)

            key_of_banned_user = next((key for key in found_users if key.lower() == username), None)

            if key_of_banned_user:
                value_of_banned_user = found_users[key_of_banned_user]
                tk.messagebox.showinfo(title="User found",
                                       message=f"The User {key_of_banned_user} was found. You banned him in: {', '.join(value_of_banned_user)}")
            else:
                tk.messagebox.showerror(title="Error", message="User not found.")

        except (FileNotFoundError, json.JSONDecodeError):
            tk.messagebox.showerror(title="Error", message="No such file found")
    else:
        tk.messagebox.showerror(title="Error!", message="Please enter a Username!")


# As the second step we need to take Input of the User and store the data of the given value for later use
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Let's declare a frame inside a frame which holds the labels and input fields
to_get_banned_user_information = tk.LabelFrame(frame, text="To be banned User")
to_get_banned_user_information.config(font=("Arial", 14, "bold"), bg="white")
to_get_banned_user_information.grid(row=0, column=0)

# Now let us start with the label and the input field.
platform_of_banned_user = tk.Label(to_get_banned_user_information, text="Platform")
platform_of_banned_user.config(bg="white", font=("Arial", 9, "bold"))
platform_of_banned_user_entry = tk.Entry(to_get_banned_user_information)
platform_of_banned_user.grid(row=0, column=0)
platform_of_banned_user_entry.grid(row=1, column=0)

# Now the want the User to write the Username of the banned user into an input field
username_of_banned_user = tk.Label(to_get_banned_user_information, text="Username to get banned")
username_of_banned_user.config(bg="white", font=("Arial", 9, "bold"))
username_of_banned_user_entry = tk.Entry(to_get_banned_user_information)
username_of_banned_user.grid(row=0, column=1)
username_of_banned_user_entry.grid(row=1, column=1)

# After those both input fields got filled, we need a button which calls a function to save those two values
send_data_button = tk.Button(to_get_banned_user_information, text="Send", command=banned_user_list)
send_data_button.grid(row=2, column=0, columnspan=2, sticky="ew")

# A new frame to add a searchbar and an output bar
frame1 = tk.Frame(root)
frame1.pack(pady=10, padx=10)

# A new labelframe and a label
searchbar = tk.LabelFrame(frame1, text="Search username", font=("Arial", 14, "bold"), bg="white")
search_username_label = tk.Label(searchbar, text="search username here", font=("Arial", 9, "bold"))
search_username_label.config(bg="white")
search_username_label.grid(row=0, column=0)
searchbar.grid(row=0, column=0)

# A new input field where the user writes the username of the banned one
banned_user_search = tk.Entry(searchbar)
banned_user_search.grid(row=1, column=0)

# If username was found
if_username_found = tk.Label(searchbar, text="Result: ")
if_username_found.config(bg="white", font=("Arial", 9, "bold"))
if_username_found_entry = tk.Entry(searchbar, state="disabled")
if_username_found.grid(row=0, column=1)
if_username_found_entry.grid(row=1, column=1)

# A button to send the searched username
send_searched_username_button = tk.Button(searchbar, text="send", command=user_banned_or_not)
send_searched_username_button.grid(row=2, column=0, columnspan=2, sticky="ew")

# Let us add some padding
for widget in to_get_banned_user_information.winfo_children():
    widget.grid_configure(padx=5, pady=5)

for widget in searchbar.winfo_children():
    widget.grid_configure(padx=5, pady=5)

# the mainloop (almost forgot)
root.mainloop()