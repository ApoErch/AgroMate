import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk
import json

class Fertilization(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.geometry("650x450")
        self.configure(bg="#2E2E2E")
        self.title("Fertilization")
        self.main_menu_frame = tk.Frame(self, bg="#2E2E2E")
        self.main_menu_frame.pack(expand=True, fill=tk.BOTH)

        # Variable that we use to imitate the check to see if the control system is on
        self.control_system_check = 1

        # Call the cs_check method
        self.cs_check()

    def cs_check(self):
        if self.control_system_check == 1:
            # Display the GUI window (you can customize this as needed)
            self.fert_menu(self.main_menu_frame)
        else:
            # Show rejection message and return to the main menu
            messagebox.showerror("Error", "Control system is not available.")
            self.destroy()  # Close the current window

    def fert_menu(self, parent_frame):
        parent_frame.destroy()
        self.fert_frame = tk.Frame(self, bg="#2E2E2E")
        self.fert_frame.pack(expand=True, fill=tk.BOTH)

        # Create a frame to hold the back button
        self.button_frame_top = tk.Frame(self.fert_frame, bg="#2E2E2E")
        self.button_frame_top.pack(fill=tk.X, padx=(10, 10))

        # Back button
        self.back_button = ctk.CTkButton(
            self.button_frame_top, text="Back", command=self.destroy,
            fg_color="#2E2E2E", border_width=2, border_color="#00FF00",
            text_color="#00FF00", corner_radius=8, width=40, height=30,
            hover_color="#FFFFFF"
        )
        self.back_button.pack(side=tk.LEFT, pady=(10, 0))

        # Field label
        self.field_title = tk.Label(self.fert_frame, text="Select Field", font=("Arial", 16), bg="#2E2E2E", fg="#00FF00")
        self.field_title.pack(pady=(10, 5), anchor='n')

        # Treeview style
        tree_style = ttk.Style()
        tree_style.configure("Custom.Treeview.Heading", background="#2E2E2E", foreground="#00FF00", font=('Arial', 10, 'bold'))
        tree_style.configure("Custom.Treeview", background="#2E2E2E", foreground="#00FF00", fieldbackground="#2E2E2E")

        # Treeview Fields
        columns = ("field", "crop", "date")
        self.tree = ttk.Treeview(self.fert_frame, columns=columns, height=3, show='headings', style="Custom.Treeview")
        self.tree.pack(pady=20, padx=10, expand=True, fill=tk.BOTH)
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor='center')

        # Bind the selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_field_select)

        # Load fields from cultivation_history.json and populate treeview
        self.load_cultivation_history()

        # Fertilizer label
        self.fert_title = tk.Label(self.fert_frame, text="Select Fertilizer", font=("Arial", 16), bg="#2E2E2E", fg="#00FF00")
        self.fert_title.pack(pady=(10, 5), anchor='n')

        # Treeview Fertilizers
        fert_columns = ("Fertilizer", "Stock", "Max Quantity")
        self.fert_tree = ttk.Treeview(self.fert_frame, columns=fert_columns, height=3, show='headings', style="Custom.Treeview")
        self.fert_tree.pack(pady=20, padx=10, expand=True, fill=tk.BOTH)
        for col in fert_columns:
            self.fert_tree.heading(col, text=col)
            self.fert_tree.column(col, anchor='center')

        # Create a frame to hold the next and filter buttons
        self.button_frame_bottom = tk.Frame(self.fert_frame, bg="#2E2E2E")
        self.button_frame_bottom.pack(pady=20)

        # Filter button
        self.fert_filter_button = ctk.CTkButton(
            self.button_frame_bottom, text="Filter", command=self.show_filter,
            fg_color="#2E2E2E", border_width=2, border_color="#00FF00",
            text_color="#00FF00", corner_radius=8, width=40, height=30,
            hover_color="#FFFFFF"
        )
        self.fert_filter_button.pack(side=tk.LEFT, padx=10)

        # Next button
        self.next_button = ctk.CTkButton(
            self.button_frame_bottom, text="Next", command=self.show_form_page,
            fg_color="#2E2E2E", border_width=2, border_color="#00FF00",
            text_color="#00FF00", corner_radius=8, width=40, height=30,
            hover_color="#FFFFFF"
        )
        self.next_button.pack(side=tk.LEFT, padx=10)

    def load_cultivation_history(self):
        try:
            with open("cultivation_history.json", "r") as file:
                data = json.load(file)
                for field, details in data.items():
                    self.tree.insert("", "end", values=(
                        field,
                        details.get("Crop", ""),
                        details.get("Date", "")
                    ))
        except FileNotFoundError:
            messagebox.showerror("Error", "The cultivation history file was not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error decoding the cultivation history file.")

    def on_field_select(self, event):
        # Call load_all_fertilizers to refresh the fertilizers for any selected field
        self.load_all_fertilizers()

    def load_all_fertilizers(self):
        try:
            with open("fertilizers.json", "r") as file:
                data = json.load(file)
                self.fert_tree.delete(*self.fert_tree.get_children())  # Clear existing rows
                for fert in data:
                    self.fert_tree.insert("", "end", values=(
                        fert.get("Fertilizer", ""),
                        fert.get("Stock", ""),
                        fert.get("Max Quantity", "")
                    ))
        except FileNotFoundError:
            messagebox.showerror("Error", "The fertilizers file was not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error decoding the fertilizers file.")

    def show_form_page(self):
        # Implement the logic for the next page or form
        messagebox.showinfo("Info", "Next button clicked!")

    def show_filter(self):
        # Implement the logic for the filter functionality
        messagebox.showinfo("Info", "Filter button clicked!")