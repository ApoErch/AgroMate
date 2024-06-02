import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk
import json
import os
from tkcalendar import DateEntry
from datetime import date, datetime, timedelta

class Fertilization(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.geometry("650x450")
        self.configure(bg="#2E2E2E")
        self.title("Fertilization")
        self.main_menu_frame = tk.Frame(self, bg="#2E2E2E")
        self.main_menu_frame.pack(expand=True, fill=tk.BOTH)

        # Cultivation history and fertilizer data
        self.cult_history = {}
        self.fert_data = []

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
        for widget in self.winfo_children():
            widget.destroy()
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
                self.cult_history = json.load(file)
                for field, details in self.cult_history.items():
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
                self.fert_data = json.load(file)
                self.fert_tree.delete(*self.fert_tree.get_children())  # Clear existing rows
                for fert in self.fert_data:
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
        # Get selected items from tree
        selected_fields = [self.tree.item(item, "values") for item in self.tree.selection()]
        
        # Get selected items from fert_tree
        selected_fertilizers = [self.fert_tree.item(item, "values") for item in self.fert_tree.selection()]

        # Combine the selected data
        combined_data = {
            "selected_fields": selected_fields,
            "selected_fertilizers": selected_fertilizers
        }

        # Save the combined data to a single JSON file
        with open("backup_data.json", "w") as file:
            json.dump(combined_data, file, indent=4)

        messagebox.showinfo("Info", "Selected data saved successfully!")

        self.fert_frame.destroy()
        self.form_frame = tk.Frame(self, bg="#2E2E2E")
        self.form_frame.pack(expand=True, fill=tk.BOTH)

        # Create a frame to hold the back button
        self.button_frame_top = tk.Frame(self.form_frame, bg="#2E2E2E")
        self.button_frame_top.pack(fill=tk.X, padx=(10, 10))

        # Back button
        self.back_button = ctk.CTkButton(
            self.button_frame_top, text="Back", command=self.back_to_fert_menu,
            fg_color="#2E2E2E", border_width=2, border_color="#00FF00",
            text_color="#00FF00", corner_radius=8, width=40, height=30,
            hover_color="#FFFFFF"
        )
        self.back_button.pack(side=tk.LEFT, pady=(10, 0))

        # Field label
        self.field_title = tk.Label(self.form_frame, text="Fertilization History of this Field with this Fertilizer", font=("Arial", 16), bg="#2E2E2E", fg="#00FF00")
        self.field_title.pack(pady=(10, 5), anchor='n')

        # Treeview Fertilization History of this Field with this Fertilizer
        fert_history_columns = ("Field", "Crop", "Date", "Time", "Fertilizer")
        self.fert_history_tree = ttk.Treeview(self.form_frame, columns=fert_history_columns, height=3, show='headings', style="Custom.Treeview")
        self.fert_history_tree.pack(pady=20, padx=10, expand=True, fill=tk.BOTH)
        for col in fert_history_columns:
            self.fert_history_tree.heading(col, text=col)
            self.fert_history_tree.column(col, anchor='center', width=100)

        # Create a frame to hold the date and time labels and entries
        self.date_time_frame = tk.Frame(self.form_frame, bg="#2E2E2E")
        self.date_time_frame.pack(pady=(10, 5))

        label_width = 30

        # Label and DateEntry for Date
        self.date_label = tk.Label(self.date_time_frame, text="Date:", font=("Arial", 12), bg="#2E2E2E", fg="#00FF00", width=label_width, anchor='w')
        self.date_label.grid(row=0, column=0, padx=(0, 10), pady=(0, 5))
        self.date_entry = DateEntry(self.date_time_frame, font=("Arial", 12), date_pattern='yyyy-mm-dd', mindate=date.today(), width=10, state='readonly')
        self.date_entry.grid(row=0, column=1, pady=(0, 5))

        # Calculate the next closest hour
        now = datetime.now()
        next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        closest_time = f"{next_hour.hour:02}:00"

        # Label and Entry for Time
        self.time_label = tk.Label(self.date_time_frame, text="Time:", font=("Arial", 12), bg="#2E2E2E", fg="#00FF00", width=label_width, anchor='w')
        self.time_label.grid(row=1, column=0, padx=(0, 10))
        self.time_entry = ttk.Combobox(self.date_time_frame, font=("Arial", 12), values=[f"{hour:02}:00" for hour in range(24)], width=10, state='readonly')
        self.time_entry.grid(row=1, column=1)
        self.time_entry.set(closest_time)

        # Label and Entry for Duration
        self.duration_label = tk.Label(self.date_time_frame, text="Duration:", font=("Arial", 12), bg="#2E2E2E", fg="#00FF00", width=label_width, anchor='w')
        self.duration_label.grid(row=2, column=0, padx=(0, 10), pady=(5, 0))
        self.duration_entry = ttk.Combobox(self.date_time_frame, font=("Arial", 12), values=["30", "60", "90", "120", "150"], width=10, state='readonly')
        self.duration_entry.grid(row=2, column=1, pady=(5, 0))
        self.duration_entry.current(0)

        # Label and Entry for Weight
        self.weight_label = tk.Label(self.date_time_frame, text="Weight (up to 100kg):", font=("Arial", 12), bg="#2E2E2E", fg="#00FF00", width=label_width, anchor='w')
        self.weight_label.grid(row=3, column=0, padx=(0, 10), pady=(5, 0))
        self.weight_entry = tk.Entry(self.date_time_frame, font=("Arial", 12), width=13)  # Same width as duration_entry
        self.weight_entry.grid(row=3, column=1, pady=(5, 0))
        self.weight_entry.bind('<KeyRelease>', self.validate_weight)

        # Label and Entry for WWR (Weight/Water Ratio)
        self.wwr_label = tk.Label(self.date_time_frame, text="Weight/Water Ratio (up to 30%):", font=("Arial", 12), bg="#2E2E2E", fg="#00FF00", width=label_width, anchor='w')
        self.wwr_label.grid(row=4, column=0, padx=(0, 10), pady=(5, 0))
        self.wwr_entry = tk.Entry(self.date_time_frame, font=("Arial", 12), width=13)  # Same width as duration_entry
        self.wwr_entry.grid(row=4, column=1, pady=(5, 0))
        self.wwr_entry.bind('<KeyRelease>', self.validate_wwr)

        # Check Form Button
        self.check_form_button = ctk.CTkButton(
            self.date_time_frame, text="Check Form", command=self.check_form,
            fg_color="#2E2E2E", border_width=2, border_color="#00FF00",
            text_color="#00FF00", corner_radius=8, width=120, height=30,
            hover_color="#FFFFFF"
        )
        self.check_form_button.grid(row=5, column=0, columnspan=2, pady=(10, 0))

    def validate_weight(self, event):
        value = self.weight_entry.get()
        if not value.isdigit() or int(value) > 100:
            self.weight_entry.delete(0, tk.END)
            self.weight_entry.insert(0, ''.join(filter(str.isdigit, value))[:3])
            if int(self.weight_entry.get() or 0) > 100:
                self.weight_entry.delete(2, tk.END)

    def validate_wwr(self, event):
        value = self.wwr_entry.get()
        if not value.isdigit() or int(value) > 30:
            self.wwr_entry.delete(0, tk.END)
            self.wwr_entry.insert(0, ''.join(filter(str.isdigit, value))[:2])
            if int(self.wwr_entry.get() or 0) > 30:
                self.wwr_entry.delete(1, tk.END)

    def check_form(self):
        weight = int(self.weight_entry.get())
        try:
            with open("backup_data.json", "r") as file:
                backup_data = json.load(file)
                selected_fertilizers = backup_data["selected_fertilizers"]
                if selected_fertilizers:
                    selected_fertilizer = selected_fertilizers[0]
                    stock = int(selected_fertilizer[1])  # Assuming stock is the second value in the list
                    if weight > stock:
                        messagebox.showerror("Error", f"The weight exceeds the available stock. Available stock: {stock} kg.")
                    else:
                        messagebox.showinfo("Success", "The weight is within the available stock.")
                else:
                    messagebox.showerror("Error", "No fertilizer selected.")
        except FileNotFoundError:
            messagebox.showerror("Error", "The backup data file was not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error decoding the backup data file.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def back_to_fert_menu(self):
        if os.path.exists("backup_data.json"):
            os.remove("backup_data.json")

        self.form_frame.destroy()
        self.fert_menu(self)

    def show_filter(self):
        # Implement the logic for the filter functionality
        messagebox.showinfo("Info", "Filter button clicked!")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    app = Fertilization(root)
    app.mainloop()
