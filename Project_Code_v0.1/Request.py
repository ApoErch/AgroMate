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
        self.agro_request_main_frame = tk.Frame(self,bg="#2E2E2E")
        self.agro_request_main_frame.pack(expand=True, fill=tk.BOTH)
        self.agro_request_main(self.agro_request_main_frame)

    def agro_request_main(self, parent_frame):
        parent_frame.destroy()
        self.main_frame = tk.Frame(self,bg="#2E2E2E")
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        #Back Button

        #Title Label

        #Listobox

        #Label Region

        #Entry Region

        #Button Search