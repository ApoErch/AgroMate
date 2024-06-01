import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
from customtkinter import CTkButton

# Path to the credentials file
CREDENTIALS_FILE = "credentials.json"
# Path to the user availabilities file
USER_AVAILABILITIES_FILE = "user_availabilities.json"

# Load credentials from file
def load_credentials():
    try:
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Load user availabilities from file
def load_user_availabilities():
    try:
        with open(USER_AVAILABILITIES_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save user availabilities to file
def save_user_availabilities(availabilities):
    with open(USER_AVAILABILITIES_FILE, "w") as file:
        json.dump(availabilities, file, indent=4)

# Dictionary to store user credentials
user_credentials = load_credentials()
# Dictionary to store user availabilities
user_availabilities = load_user_availabilities()

class ExperimentParticipationPage(tk.Frame):
    def __init__(self, parent, email=None):
        super().__init__(parent, bg="#2E2E2E")
        self.parent = parent
        self.email = email if email else parent.current_user_email  # Use parent's email if not provided
        self.setup_ui()

    def setup_ui(self):
        label = tk.Label(self, text="Experiment Participation Page", font=("Helvetica", 16), bg="#2E2E2E", fg="#00FF00")
        label.pack(pady=20)

        start_date_label = tk.Label(self, text="Start Date:", bg="#2E2E2E", fg="#00FF00")
        start_date_label.pack()
        self.start_calendar = DateEntry(self, selectmode="day", year=2024, month=5, day=20, date_pattern="yyyy-mm-dd")
        self.start_calendar.pack()

        end_date_label = tk.Label(self, text="End Date:", bg="#2E2E2E", fg="#00FF00")
        end_date_label.pack()
        self.end_calendar = DateEntry(self, selectmode="day", year=2024, month=5, day=20, date_pattern="yyyy-mm-dd")
        self.end_calendar.pack()

        save_button = CTkButton(self, text="Save Availability", command=self.save_availability, fg_color="#2E2E2E", border_width=2,
                                border_color="#00FF00", text_color="#00FF00", corner_radius=8, width=200, height=40,
                                hover_color="#FFFFFF")
        save_button.pack(pady=(20, 10))

        back_button = CTkButton(self, text="Back", command=self.parent.show_main_page, fg_color="#2E2E2E", border_width=2,
                                border_color="#00FF00", text_color="#00FF00", corner_radius=8, width=200, height=40,
                                hover_color="#FFFFFF")
        back_button.pack(pady=(10, 10))

    def save_availability(self):
        start_date = self.start_calendar.get_date()
        end_date = self.end_calendar.get_date()
    
        # Validate dates
        if start_date > end_date:
            messagebox.showerror("Error", "End date cannot be before start date.")
            return

        # Check if description is empty
        if not start_date or not end_date:
            messagebox.showerror("Error", "Please select both start and end dates.")
            return

        # Retrieve last name of the user from credentials
        last_name = user_credentials[self.email]["last_name"]

        # Load existing availabilities from file
        try:
            with open("user_availabilities.json", "r") as file:
                availabilities = json.load(file)
        except FileNotFoundError:
            availabilities = {}

        # Update or add availability for the current user
        if last_name in availabilities:
            # If last name exists, update availability
            availabilities[last_name].append({"start_date": str(start_date), "end_date": str(end_date)})
        else:
            # If last name doesn't exist, create a new entry
            availabilities[last_name] = [{"start_date": str(start_date), "end_date": str(end_date)}]

        # Save updated availabilities back to file
        with open("user_availabilities.json", "w") as file:
            json.dump(availabilities, file, indent=4)

        messagebox.showinfo("Success", f"Availability saved from {start_date} to {end_date} for user {last_name}")


class MainPage(tk.Frame):
    def __init__(self, parent, show_login, show_signup):
        super().__init__(parent, bg="#2E2E2E")
        self.parent = parent
        self.show_login = show_login
        self.show_signup = show_signup

        self.setup_ui()

    def setup_ui(self):
        experiment_button = tk.Button(self, text="Experiment Participation", command=self.show_experiment_participation)
        experiment_button.pack(pady=(20, 10))

    def show_experiment_participation(self):
        email = self.parent.current_user_email
        if email:
            self.parent.show_frame(lambda parent: ExperimentParticipationPage(parent, email))  # Pass 'email' argument
        else:
            messagebox.showinfo("Error", "Please login first.")

class LoginPage(tk.Frame):
    def __init__(self, parent, show_main_menu, show_main_page):
        frame = tk.Frame(parent, bg="#2E2E2E")
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Email:", background="#2E2E2E", foreground="#00FF00").pack(pady=(50, 0))
        email_entry = ttk.Entry(frame)
        email_entry.pack(pady=10)

        ttk.Label(frame, text="Password:", background="#2E2E2E", foreground="#00FF00").pack(pady=(20, 0))
        password_entry = ttk.Entry(frame, show="*")
        password_entry.pack(pady=10)

        def authenticate():
            email = email_entry.get()
            password = password_entry.get()
            if email in user_credentials and user_credentials[email]['password'] == password:
                user_type = user_credentials[email]['type']
                if user_type == 'farmer':
                    parent.current_user_email = email
                    show_main_menu()
                else:
                    messagebox.showinfo("Error", "You are not authorized to access this menu.")
            else:
                messagebox.showerror("Error", "Invalid credentials.")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AgroMate")
        self.geometry("300x600")
        self.configure(bg="#2E2E2E")
        self.current_frame = None
        self.current_user_email = None

        self.show_main_page()

    def show_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(expand=True, fill="both")

    def show_main_page(self):
        self.show_frame(MainPage)

    def show_login_page(self):
        self.show_frame(LoginPage)


if __name__ == "__main__":
    app = App()
    app.mainloop()