import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
import os
from datetime import date
import customtkinter as ctk


class ValidationCheck:
    def __init__(self, master=None, *args, **kwargs):
        self.master = master
        self.checks = ["Validation 1", "Validation 2", "Validation 3"]
        self.results = {}

    def perform_checks(self):
        # Load validation info from JSON file
        try:
            with open("Validations.json", "r") as file:
                validation_data = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "Validations.json file not found.")
            return {check: "Fail" for check in self.checks}

        # Check if the validation data matches the expected checks
        for check in self.checks:
            self.results[check] = "Pass" if validation_data.get(check) else "Fail"
            if self.results[check] == "Fail":
                messagebox.showerror("Validation Failed", f"Validation check '{check}' failed.")
        return self.results

class ExperimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Experiment Setup")
        self.root.configure(bg="#2E2E2E")  # Set background color to grey

        # Perform validation checks
        self.validation = ValidationCheck(self.root)
        self.validation_results = self.validation.perform_checks()

        # Display validation results
        self.display_validation_results()

        # Experiment setup button (only enabled if all validations pass)
        self.setup_button = ctk.CTkButton(root, text="Setup Experiment", fg_color="#2E2E2E", border_width=2,
                                          border_color="#00FF00", text_color="#00FF00", corner_radius=8, width=200,
                                          height=40,
                                          hover_color="#FFFFFF", command=self.setup_experiment)
        self.setup_button.pack(pady=20)
        if not all(result == "Pass" for result in self.validation_results.values()):
            self.setup_button.configure(state=tk.DISABLED)

    def display_validation_results(self):
        for check, result in self.validation_results.items():
            result_color = "#00FF00" if result == "Pass" else "#FF0000"
            result_label = ttk.Label(self.root, text=f"{check}: {result}", background="#2E2E2E",
                                     foreground=result_color,
                                     font=('Helvetica', 12, 'bold'))
            result_label.pack(pady=5)

    def setup_experiment(self):
        experiment_window = tk.Toplevel(self.root)
        experiment_window.title("Experiment Details")
        experiment_window.configure(bg="#2E2E2E")

        experiment_label = ttk.Label(experiment_window, text="Setup Your Experiment", background="#2E2E2E",
                                     foreground="#00FF00",
                                     font=('Helvetica', 14, 'bold'))
        experiment_label.pack(pady=10)

        # Textbox for experiment details
        experiment_text = tk.Text(experiment_window, height=10, width=50, bg="#2E2E2E", fg="#FFFFFF",
                                  insertbackground="#FFFFFF",
                                  highlightbackground="#FFFFFF", highlightcolor="#FFFFFF")
        experiment_text.pack(pady=10)

        # Date picker for experiment start date
        start_date_label = ttk.Label(experiment_window, text="Experiment Start Date:", background="#2E2E2E",
                                     foreground="#00FF00",
                                     font=('Helvetica', 12, 'bold'))
        start_date_label.pack(pady=5)
        self.start_date_entry = DateEntry(experiment_window, background="#2E2E2E", foreground="#FFFFFF",
                                          borderwidth=0)
        self.start_date_entry.pack(pady=5)

        # Date picker for experiment end date
        end_date_label = ttk.Label(experiment_window, text="Experiment End Date:", background="#2E2E2E",
                                   foreground="#00FF00",
                                   font=('Helvetica', 12, 'bold'))
        end_date_label.pack(pady=5)
        self.end_date_entry = DateEntry(experiment_window, background="#2E2E2E", foreground="#FFFFFF",
                                        borderwidth=0)
        self.end_date_entry.pack(pady=5)

        # Submit button
        submit_button = ctk.CTkButton(experiment_window, text="Submit Experiment", fg_color="#2E2E2E",
                                      border_width=2,
                                      border_color="#00FF00", text_color="#00FF00", corner_radius=8, width=200,
                                      height=40,
                                      hover_color="#FFFFFF",
                                      command=lambda: self.submit_experiment(experiment_text, experiment_window))
        submit_button.pack(pady=10)

    def submit_experiment(self, experiment_text, experiment_window):
        experiment_details = experiment_text.get("1.0", tk.END).strip()
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()

        # Check if experiment description is empty
        if not experiment_details:
            messagebox.showwarning("Missing Information", "Please enter experiment details.")
            return

        # Check if start date is in the past
        if start_date < date.today():
            messagebox.showwarning("Invalid Start Date", "Start date cannot be in the past.")
            return

        # Check if end date is before start date
        if end_date < start_date:
            messagebox.showwarning("Invalid End Date", "End date cannot be before start date.")
            return

        # Convert dates to string format
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")

        # Check for available farmers
        available_farmers = self.check_available_farmers(start_date_str, end_date_str)
        if not available_farmers:
            messagebox.showwarning("No Available Farmers", "No farmers are available during the specified dates.")
            return

        # Display available farmers and allow user to select
        self.display_available_farmers(experiment_window, available_farmers, experiment_details, start_date,
                                        end_date)

    def check_available_farmers(self, start_date, end_date):
        available_farmers = []
        if os.path.exists("user_availabilities.json"):
            with open("user_availabilities.json", "r") as file:
                user_availabilities = json.load(file)
                for farmer, availabilities in user_availabilities.items():
                    for availability in availabilities:
                        available_start_date = availability["start_date"]
                        available_end_date = availability["end_date"]
                        if (start_date <= available_end_date and end_date >= available_start_date):
                            available_farmers.append(farmer)
                            break
        return available_farmers

    def display_available_farmers(self, experiment_window, available_farmers, experiment_details, start_date,
                                  end_date):
        available_farmers_window = tk.Toplevel(experiment_window)
        available_farmers_window.title("Available Farmers")
        available_farmers_window.configure(bg="#2E2E2E")

        available_farmers_label = ttk.Label(available_farmers_window, text="Available Farmers", background="#2E2E2E", foreground="#00FF00", font=('Helvetica', 14, 'bold'))
        available_farmers_label.pack(pady=10)

        farmers_listbox = tk.Listbox(available_farmers_window, bg="#2E2E2E", fg="#FFFFFF",
                                      selectbackground="#00FF00", selectforeground="#2E2E2E",
                                      selectmode=tk.MULTIPLE, font=('Helvetica', 12))
        farmers_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        for farmer in available_farmers:
            farmers_listbox.insert(tk.END, farmer)

        select_button = ctk.CTkButton(available_farmers_window, text="Select Farmer", fg_color="#2E2E2E",
                                      border_width=2,
                                      border_color="#00FF00", text_color="#00FF00", corner_radius=8, width=200,
                                      height=40,
                                      hover_color="#FFFFFF",
                                      command=lambda: self.confirm_and_send_contracts(farmers_listbox,
                                                                                         available_farmers_window,
                                                                                         experiment_details,
                                                                                         start_date, end_date))
        select_button.pack(pady=10)

    def confirm_and_send_contracts(self, farmers_listbox, available_farmers_window, experiment_details, start_date,
                                   end_date):
        selected_farmers_indices = farmers_listbox.curselection()
        if not selected_farmers_indices:
            messagebox.showwarning("No Farmer Selected", "Please select at least one farmer.")
            return

        selected_farmers = [farmers_listbox.get(i) for i in selected_farmers_indices]

        confirmation = messagebox.askyesno("Confirm Contracts", "Are you sure you want to send contracts to the selected farmers?")
        if confirmation:
            for farmer in selected_farmers:
                self.send_contracts(farmer, experiment_details, start_date, end_date)
            messagebox.showinfo("Contracts Sent", "Contracts have been sent to the selected farmers.")
            available_farmers_window.destroy()
            self.root.quit()

    def send_contracts(self, farmer, experiment_details, start_date, end_date):
        contract_statement = f"This is a certificate to show that {farmer} has participated in the {experiment_details} experiment."
        contract_data = {
            "farmer_name": farmer,
            "experiment_details": experiment_details,
            "start_date": start_date.strftime("%Y-%m-%d"),  
            "end_date": end_date.strftime("%Y-%m-%d"),      
            "certificate_statement": contract_statement
        }
        directory = "experiment_contracts"
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = os.path.join(directory, f"{farmer}_contract.json")

        # Check if the JSON file already exists for the farmer
        if os.path.exists(filename):
            with open(filename, "r") as contract_file:
                existing_data = json.load(contract_file)
        else:
            existing_data = {}

        # Generate a unique key for the new experiment
        new_experiment_key = f"{experiment_details}_{start_date}_{end_date}"

        # Add the new experiment data to the existing dictionary
        existing_data[new_experiment_key] = contract_data

        # Write the updated data back to the file
        with open(filename, "w") as contract_file:
            json.dump(existing_data, contract_file, indent=4)


if __name__ == "__main__":
    root = tk.Tk()
    app = ExperimentApp(root)
    root.mainloop()