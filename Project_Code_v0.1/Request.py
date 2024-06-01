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
        self.agro_request_main_frame = tk.Frame(self, bg="#2E2E2E")
        self.agro_request_main_frame.pack(expand=True, fill=tk.BOTH)
        self.agro_request_main(self.agro_request_main_frame)

    def agro_request_main(self, parent_frame):
        parent_frame.destroy()
        self.main_frame = tk.Frame(self, bg="#2E2E2E")
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # CustomTkinter Back Button
        self.back_button = ctk.CTkButton(
            self.main_frame, text="Back", command=self.close_window,
            fg_color="#2E2E2E", border_width=2, border_color="#00FF00",
            text_color="#00FF00", corner_radius=8, width=40, height=30,
            hover_color="#FFFFFF"
        )
        self.back_button.pack(pady=(10, 10), padx=(10, 0), anchor='nw')

        # Title Label
        self.title_label = tk.Label(self.main_frame, text="Select Agronomist", font=("Arial", 16), bg="#2E2E2E", fg="#00FF00")
        self.title_label.pack(pady=5, anchor='n')

        # Styling Treeview
        style = ttk.Style()
        style.configure("Custom.Treeview.Heading", background="#2E2E2E", foreground="#00FF00", font=('Arial', 10, 'bold'))
        style.configure("Custom.Treeview", background="#2E2E2E", foreground="#00FF00", fieldbackground="#2E2E2E")

        # Treeview for Agronomists
        self.tree = ttk.Treeview(self.main_frame, columns=("Name", "Region"), show="headings", height=5, style="Custom.Treeview")
        self.tree.pack(pady=20, padx=10, expand=True, fill=tk.BOTH)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Region", text="Region")
        self.tree.column("Name", anchor='center')
        self.tree.column("Region", anchor='center')

        # Populate Treeview (example data)
        self.agronomists = [
            ("Cretan Cultivators", "Crete"), ("Macedonian Meadows", "Macedonia"), 
            ("Cycladic Cultures", "Cyclades"), ("Peloponnesian Planters", "Peloponnese"),
            ("Minoan Meadows", "Crete"), ("Thracian Tillers", "Thrace"), 
            ("Argolic Agro", "Peloponnese"), ("Delphic Growers", "Macedonia"), 
            ("Ionian Irrigators", "Cyclades"), ("Athenian Agrarians", "Thrace")
        ]
        for agronomist in self.agronomists:
            self.tree.insert("", tk.END, values=agronomist)

        # Label Region
        self.region_label = tk.Label(self.main_frame, text="Region:", bg="#2E2E2E", fg="#00FF00", font=("Arial", 12))
        self.region_label.pack(pady=(10, 0))

        # Entry Region
        self.region_entry = tk.Entry(self.main_frame, width=40)
        self.region_entry.pack(pady=10)

        # Button Search
        self.search_button = ctk.CTkButton(
            self.main_frame, text="Search", command=self.search_agronomist,
            fg_color="#2E2E2E", border_width=2, border_color="#00FF00",
            text_color="#00FF00", corner_radius=8, width=40, height=30,
            hover_color="#FFFFFF"
        )
        self.search_button.pack(pady=20)

    def close_window(self):
        self.destroy()

    def search_agronomist(self):
        # Clear existing entries in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get the region from the entry box
        search_region = self.region_entry.get().strip()

        # Repopulate Treeview with matching entries
        for agronomist in self.agronomists:
            if search_region.lower() in agronomist[1].lower():
                self.tree.insert("", tk.END, values=agronomist)

if __name__ == "__main__":
    root = tk.Tk()
    app = Agro_Request_Start(root)
    app.mainloop()
