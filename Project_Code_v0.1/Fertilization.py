import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

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
        self.cs_check(self.main_menu_frame)

    def cs_check(self, parent_frame):
        if self.control_system_check == 1:
            # Display the GUI window (you can customize this as needed)
            self.fert_menu(parent_frame)
        else:
            # Show rejection message and return to the main menu
            messagebox.showerror("Error", "Control system is not available.")
            self.destroy()  # Close the current window

    def fert_menu(self, parent_frame):
        parent_frame.destroy()
        self.fert_frame = tk.Frame(self, bg="#2E2E2E")
        self.fert_frame.pack(expand=True, fill=tk.BOTH)

        #Back Button

        #Label Field

        #Treeview Fields from cultivation_history.json

        

        