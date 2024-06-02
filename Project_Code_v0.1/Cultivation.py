import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from tkcalendar import Calendar
import json
import os

class CultivationPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Cultivation")
        self.geometry("600x400")
        self.configure(bg="#2E2E2E")
        self.parent = parent

        # Fixed fields and crops data
        self.fields = [
            "Field A - 5 acres", "Field B - 10 acres", "Field C - 15 acres", 
            "Field D - 20 acres", "Field E - 25 acres", "Field F - 30 acres"
        ]
        self.unavailable_fields = {
            "Field C - 15 acres": "Field C is under maintenance.",
            "Field E - 25 acres": "Field E is under maintenance."
        }
        self.crops = {
            "Wheat": "Wheat is a cereal grain. It is used for making flour, bread, and pasta.",
            "Corn": "Corn is a grain plant that produces kernels on large ears. It is used as food for humans and livestock.",
            "Rice": "Rice is a staple food for over half of the world's population. It is grown in flooded fields.",
            "Soybean": "Soybean is a legume used for its protein-rich seeds. It is used in various food products.",
            "Barley": "Barley is a cereal grain used for animal feed, brewing beer, and making various food products.",
            "Oats": "Oats are used for animal feed and as a popular breakfast food in oatmeal and granola."
        }

        self.selected_field = None
        self.selected_crop = None
        self.selected_date = None
        self.field_checked = False
        self.date_checked = False

        # Load cultivation history
        self.load_cultivation_history()

        self.show_fields()

    def load_cultivation_history(self):
        global cultivation_history
        if os.path.exists("cultivation_history.json"):
            with open("cultivation_history.json", "r") as file:
                cultivation_history = json.load(file)
        else:
            cultivation_history = {}

    def show_fields(self):
        self.clear_frame()
        tk.Label(self, text="Select a Field for Cultivation", font=("Arial", 16), bg="#2E2E2E", fg="#00FF00").pack(pady=10)
        
        fields_frame = tk.Frame(self, bg="#2E2E2E")
        fields_frame.pack(pady=10)
        
        self.field_var = tk.StringVar(value="Select a field")
        field_dropdown = ttk.Combobox(fields_frame, textvariable=self.field_var, values=self.fields, state="readonly")
        field_dropdown.pack(pady=5)
        
        check_button = ctk.CTkButton(fields_frame, text="Check Availability", command=self.check_field_availability, fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8)
        check_button.pack(pady=10)

        self.confirm_field_button = ctk.CTkButton(fields_frame, text="Confirm Field", command=self.confirm_field, fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8, state="disabled")
        self.confirm_field_button.pack(pady=10)
        
        back_button = ctk.CTkButton(self, text="Back", command=self.destroy, fg_color="#FE2020", text_color="white", corner_radius=8)
        back_button.pack(pady=20)

    def check_field_availability(self):
        self.selected_field = self.field_var.get()
        if self.selected_field == "Select a field":
            messagebox.showerror("Error", "Please select a field.")
            return

        # Check if the field is unavailable for a predefined reason
        if self.selected_field in self.unavailable_fields:
            reason = self.unavailable_fields[self.selected_field]
            messagebox.showerror("Unavailable", f"The selected field is not available for cultivation. Reason: {reason}")
            self.field_checked = False
            self.confirm_field_button.configure(state="disabled")
            return

        messagebox.showinfo("Available", "The selected field is available for cultivation.")
        self.field_checked = True
        self.confirm_field_button.configure(state="normal")

    def confirm_field(self):
        if self.field_checked:
            self.select_crop()
        else:
            messagebox.showerror("Error", "Please check the field availability first.")

    def select_crop(self):
        self.clear_frame()
        tk.Label(self, text="Select a Crop for Cultivation", font=("Arial", 16), bg="#2E2E2E", fg="#00FF00").pack(pady=10)
        
        crops_frame = tk.Frame(self, bg="#2E2E2E")
        crops_frame.pack(pady=10)
        
        self.crop_var = tk.StringVar(value="Select a crop")
        crop_dropdown = ttk.Combobox(crops_frame, textvariable=self.crop_var, values=list(self.crops.keys()), state="readonly")
        crop_dropdown.pack(pady=5)
        
        crop_dropdown.bind("<<ComboboxSelected>>", self.show_crop_info)
        
        self.crop_info_label = tk.Label(crops_frame, text="", font=("Arial", 12), bg="#2E2E2E", fg="#00FF00", wraplength=500)
        self.crop_info_label.pack(pady=5)

        confirm_button = ctk.CTkButton(crops_frame, text="Confirm", command=self.confirm_crop, fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8)
        confirm_button.pack(pady=10)
        
        back_button = ctk.CTkButton(self, text="Back", command=self.show_fields, fg_color="#FE2020", text_color="white", corner_radius=8)
        back_button.pack(pady=20)

    def show_crop_info(self, event):
        selected_crop = self.crop_var.get()
        if selected_crop in self.crops:
            self.crop_info_label.config(text=self.crops[selected_crop])

    def confirm_crop(self):
        self.selected_crop = self.crop_var.get()
        if self.selected_crop == "Select a crop":
            messagebox.showerror("Error", "Please select a crop.")
            return

        self.show_cultivation_date()

    def show_cultivation_date(self):
        self.clear_frame()
        self.geometry("600x500")  # Increase the height of the window
        tk.Label(self, text="Cultivation Date", font=("Arial", 16), bg="#2E2E2E", fg="#00FF00").pack(pady=10)
        
        date_frame = tk.Frame(self, bg="#2E2E2E")
        date_frame.pack(pady=10)
        
        tk.Label(date_frame, text=f"Field: {self.selected_field}", font=("Arial", 12), bg="#2E2E2E", fg="#00FF00").pack(pady=5)
        tk.Label(date_frame, text=f"Crop: {self.selected_crop}", font=("Arial", 12), bg="#2E2E2E", fg="#00FF00").pack(pady=5)
        
        tk.Label(date_frame, text="Select Date:", font=("Arial", 12), bg="#2E2E2E", fg="#00FF00").pack(pady=5)
        
        self.calendar = Calendar(date_frame, selectmode="day", year=2024, month=6, day=1)
        self.calendar.pack(pady=10)
        
        check_date_button = ctk.CTkButton(date_frame, text="Check Date Availability", command=self.check_date_availability, fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8)
        check_date_button.pack(pady=10)

        self.confirm_date_button = ctk.CTkButton(date_frame, text="Confirm Date", command=self.confirm_date, fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8, state="disabled")
        self.confirm_date_button.pack(pady=10)
        
        back_button = ctk.CTkButton(self, text="Back", command=self.select_crop, fg_color="#FE2020", text_color="white", corner_radius=8)
        back_button.pack(pady=20)

    def check_date_availability(self):
        self.selected_date = self.calendar.get_date()
        # Check if the field is available on the selected date
        key = f"{self.selected_field} {self.selected_date}"
        if key in cultivation_history:
            messagebox.showerror("Unavailable", f"The selected date {self.selected_date} is not available for cultivation in {self.selected_field}. Please choose another date or field.")
            self.date_checked = False
            self.confirm_date_button.configure(state="disabled")
        else:
            messagebox.showinfo("Available", f"The selected date {self.selected_date} is available for cultivation in {self.selected_field}.")
            self.date_checked = True
            self.confirm_date_button.configure(state="normal")

    def confirm_date(self):
        if self.date_checked:
            self.show_cultivation_plan()
        else:
            messagebox.showerror("Error", "Please check the date availability first.")

    def show_cultivation_plan(self):
        self.clear_frame()
        tk.Label(self, text="Cultivation Plan", font=("Arial", 16), bg="#2E2E2E", fg="#00FF00").pack(pady=10)
        
        plan_frame = tk.Frame(self, bg="#2E2E2E")
        plan_frame.pack(pady=10)
        
        tk.Label(plan_frame, text=f"Field: {self.selected_field}", font=("Arial", 12), bg="#2E2E2E", fg="#00FF00").pack(pady=5)
        tk.Label(plan_frame, text=f"Crop: {self.selected_crop}", font=("Arial", 12), bg="#2E2E2E", fg="#00FF00").pack(pady=5)
        tk.Label(plan_frame, text=f"Date: {self.selected_date}", font=("Arial", 12), bg="#2E2E2E", fg="#00FF00").pack(pady=5)
        
        field_size = int(self.selected_field.split('-')[1].strip().split(" ")[0])
        self.cultivation_plan = {
            "Wheat": (field_size * 20, field_size * 2),
            "Corn": (field_size * 15, field_size * 1.5),
            "Rice": (field_size * 25, field_size * 3),
            "Soybean": (field_size * 10, field_size * 1),
            "Barley": (field_size * 18, field_size * 1.8),
            "Oats": (field_size * 12, field_size * 1.2)
        }
        
        required_crops, required_medicines = self.cultivation_plan.get(self.selected_crop, (0, 0))
        
        tk.Label(plan_frame, text=f"Required Crops: {required_crops}", font=("Arial", 12), bg="#2E2E2E", fg="#00FF00").pack(pady=5)
        tk.Label(plan_frame, text=f"Required Plant Medicines: {required_medicines}", font=("Arial", 12), bg="#2E2E2E", fg="#00FF00").pack(pady=5)
        
        confirm_button = ctk.CTkButton(plan_frame, text="Confirm Plan", command=self.confirm_plan, fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8)
        confirm_button.pack(pady=10)
        
        back_button = ctk.CTkButton(self, text="Back", command=self.show_cultivation_date, fg_color="#FE2020", text_color="white", corner_radius=8)
        back_button.pack(pady=20)

    def save_cultivation_history(self):
        with open("cultivation_history.json", "w") as file:
            json.dump(cultivation_history, file, indent=4)

    def confirm_plan(self):
        field_size = int(self.selected_field.split('-')[1].strip().split(" ")[0])
        required_crops, required_medicines = self.cultivation_plan.get(self.selected_crop, (0, 0))

        # Store cultivation data in the cultivation history
        key = f"{self.selected_field} {self.selected_date}"
        cultivation_history[key] = {
            "Field": self.selected_field,
            "Crop": self.selected_crop,
            "Date": self.selected_date,
            "Required Crops": required_crops,
            "Required Plant Medicines": required_medicines
        }
        
        self.save_cultivation_history()

        self.show_confirmation_page()

    def show_confirmation_page(self):
        self.clear_frame()
        tk.Label(self, text="Cultivation Confirmation", font=("Arial", 16), bg="#2E2E2E", fg="#00FF00").pack(pady=10)
        
        confirmation_frame = tk.Frame(self, bg="#2E2E2E")
        confirmation_frame.pack(pady=10)
        
        tk.Label(confirmation_frame, text=f"Field: {self.selected_field}", font=("Arial", 12), bg="#2E2E2E", fg="#00FF00").pack(pady=5)
        tk.Label(confirmation_frame, text=f"Crop: {self.selected_crop}", font=("Arial", 12), bg="#2E2E2E", fg="#00FF00").pack(pady=5)
        tk.Label(confirmation_frame, text=f"Date: {self.selected_date}", font=("Arial", 12), bg="#2E2E2E", fg="#00FF00").pack(pady=5)
        
        field_size = int(self.selected_field.split('-')[1].strip().split(" ")[0])
        required_crops, required_medicines = self.cultivation_plan.get(self.selected_crop, (0, 0))
        
        tk.Label(confirmation_frame, text=f"Required Crops: {required_crops}", font=("Arial", 12), bg="#2E2E2E", fg="#00FF00").pack(pady=5)
        tk.Label(confirmation_frame, text=f"Required Plant Medicines: {required_medicines}", font=("Arial", 12), bg="#2E2E2E", fg="#00FF00").pack(pady=5)
        
        tk.Label(confirmation_frame, text="Cultivation confirmed successfully!", font=("Arial", 12), bg="#2E2E2E", fg="#00FF00").pack(pady=10)
        
        close_button = ctk.CTkButton(confirmation_frame, text="Close", command=self.destroy, fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8)
        close_button.pack(pady=20)
    
    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

