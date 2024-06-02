import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json

class Fertilization(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.geometry("600x400")
        self.configure(bg="#2E2E2E")
        self.main_menu_frame = tk.Frame(self, bg="#2E2E2E")
        self.main_menu_frame.pack(expand=True, fill=tk.BOTH)
        
        # Variable that we use to imitate the check to see if the control system is on
        self.control_system_check = 1
        
        # Call the cs_check method
        self.cs_check()

    def cs_check(self):
        if self.control_system_check == 1:
            # Display the GUI window (you can customize this as needed)
            self.fert_menu()
        else:
            # Show rejection message and return to the main menu
            messagebox.showerror("Error", "Control system is not available.")
            self.destroy()  # Close the current window

    def fert_menu(self):
        self.fert_frame = tk.Frame(self, bg="#2E2E2E")
        self.fert_frame.pack(expand=True, fill=tk.BOTH)

        # Back Button
        back_button = tk.Button(self.fert_frame, text="Back", command=self.destroy, bg="#4A4A4A", fg="#FFFFFF")
        back_button.pack(side=tk.TOP, anchor="nw", padx=10, pady=10)

        # Label Field
        label = tk.Label(self.fert_frame, text="Fertilization History", bg="#2E2E2E", fg="#FFFFFF", font=("Arial", 16))
        label.pack(pady=10)

        # Treeview
        columns = ("field", "crop", "date")
        self.tree = ttk.Treeview(self.fert_frame, columns=columns, show='headings', style="Custom.Treeview")
        self.tree.heading("field", text="Field")
        self.tree.heading("crop", text="Crop")
        self.tree.heading("date", text="Date")

        self.tree.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Style for Treeview
        style = ttk.Style()
        style.configure("Custom.Treeview", 
                        background="#2E2E2E", 
                        foreground="white", 
                        fieldbackground="#2E2E2E", 
                        bordercolor="#2E2E2E", 
                        borderwidth=0,
                        font=('Arial', 12))
        style.configure("Custom.Treeview.Heading", 
                        background="#4A4A4A", 
                        foreground="white", 
                        font=('Arial', 12, 'bold'))

        # Load fields from cultivation_history.json and populate treeview
        self.load_cultivation_history()

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
