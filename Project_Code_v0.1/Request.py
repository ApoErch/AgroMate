import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
import json

class Agro_Request_Start(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.geometry("600x400")
        self.configure(bg="#2E2E2E")
        self.title("Agronomist Request")

        # Agronomists and shops data
        self.agronomists = [
            ("Giorgos Georgiou", "Minoan Meadows", "Yes"),
            ("Maria Marinou", "Cretan Cultivators", "No"),
            ("Nikos Nikou", "Macedonian Meadows", "Yes"),
            ("Eleni Eleniou", "Cycladic Cultures", "No")
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

        # Back button
        self.back_button = ctk.CTkButton(
            self.main_frame, text="Back", command=self.close_window,
            fg_color="#2E2E2E", border_width=2, border_color="#00FF00",
            text_color="#00FF00", corner_radius=8, width=40, height=30,
            hover_color="#FFFFFF"
        )
        self.back_button.pack(pady=(10, 10), padx=(10, 0), anchor='nw')

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

        # Populate Treeview with all agronomists for the selected shop
        for agronomist in self.agronomists:
            if agronomist[1] == selected_shop:
                self.tree_agro.insert("", tk.END, values=agronomist)

        # Filter button for showing only agronomists with "Past Consult" = "Yes"
        self.filter_button = ctk.CTkButton(
            self.agro_list_frame, text="Show Yes Only", command=self.filter_yes,
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
