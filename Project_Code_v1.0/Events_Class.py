import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk

class RejectionPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("No Events Available")
        self.geometry("400x200")
        self.configure(bg="#2E2E2E")

        tk.Label(self, text="No events available at the moment.", font=("Arial", 16), bg="#2E2E2E", fg="#FF0000").pack(pady=20)
        tk.Label(self, text="Please check back later.", font=("Arial", 12), bg="#2E2E2E", fg="#FF0000").pack(pady=10)

        close_button = ctk.CTkButton(self, text="Close", command=self.destroy, fg_color="#2E2E2E", border_width=2,
                                     border_color="#FF0000", text_color="#FF0000", corner_radius=8, width=200, height=40,
                                     hover_color="#FFFFFF")
        close_button.pack(pady=20)

class Events(tk.Toplevel):
    def __init__(self, parent, user_details):
        super().__init__(parent)
        self.parent = parent
        self.user_details = user_details
        self.BG_COLOR = "#121212"
        self.TEXT_COLOR = "#FFFFFF"
        self.BUTTON_BG_COLOR = "#4CAF50"
        self.BUTTON_TEXT_COLOR = "#FFFFFF"
        self.FarmerCalendar = {}
        self.eventsList = [
            'FarmTech Conference', '06/10/2024 11:00:00', 'Patras',
            'Sustainable Farming Field Day', '06/12/2024 14:00:00', 'Patras',
            'Precision Agriculture Expo', '06/15/2024 15:00:00', 'Athens',
            'AgroEco Conference', '06/22/2024 10:00:00', 'Thessaloniki',
            'Crop Innovation Symposium', '06/28/2024 16:00:00', 'Athens',
            'AgriConnect Expo', '06/30/2024 13:00:00', 'Thessaloniki',
            'Organic Farming Workshop', '07/05/2024 09:00:00', 'Heraklion',
            'Greenhouse Management Seminar', '07/08/2024 13:30:00', 'Athens',
            'Soil Conservation Conference', '07/12/2024 11:00:00', 'Thessaloniki',
            'Livestock Health Symposium', '07/18/2024 10:30:00', 'Patras'
        ]
        if not self.eventsList:
            self.show_rejection_page()
        else:
            self.setup_ui()

    def show_rejection_page(self):
        self.destroy()
        RejectionPage(self.parent)

    def setup_ui(self):
        self.title("Events List")
        self.geometry("600x300")
        self.configure(bg=self.BG_COLOR)

        mainframe = tk.Frame(self, bg=self.BG_COLOR, width=600, height=300)
        mainframe.place(x=0, y=0, relwidth=1, relheight=1)

        self.tree = ttk.Treeview(self, columns=("Event Name", "Date and Time", "Location"), show="headings", style='Custom.Treeview')
        self.tree.heading("Event Name", text="Event Name", anchor="center")
        self.tree.heading("Date and Time", text="Date and Time", anchor="center")
        self.tree.heading("Location", text="Location", anchor="center")
        self.tree.column("Event Name", anchor="center")
        self.tree.column("Date and Time", anchor="center")
        self.tree.column("Location", anchor="center")
        self.tree.pack(padx=1, pady=1)

        style = ttk.Style()
        style.configure("Custom.Treeview.Heading", background=self.BG_COLOR, foreground=self.BUTTON_BG_COLOR)
        style.configure("Custom.Treeview", background=self.BG_COLOR, foreground=self.BUTTON_BG_COLOR)

        for i in range(0, len(self.eventsList), 3):
            self.tree.insert("", "end", values=(self.eventsList[i], self.eventsList[i+1], self.eventsList[i+2]))

        self.tree.update_idletasks()  
        tree_height = self.tree.winfo_height()
        mainframe_height = tree_height + 100  
        mainframe.config(height=mainframe_height)

        select_button = ctk.CTkButton(mainframe, text="Select Event", command=self.select_event, fg_color=self.BUTTON_BG_COLOR, text_color=self.BUTTON_TEXT_COLOR, corner_radius=8)
        select_button.place(relx=0.2, rely=0.85, anchor="center")

        back_button = ctk.CTkButton(mainframe, text="Back", command=self.go_back, fg_color="#FE2020", text_color='white', corner_radius=8)
        back_button.place(relx=0.8, rely=0.85, anchor="center")

    def select_event(self):
        selected_item = self.tree.focus()
        if selected_item:
            item_values = self.tree.item(selected_item, 'values')
            self.register_page(item_values)
        else:
            messagebox.showerror("Error", "Please select an event.")

    def go_back(self):
        self.destroy()
        self.parent.show_main_menu()

    def register_page(self, selected_event):
        self.withdraw()
        register_root = tk.Toplevel(self)
        register_root.title("Event Registration")
        register_root.geometry("400x400")
        register_root.configure(bg=self.BG_COLOR)

        event_name, event_datetime, event_location = selected_event

        event_label = tk.Label(register_root, text=f"Event: {event_name}\nDate and Time: {event_datetime}\nLocation: {event_location}",
                               font=("Arial", 12, "bold"), bg=self.BG_COLOR, fg=self.BUTTON_BG_COLOR)
        event_label.pack(pady=10)

        first_name_label = tk.Label(register_root, text="First Name:", bg=self.BG_COLOR, fg=self.BUTTON_BG_COLOR)
        first_name_label.pack()
        first_name_entry = tk.Entry(register_root)
        first_name_entry.insert(0, self.user_details['first_name'])  # Pre-fill with user details
        first_name_entry.pack(pady=5)

        last_name_label = tk.Label(register_root, text="Last Name:", bg=self.BG_COLOR, fg=self.BUTTON_BG_COLOR)
        last_name_label.pack()
        last_name_entry = tk.Entry(register_root)
        last_name_entry.insert(0, self.user_details['last_name'])  # Pre-fill with user details
        last_name_entry.pack(pady=5)

        email_label = tk.Label(register_root, text="Email:", bg=self.BG_COLOR, fg=self.BUTTON_BG_COLOR)
        email_label.pack()
        email_entry = tk.Entry(register_root)
        email_entry.insert(0, self.user_details['email'])  # Pre-fill with user details
        email_entry.pack(pady=5)

        def register():
            if first_name_entry.get() == '' or last_name_entry.get() == '' or email_entry.get() == '':
                messagebox.showerror("Error", "Please fill in all the required fields.")
            else:
                self.FarmerCalendar[event_name] = {
                    "First Name": first_name_entry.get(),
                    "Last Name": last_name_entry.get(),
                    "Email": email_entry.get(),
                    "Event DateTime": event_datetime,
                    "Location": event_location
                }

                register_root.destroy()
                self.show_add_to_calendar_page(event_name, event_datetime, event_location)

        register_button = ctk.CTkButton(register_root, text="Register", command=register, fg_color=self.BUTTON_BG_COLOR, text_color=self.BUTTON_TEXT_COLOR, corner_radius=8)
        register_button.pack(pady=10)

        back_button = ctk.CTkButton(register_root, text="Back", command=lambda: self.back_to_events(register_root), fg_color="#FE2020", text_color='white', corner_radius=8)
        back_button.pack()

    def show_add_to_calendar_page(self, event_name, event_datetime, event_location):
        add_to_calendar_root = tk.Toplevel(self)
        add_to_calendar_root.title("Add to Calendar")
        add_to_calendar_root.geometry("400x200")
        add_to_calendar_root.configure(bg=self.BG_COLOR)

        add_label = tk.Label(add_to_calendar_root, text="Do you want to add this event to your calendar?", font=("Arial", 14), bg=self.BG_COLOR, fg=self.BUTTON_BG_COLOR)
        add_label.pack(pady=20)

        yes_button = ctk.CTkButton(add_to_calendar_root, text="Yes", command=lambda: self.confirm_add_to_calendar(add_to_calendar_root, event_name, event_datetime, event_location), fg_color=self.BUTTON_BG_COLOR, text_color=self.BUTTON_TEXT_COLOR, corner_radius=8)
        yes_button.pack(side="left", padx=20)

        no_button = ctk.CTkButton(add_to_calendar_root, text="No", command=lambda: self.invite_friends_page(add_to_calendar_root, event_name, event_datetime, event_location), fg_color="#FE2020", text_color='white', corner_radius=8)
        no_button.pack(side="right", padx=20)

    def confirm_add_to_calendar(self, root, event_name, event_datetime, event_location):
        root.destroy()
        messagebox.showinfo("Success", "Event is added to your calendar")
        self.invite_friends_page(root, event_name, event_datetime, event_location)

    def invite_friends_page(self, root, event_name, event_datetime, event_location):
        root.destroy()
        invite_root = tk.Toplevel(self)
        invite_root.title("Invite Friends")
        invite_root.geometry("600x400")
        invite_root.configure(bg=self.BG_COLOR)

        title_label = tk.Label(invite_root, text=f"Invite Friends to {event_name}", font=("Arial", 16, "bold"), bg=self.BG_COLOR, fg=self.BUTTON_BG_COLOR)
        title_label.pack(pady=10)

        friends_tree = ttk.Treeview(invite_root, columns=("Name", "Email"), show="headings", style='Custom.Treeview')
        friends_tree.heading("Name", text="Name", anchor="center")
        friends_tree.heading("Email", text="Email", anchor="center")
        friends_tree.column("Name", anchor="center")
        friends_tree.column("Email", anchor="center")
        friends_tree.pack(padx=10, pady=10)

        send_invite_button = ctk.CTkButton(invite_root, text="Send Invites", command=lambda: self.send_invites(invite_root, event_name, event_datetime, event_location, friends_tree), fg_color=self.BUTTON_BG_COLOR, text_color=self.BUTTON_TEXT_COLOR, corner_radius=8)
        send_invite_button.pack(pady=10)

        cancel_button = ctk.CTkButton(invite_root, text="Cancel", command=lambda: self.confirmation_page(invite_root, event_name, event_datetime, event_location), fg_color="#FE2020", text_color='white', corner_radius=8)
        cancel_button.pack()

        friends_list = [
            ("John Newton", "john@gmail.com"),
            ("Jane Smith", "jane@gmail.com"),
            ("Alice Johnson", "alice@gmail.com")
        ]

        for friend in friends_list:
            friends_tree.insert("", "end", values=friend)

    def send_invites(self, root, event_name, event_datetime, event_location, friends_tree):
        selected_item = friends_tree.focus()
        if selected_item:
            selected_friend = friends_tree.item(selected_item, 'values')[0]
            messagebox.showinfo("Success", f"Invitation sent to {selected_friend}!")
            self.confirmation_page(root, event_name, event_datetime, event_location)
        else:
            messagebox.showerror("Error", "Please select a friend to send the invite to.")

    def confirmation_page(self, root, event_name, event_datetime, event_location):
        root.destroy()
        confirmation_root = tk.Toplevel(self)
        confirmation_root.title("Registration Successful")
        confirmation_root.geometry("400x200")
        confirmation_root.configure(bg=self.BG_COLOR)

        confirmation_label = tk.Label(confirmation_root, text=f"Registration Successful!\n\nEvent: {event_name}\nDate and Time: {event_datetime}\nLocation: {event_location}",
                                      font=("Arial", 14), bg=self.BG_COLOR, fg=self.BUTTON_BG_COLOR)
        confirmation_label.pack(pady=20)

        done_button = ctk.CTkButton(confirmation_root, text="Done", command=lambda: self.finish_registration(confirmation_root), fg_color=self.BUTTON_BG_COLOR, text_color=self.BUTTON_TEXT_COLOR, corner_radius=8)
        done_button.pack(side="right", padx=20)

    def finish_registration(self, root):
        root.destroy()
        

    def back_to_events(self, root):
        root.destroy()
        self.deiconify()
