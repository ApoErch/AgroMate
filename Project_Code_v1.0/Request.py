import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import json
from tkcalendar import Calendar
import datetime

class Agro_Request_Start(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.geometry("600x450")
        self.configure(bg="#2E2E2E")
        self.title("Agronomist Request")

        # Agronomists and shops data
        self.agronomists = [
            ("Giorgos Georgiou", "Minoan Meadows", "Yes"),
            ("Maria Marinou", "Cretan Cultivators", "No"),
            ("Nikos Nikou", "Macedonian Meadows", "Yes"),
            ("Eleni Eleniou", "Cycladic Cultures", "No"),
            ("Stelios Stavrou", "Cretan Cultivators", "Yes"),
            ("Ioanna Ioannou", "Macedonian Meadows", "No"),
            ("Petros Petrou", "Cycladic Cultures", "Yes"),
            ("Katerina Katerinou", "Peloponnesian Planters", "No"),
            ("Dimitris Dimitriou", "Minoan Meadows", "Yes"),
            ("Vasilis Vasilakis", "Thracian Tillers", "No"),
            ("Anna Anagnostou", "Argolic Agro", "Yes"),
            ("Nikolaos Nikolaou", "Delphic Growers", "No"),
            ("Maria Mariou", "Ionian Irrigators", "Yes"),
            ("Yiannis Ioannidis", "Athenian Agrarians", "No")
        ]
        self.shops = [
            ("Cretan Cultivators", "Crete"), ("Macedonian Meadows", "Macedonia"),
            ("Cycladic Cultures", "Cyclades"), ("Peloponnesian Planters", "Peloponnese"),
            ("Minoan Meadows", "Crete"), ("Thracian Tillers", "Thrace"),
            ("Argolic Agro", "Peloponnese"), ("Delphic Growers", "Macedonia"),
            ("Ionian Irrigators", "Cyclades"), ("Athenian Agrarians", "Thrace")
        ]

        self.agro_request_main_frame = tk.Frame(self, bg="#2E2E2E")
        self.agro_request_main_frame.pack(expand=True, fill=tk.BOTH)
        self.agro_request_main(self.agro_request_main_frame)

    def agro_request_main(self, parent_frame):
        # Main GUI setup
        parent_frame.destroy()
        self.main_frame = tk.Frame(self, bg="#2E2E2E")
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Create a frame to hold the back and pending requests buttons
        self.button_frame_top = tk.Frame(self.main_frame, bg="#2E2E2E")
        self.button_frame_top.pack(fill=tk.X, pady=(10, 10), padx=(10, 10))

        # Back button
        self.back_button = ctk.CTkButton(
            self.button_frame_top, text="Back", command=self.close_window,
            fg_color="#2E2E2E", border_width=2, border_color="#00FF00",
            text_color="#00FF00", corner_radius=8, width=40, height=30,
            hover_color="#FFFFFF"
        )
        self.back_button.pack(side=tk.LEFT)

        # Pending Requests button
        self.pending_button = ctk.CTkButton(
            self.button_frame_top, text="Pending Requests", command=self.show_pending_requests,
            fg_color="#2E2E2E", border_width=2, border_color="#00FF00",
            text_color="#00FF00", corner_radius=8, width=120, height=30,
            hover_color="#FFFFFF"
        )
        self.pending_button.pack(side=tk.RIGHT)

        # Title label
        self.title_label = tk.Label(self.main_frame, text="Select Shop", font=("Arial", 16), bg="#2E2E2E", fg="#00FF00")
        self.title_label.pack(pady=5, anchor='n')

        # Treeview style
        tree_style = ttk.Style()
        tree_style.configure("Custom.Treeview.Heading", background="#2E2E2E", foreground="#00FF00", font=('Arial', 10, 'bold'))
        tree_style.configure("Custom.Treeview", background="#2E2E2E", foreground="#00FF00", fieldbackground="#2E2E2E")

        # Treeview for displaying shops
        self.tree = ttk.Treeview(self.main_frame, columns=("Name", "Region"), show="headings", height=5, style="Custom.Treeview")
        self.tree.pack(pady=20, padx=10, expand=True, fill=tk.BOTH)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Region", text="Region")
        self.tree.column("Name", anchor='center')
        self.tree.column("Region", anchor='center')
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        for shop in self.shops:
            self.tree.insert("", tk.END, values=shop)

        # Region label and entry
        self.region_label = tk.Label(self.main_frame, text="Region:", bg="#2E2E2E", fg="#00FF00", font=("Arial", 12))
        self.region_label.pack(pady=(10, 0))

        self.region_entry = tk.Entry(self.main_frame, width=40)
        self.region_entry.pack(pady=10)

        # Search button
        self.search_button = ctk.CTkButton(
            self.main_frame, text="Search", command=self.search_shop,
            fg_color="#2E2E2E", border_width=2, border_color="#00FF00",
            text_color="#00FF00", corner_radius=8, width=40, height=30,
            hover_color="#FFFFFF"
        )
        self.search_button.pack(pady=20)

    def close_window(self):
        self.destroy()

    def search_shop(self):
        # Search functionality for shops
        for item in self.tree.get_children():
            self.tree.delete(item)
        search_region = self.region_entry.get().strip()
        for shop in self.shops:
            if search_region.lower() in shop[1].lower():
                self.tree.insert("", tk.END, values=shop)

    def on_tree_select(self, event):
        # Handle shop selection to display agronomists
        selected_item = self.tree.selection()[0]
        selected_shop = self.tree.item(selected_item)['values'][0]
        self.agro_list(self.main_frame, selected_shop)

    def agro_list(self, parent_frame, selected_shop):
        # Secondary GUI for agronomists
        parent_frame.destroy()
        self.agro_list_frame = tk.Frame(self, bg="#2E2E2E")
        self.agro_list_frame.pack(expand=True, fill=tk.BOTH)

        # Back button
        self.back_button = ctk.CTkButton(
            self.agro_list_frame, text="Back", command=lambda: self.agro_request_main(self.agro_list_frame),
            fg_color="#2E2E2E", border_width=2, border_color="#00FF00",
            text_color="#00FF00", corner_radius=8, width=40, height=30,
            hover_color="#FFFFFF"
        )
        self.back_button.pack(pady=(10, 10), padx=(10, 0), anchor='nw')

        # Agronomist list label
        self.agro_list_label = tk.Label(self.agro_list_frame, text="Select Agronomist", font=("Arial", 16), bg="#2E2E2E", fg="#00FF00")
        self.agro_list_label.pack(pady=5, anchor='n')

        # Treeview for agronomists
        self.tree_agro = ttk.Treeview(self.agro_list_frame, columns=("Name", "Shop", "Past Consult"), show="headings", height=5, style="Custom.Treeview")
        self.tree_agro.pack(pady=20, padx=10, expand=True, fill=tk.BOTH)
        self.tree_agro.heading("Name", text="Name")
        self.tree_agro.heading("Shop", text="Shop")
        self.tree_agro.heading("Past Consult", text="Past Consult")
        self.tree_agro.column("Name", anchor='center')
        self.tree_agro.column("Shop", anchor='center')
        self.tree_agro.column("Past Consult", anchor='center')
        self.tree_agro.bind("<<TreeviewSelect>>", self.show_agro_calendar)

        # Populate Treeview with all agronomists for the selected shop
        for agronomist in self.agronomists:
            if agronomist[1] == selected_shop:
                self.tree_agro.insert("", tk.END, values=agronomist)

        # Filter button for showing only agronomists with "Past Consult" = "Yes"
        self.filter_button = ctk.CTkButton(
            self.agro_list_frame, text="Past Consultants", command=self.filter_yes,
            fg_color="#2E2E2E", border_width=2, border_color="#00FF00",
            text_color="#00FF00", corner_radius=8, width=120, height=30,
            hover_color="#FFFFFF"
        )
        self.filter_button.pack(pady=20)

    def filter_yes(self):
        # Apply filter to show only agronomists with "Past Consult" = "Yes"
        for item in self.tree_agro.get_children():
            item_values = self.tree_agro.item(item, 'values')
            if item_values[2] != "Yes":
                self.tree_agro.detach(item)  # Detach the item if it does not meet the criteria

    def show_agro_calendar(self, event):
        # Show calendar in a new frame
        selected_item = self.tree_agro.selection()[0]
        self.agronomist_name = self.tree_agro.item(selected_item)['values'][0]
        self.selected_shop = self.tree_agro.item(selected_item)['values'][1]

        self.agro_list_frame.destroy()
        self.calendar_frame = tk.Frame(self, bg="#2E2E2E")
        self.calendar_frame.pack(expand=True, fill=tk.BOTH)

        # Back button
        self.back_button = ctk.CTkButton(
            self.calendar_frame, text="Back", command=lambda: self.agro_list(self.calendar_frame, self.selected_shop),
            fg_color="#2E2E2E", border_width=2, border_color="#00FF00",
            text_color="#00FF00", corner_radius=8, width=40, height=30,
            hover_color="#FFFFFF"
        )
        self.back_button.pack(pady=(10, 10), padx=(10, 0), anchor='nw')

        # Calendar label
        self.calendar_label = tk.Label(self.calendar_frame, text=f"Calendar for {self.agronomist_name}", font=("Arial", 16), bg="#2E2E2E", fg="#00FF00")
        self.calendar_label.pack(pady=5, anchor='n')

        # Calendar widget
        today = datetime.date.today()
        self.calendar = Calendar(self.calendar_frame, selectmode='day', year=today.year, month=today.month, day=today.day)
        self.calendar.pack(pady=20)
        self.calendar.calevent_create(today, 'Today', 'highlight')
        self.calendar.tag_config('highlight', background='yellow', foreground='black')

        # Time label and combobox frame
        self.time_frame = tk.Frame(self.calendar_frame, bg="#2E2E2E")
        self.time_frame.pack(pady=(10, 0))

        self.time_label = tk.Label(self.time_frame, text="Time:", bg="#2E2E2E", fg="#00FF00", font=("Arial", 11))
        self.time_label.pack(side=tk.LEFT, padx=(0, 10))

        times = [f"{hour:02}:00" for hour in range(8, 15)]
        self.time_combobox = ttk.Combobox(self.time_frame, values=times)
        self.time_combobox.pack(side=tk.LEFT)
        self.time_combobox.current(0)  # Set the default value to the first time slot

        # Description label and entry frame
        self.desc_frame = tk.Frame(self.calendar_frame, bg="#2E2E2E")
        self.desc_frame.pack(pady=10)

        self.desc_label = tk.Label(self.desc_frame, text="Short Description:", bg="#2E2E2E", fg="#00FF00", font=("Arial", 11))
        self.desc_label.pack(side=tk.LEFT, padx=(0, 10))

        self.desc_entry = tk.Entry(self.desc_frame, width=50)
        self.desc_entry.pack(side=tk.LEFT)

        # Button frame for Check and Submit buttons
        self.button_frame = tk.Frame(self.calendar_frame, bg="#2E2E2E")
        self.button_frame.pack(pady=10)

        # Check button
        self.check_button = ctk.CTkButton(
            self.button_frame, text="Check", command=self.check_time_conflict,
            fg_color="#2E2E2E", border_width=2, border_color="#00FF00",
            text_color="#00FF00", corner_radius=8, width=80, height=30,
            hover_color="#FFFFFF"
        )
        self.check_button.pack(side=tk.LEFT, padx=5)

        # Submit button
        self.submit_button = ctk.CTkButton(
            self.button_frame, text="Submit", command=self.submit_request,
            fg_color="#2E2E2E", border_width=2, border_color="#00FF00",
            text_color="#00FF00", corner_radius=8, width=80, height=30,
            hover_color="#FFFFFF"
        )
        self.submit_button.pack(side=tk.LEFT, padx=5)
        self.submit_button.configure(state=tk.DISABLED)  # Initially disable the submit button

    def check_time_conflict(self):
        selected_date = self.calendar.selection_get()
        selected_time = self.time_combobox.get()
        try:
            with open("agro_request.json", "r") as infile:
                requests = json.load(infile)
                if isinstance(requests, dict):
                    requests = [requests]  # Ensure it's a list of requests
        except FileNotFoundError:
            requests = []

        selected_datetime = datetime.datetime.combine(selected_date, datetime.datetime.strptime(selected_time, "%H:%M").time())

        for request in requests:
            if request.get('agronomist') == self.agronomist_name:
                existing_datetime = datetime.datetime.combine(
                    datetime.datetime.strptime(request['date'], "%Y-%m-%d").date(),
                    datetime.datetime.strptime(request['time'], "%H:%M").time()
                )
                if abs((existing_datetime - selected_datetime).total_seconds()) < 10800:  # 3 hours = 10800 seconds
                    messagebox.showwarning("Time Conflict", "This agronomist has another appointment within 3 hours of the selected time.")
                    self.submit_button.configure(state=tk.DISABLED)  # Disable submit button if there's a conflict
                    return

        messagebox.showinfo("No Conflict", "No time conflicts found for the selected agronomist.")
        self.submit_button.configure(state=tk.NORMAL)  # Enable submit button if no conflict

    def submit_request(self):
        selected_date = self.calendar.selection_get()
        selected_time = self.time_combobox.get()
        description = self.desc_entry.get()

        if not selected_date or not selected_time or not description:
            messagebox.showwarning("Incomplete Form", "Please fill in all fields.")
            return

        request_data = {
            "agronomist": self.agronomist_name,
            "shop": self.selected_shop,
            "date": str(selected_date),
            "time": selected_time,
            "description": description
        }

        try:
            with open("agro_request.json", "r") as infile:
                requests = json.load(infile)
                if isinstance(requests, dict):
                    requests = [requests]  # Ensure it's a list of requests
        except FileNotFoundError:
            requests = []

        requests.append(request_data)

        with open("agro_request.json", "w") as outfile:
            json.dump(requests, outfile)

        messagebox.showinfo("Request Submitted", "Your request has been submitted successfully!")
        self.close_window()

    def show_pending_requests(self):
        pending_requests_window = tk.Toplevel(self)
        pending_requests_window.geometry("600x400")
        pending_requests_window.configure(bg="#2E2E2E")
        pending_requests_window.title("Pending Requests")

        # Treeview style
        tree_style = ttk.Style()
        tree_style.configure("Custom.Treeview.Heading", background="#2E2E2E", foreground="#00FF00", font=('Arial', 10, 'bold'))
        tree_style.configure("Custom.Treeview", background="#2E2E2E", foreground="#00FF00", fieldbackground="#2E2E2E")

        # Treeview for displaying pending requests
        tree = ttk.Treeview(pending_requests_window, columns=("Agronomist", "Shop", "Date", "Time", "Description"), show="headings", height=10, style="Custom.Treeview")
        tree.pack(pady=20, padx=10, expand=True, fill=tk.BOTH)
        tree.heading("Agronomist", text="Agronomist")
        tree.heading("Shop", text="Shop")
        tree.heading("Date", text="Date")
        tree.heading("Time", text="Time")
        tree.heading("Description", text="Description")
        tree.column("Agronomist", anchor='center', width=100)
        tree.column("Shop", anchor='center', width=100)
        tree.column("Date", anchor='center', width=100)
        tree.column("Time", anchor='center', width=100)
        tree.column("Description", anchor='center', width=200)

        try:
            with open("agro_request.json", "r") as infile:
                requests = json.load(infile)
                if isinstance(requests, dict):
                    requests = [requests]  # Ensure it's a list of requests
        except FileNotFoundError:
            requests = []

        for request in requests:
            tree.insert("", tk.END, values=(request["agronomist"], request["shop"], request["date"], request["time"], request["description"]))