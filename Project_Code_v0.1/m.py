import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
import json
from Events_Class import Events
#from Cultivation import CultivationPage
#from New_Order import ProductOrderApp
#from aggelia import SellProductsApp
from experiment_participation import ExperimentParticipationPage
from product_review import ProductReviewApp
from experiments import ExperimentApp



# Path to the credentials file
CREDENTIALS_FILE = "credentials.json"

# Load credentials from file
def load_credentials():
    try:
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save credentials to file
def save_credentials(credentials):
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(credentials, file, indent=4)

# Dictionary to store user credentials and user types
user_credentials = load_credentials()

def switch_frame(parent, new_frame):
    if parent.current_frame is not None:
        parent.current_frame.destroy()
    parent.current_frame = new_frame
    parent.current_frame.pack(expand=True, fill="both")

def LoginPage(parent, show_main_menu, show_shop_menu, show_main_page):
    frame = tk.Frame(parent, bg="#2E2E2E")
    
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
            parent.current_user_email = email  # Store current user email
            if user_type == 'farmer':
                show_main_menu()
            else:
                show_shop_menu()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    login_button = ctk.CTkButton(frame, text="Login", command=authenticate, fg_color="#2E2E2E", border_width=2,
                                 border_color="#00FF00", text_color="#00FF00", corner_radius=8, width=200, height=40,
                                 hover_color="#FFFFFF")
    login_button.pack(pady=(20, 10))

    back_button = ctk.CTkButton(frame, text="Back", command=show_main_page, fg_color="#2E2E2E", border_width=2,
                                border_color="#00FF00", text_color="#00FF00", corner_radius=8, width=200, height=40,
                                hover_color="#FFFFFF")
    back_button.pack(pady=(10, 10))

    return frame

def SignUpPage(parent, show_login_page):
    frame = tk.Frame(parent, bg="#2E2E2E")
    
    ttk.Label(frame, text="First Name:", background="#2E2E2E", foreground="#00FF00").pack(pady=(20, 0))
    first_name_entry = ttk.Entry(frame)
    first_name_entry.pack(pady=10)

    ttk.Label(frame, text="Last Name:", background="#2E2E2E", foreground="#00FF00").pack(pady=(20, 0))
    last_name_entry = ttk.Entry(frame)
    last_name_entry.pack(pady=10)

    ttk.Label(frame, text="Email:", background="#2E2E2E", foreground="#00FF00").pack(pady=(20, 0))
    email_entry = ttk.Entry(frame)
    email_entry.pack(pady=10)

    ttk.Label(frame, text="Password:", background="#2E2E2E", foreground="#00FF00").pack(pady=(20, 0))
    password_entry = ttk.Entry(frame, show="*")
    password_entry.pack(pady=10)

    ttk.Label(frame, text="Confirm Password:", background="#2E2E2E", foreground="#00FF00").pack(pady=(20, 0))
    confirm_password_entry = ttk.Entry(frame, show="*")
    confirm_password_entry.pack(pady=10)

    farmer_var = tk.BooleanVar()
    farmer_checkbox = tk.Checkbutton(frame, text="I am a farmer", variable=farmer_var, bg="#2E2E2E",
                                     fg="#00FF00", selectcolor="#2E2E2E", activebackground="#2E2E2E",
                                     activeforeground="#00FF00")
    farmer_checkbox.pack(pady=(10, 20))

    def register():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        if password == confirm_password:
            user_credentials[email] = {'first_name': first_name, 'last_name': last_name, 'password': password, 'type': 'farmer' if farmer_var.get() else 'other'}
            save_credentials(user_credentials)
            messagebox.showinfo("Success", "Registration successful!")
            show_login_page()
        else:
            messagebox.showerror("Error", "Passwords do not match.")

    signup_button = ctk.CTkButton(frame, text="Sign Up", command=register, fg_color="#2E2E2E", border_width=2,
                                  border_color="#00FF00", text_color="#00FF00", corner_radius=8, width=200, height=40,
                                  hover_color="#FFFFFF")
    signup_button.pack(pady=(10, 20))

    back_button = ctk.CTkButton(frame, text="Back", command=show_login_page, fg_color="#2E2E2E", border_width=2,
                                border_color="#00FF00", text_color="#00FF00", corner_radius=8, width=200, height=40,
                                hover_color="#FFFFFF")
    back_button.pack(pady=(10, 10))

    return frame

def MainPage(parent, show_login, show_signup):
    frame = tk.Frame(parent, bg="#2E2E2E")
    
    # Load and resize the image
    logo = Image.open("./PNGs/logo.png")  # Path to your image file
    logo = logo.resize((210, 130), Image.LANCZOS)  # Adjust the size as needed
    logo_img = ImageTk.PhotoImage(logo)

    # Create a label to display the image
    logo_label = tk.Label(frame, image=logo_img, bg="#2E2E2E")
    logo_label.image = logo_img  # Keep a reference to avoid garbage collection
    logo_label.pack(pady=(20, 10))  # Adjust padding as needed

    login_button = ctk.CTkButton(frame, text="Login", command=show_login, fg_color="#2E2E2E", border_width=2,
                                 border_color="#00FF00", text_color="#00FF00", corner_radius=8, width=200, height=40,
                                 hover_color="#FFFFFF")
    login_button.place(relx=0.5, rely=0.5, anchor="center")

    signup_button = ctk.CTkButton(frame, text="Sign Up", command=show_signup, fg_color="#2E2E2E", border_width=2,
                                  border_color="#00FF00", text_color="#00FF00", corner_radius=8, width=200, height=40,
                                  hover_color="#FFFFFF")
    signup_button.place(relx=0.5, rely=0.7, anchor="center")

    return frame

def FarmerMainMenu(parent, show_main_page):
    frame = tk.Frame(parent, bg="#2E2E2E")
    button_style = {
        "fg_color": "#2E2E2E",
        "border_width": 2,
        "border_color": "#00FF00",
        "text_color": "#00FF00",
        "corner_radius": 8,
        "width": 200,
        "height": 40,
        "hover_color": "#FFFFFF",
    }

    #ALERT---------------------------HERE YOU WILL PUT YOUR FUNCTION CONNECTORS FOR YOUR USE CASES------------------------------
    def events():
        user_details = {
            'first_name': user_credentials[parent.current_user_email]['first_name'],
            'last_name': user_credentials[parent.current_user_email]['last_name'],
            'email': parent.current_user_email
        }
        Events(parent, user_details)  # Pass user details to Events

    def cultivation():
        CultivationPage(parent)
    
    def PlaceOrder():
        ProductOrderApp(parent)
        
    def create_ad():
        SellProductsApp(parent)
        
    def experiment_participation():
        switch_frame(parent, ExperimentParticipationPage(parent))
        
    def product_review():
        switch_frame(parent,ProductReviewApp(parent))
        

    button_texts = [
        ("Place an Order", PlaceOrder),
        ("Cultivation", cultivation),
        ("Fertilization", lambda: None),
        ("Events", events),
        ("Request for an Agronomist", lambda: None),
        ("Product Evaluation", product_review),
        ("Sell Products", create_ad),
        ("Experiment Participation", experiment_participation)
    ]

    for idx, (text, command) in enumerate(button_texts):
        button = ctk.CTkButton(frame, text=text, command=command, **button_style)
        button.place(relx=0.5, rely=(0.2 + idx * 0.1), anchor="center")

    return frame

def ShopMainMenu(parent, show_main_page):
    frame = tk.Frame(parent, bg="#2E2E2E")
    button_style = {
        "fg_color": "#2E2E2E",
        "border_width": 2,
        "border_color": "#00FF00",
        "text_color": "#00FF00",
        "corner_radius": 8,
        "width": 200,
        "height": 40,
        "hover_color": "#FFFFFF",
    }

    # Define functions for non-farmer menu options
    def pending_orders():
        pass  # Replace with actual function

    def assign_agronomist():
        pass  # Replace with actual function

    def products():
        pass  # Replace with actual function

    def service_control():
        pass  # Replace with actual function

    def information():
        pass  # Replace with actual function

    def calendar():
        pass  # Replace with actual function

    def experiments():
        switch_frame(parent, ExperimentApp(parent))

    button_texts = [
        ("Pending Orders", pending_orders),
        ("Assign Agronomist", assign_agronomist),
        ("Products", products),
        ("Service Control", service_control),
        ("Information", information),
        ("Calendar", calendar),
        ("Expirements", experiments)
    ]

    for idx, (text, command) in enumerate(button_texts):
        button = ctk.CTkButton(frame, text=text, command=command, **button_style)
        button.place(relx=0.5, rely=(0.2 + idx * 0.1), anchor="center")

    return frame

def EditProfilePage(parent):
    window = tk.Toplevel(parent)
    window.title("Edit Profile")
    window.geometry("300x300")
    window.configure(bg="#2E2E2E")

    first_name_entry = ttk.Entry(window)
    last_name_entry = ttk.Entry(window)
    email_entry = ttk.Entry(window)
    password_entry = ttk.Entry(window, show="*")
    edit_button = ctk.CTkButton(window, text="Edit", command=lambda: edit_profile(parent, window, first_name_entry, last_name_entry, email_entry, password_entry), fg_color="#2E2E2E", border_width=2,
                                border_color="#00FF00", text_color="#00FF00", corner_radius=8, width=200, height=40,
                                hover_color="#FFFFFF")

    ttk.Label(window, text="First Name:", background="#2E2E2E", foreground="#00FF00").pack()
    first_name_entry.pack()
    ttk.Label(window, text="Last Name:", background="#2E2E2E", foreground="#00FF00").pack()
    last_name_entry.pack()
    ttk.Label(window, text="Email:", background="#2E2E2E", foreground="#00FF00").pack()
    email_entry.pack()
    ttk.Label(window, text="Password:", background="#2E2E2E", foreground="#00FF00").pack()
    password_entry.pack()
    edit_button.pack()

    back_button = ctk.CTkButton(window, text="Back", command=window.destroy, fg_color="#2E2E2E", border_width=2,
                                border_color="#00FF00", text_color="#00FF00", corner_radius=8, width=200, height=40,
                                hover_color="#FFFFFF")
    back_button.pack()

    load_current_user_data(parent, first_name_entry, last_name_entry, email_entry)

def load_current_user_data(parent, first_name_entry, last_name_entry, email_entry):
    current_user_email = parent.current_user_email
    user_data = user_credentials.get(current_user_email, {})
    first_name_entry.insert(0, user_data.get("first_name", ""))
    last_name_entry.insert(0, user_data.get("last_name", ""))
    email_entry.insert(0, current_user_email)

def edit_profile(parent, window, first_name_entry, last_name_entry, email_entry, password_entry):
    current_user_email = parent.current_user_email
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    new_email = email_entry.get()
    password = password_entry.get()

    if first_name and last_name and new_email:
        user_credentials[new_email] = user_credentials.pop(current_user_email)
        user_credentials[new_email]['first_name'] = first_name
        user_credentials[new_email]['last_name'] = last_name
        if password:
            user_credentials[new_email]['password'] = password
        parent.current_user_email = new_email  # Update the current user email in the parent

        save_credentials(user_credentials)
        messagebox.showinfo("Success", "Profile updated successfully!")
        window.destroy()
    else:
        messagebox.showerror("Error", "Please fill all required fields.")

def main():
    root = tk.Tk()
    root.title("AgroMate")
    root.geometry("300x600")
    root.configure(bg="#2E2E2E")
    root.current_frame = None
    root.current_user_email = None  # Store current user email

    def show_main_page():
        switch_frame(root, MainPage(root, show_login_page, show_signup_page))

    def show_login_page():
        switch_frame(root, LoginPage(root, show_main_menu, show_shop_menu, show_main_page))

    def show_signup_page():
        switch_frame(root, SignUpPage(root, show_login_page))

    def show_main_menu():
        switch_frame(root, FarmerMainMenu(root, show_main_page))
        create_buttons()

    def show_shop_menu():
        switch_frame(root, ShopMainMenu(root, show_main_page))
        create_buttons()

    def create_buttons():
        logout_icon = ImageTk.PhotoImage(Image.open("./PNGs/logout_icon.png").resize((30, 30)))
        root.logout_button = tk.Button(root, image=logout_icon, command=logout, bg="#2E2E2E", borderwidth=0, activebackground='#2E2E2E')
        root.logout_button.image = logout_icon
        root.logout_button.place(x=10, y=10)

        settings_icon = ImageTk.PhotoImage(Image.open("./PNGs/settings_icon.png").resize((30, 30)))
        root.settings_button = tk.Button(root, image=settings_icon, command=open_settings, bg="#2E2E2E", borderwidth=0, activebackground='#2E2E2E')
        root.settings_button.image = settings_icon
        root.settings_button.place(x=260, y=10)

    def logout():
        root.current_user_email = None  # Clear current user email on logout
        show_main_page()

    def open_settings():
        EditProfilePage(root)

    show_main_page()
    root.mainloop()
    
    

if __name__ == "__main__":
    main()