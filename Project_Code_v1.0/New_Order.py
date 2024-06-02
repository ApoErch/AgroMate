import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import random

class ProductOrderApp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.geometry("800x600")
        self.configure(bg="#2E2E2E")
        self.parent.title("Product Order")

        # Load product data from JSON file
        with open("Project_Code_v1.0/products.json", "r") as file:
            self.product_data = json.load(file)

        # Create the main frames for the product, cart, and order history pages
        self.product_page = tk.Frame(self, bg="#2E2E2E")
        self.cart_page = tk.Frame(self, bg="#2E2E2E")
        self.order_history_page = tk.Frame(self, bg="#2E2E2E")
        self.delivery_collect_page = tk.Frame(self, bg="#2E2E2E")
        self.delivery_time_page = tk.Frame(self, bg="#2E2E2E")
        self.confirmation_page = tk.Frame(self, bg="#2E2E2E")

        # Frame to hold the top bar with cart button
        self.top_frame = tk.Frame(self.product_page, height=50, bg="#2E2E2E")
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        # Frame to hold category buttons (sidebar)
        self.sidebar_frame = tk.Frame(self.product_page, width=200, bg="#2E2E2E")
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Main frame to hold product images and details
        self.main_frame = tk.Frame(self.product_page, bg="#2E2E2E")
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Frame to hold product images
        self.product_frame = tk.Frame(self.main_frame, bg="#2E2E2E")
        self.product_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the product frame
        self.canvas = tk.Canvas(self.product_frame, bg="#2E2E2E")
        self.scrollbar = tk.Scrollbar(self.product_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#2E2E2E")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Frame to hold product details
        self.details_frame = tk.Frame(self.main_frame, bg="#2E2E2E")
        self.details_frame.pack(padx=20, pady=10)

        # Dictionary to store product images, labels, descriptions, and price widgets
        self.products = {}
        self.selected_products = []
        self.order_history = []

        # Load cart icon image
        self.cart_icon = Image.open("Project_Code_v1.0/PNGs/cart.png")
        self.cart_icon = self.cart_icon.resize((20, 20))
        self.cart_icon_photo = ImageTk.PhotoImage(self.cart_icon)

        # Create cart button in the top frame
        self.cart_button = ctk.CTkButton(self.top_frame, text="View Cart", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8,
                                         image=self.cart_icon_photo, compound="left", command=self.show_cart_page)
        self.cart_button.pack(pady=10, padx=10, side=tk.RIGHT)

        # Create order history button in the top frame
        self.order_history_button = ctk.CTkButton(self.top_frame, text="Order History", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8, 
                                                  command=self.show_order_history)
        self.order_history_button.pack(pady=10, padx=10, side=tk.RIGHT)

        # Create category buttons in the sidebar
        self.create_category_buttons()

        # Label to show temporary messages
        self.message_label = tk.Label(self.top_frame, bg="#2E2E2E", fg="#00FF00", font=("Arial", 10, "bold"))
        self.message_label.pack(side=tk.RIGHT, padx=10)

        # Pack the product page initially
        self.product_page.pack(fill=tk.BOTH, expand=True)

        # Cart page setup
        self.setup_cart_page()

    def create_category_buttons(self):
        for category in self.product_data.keys():
            button = ctk.CTkButton(self.sidebar_frame, text=category, fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8,
                                   command=lambda c=category: self.load_products(c))
            button.pack(pady=5, fill=tk.X)

    def load_products(self, category):
        # Clear the previous products
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        row = 0
        col = 0

        for name, data in self.product_data[category].items():
            try:
                image_path = data["image"]
                description = data["description"]
                price = data["price"]
                rating = data["rating"]

                image = Image.open(image_path)
                image = image.resize((100, 100))  # Resize to fit in the GUI
                photo = ImageTk.PhotoImage(image)

                # Create a label for each product
                label = tk.Label(self.scrollable_frame, bg="#2E2E2E", fg="#00FF00", image=photo, text=name, compound='top')
                label.image = photo  # Keep a reference to the image
                label.grid(row=row, column=col, padx=10, pady=10)

                # Display price below the product image
                price_label = tk.Label(self.scrollable_frame, bg="#2E2E2E", fg="#00FF00", text=f"${price:.2f}")
                price_label.grid(row=row+1, column=col, pady=5)

                # Display rating below the price
                rating_label = tk.Label(self.scrollable_frame, bg="#2E2E2E", fg="#00FF00", text=f"Rating: {rating:.1f}⭐")
                rating_label.grid(row=row+2, column=col, pady=5)

                # Stock label
                stock_label = tk.Label(self.scrollable_frame, bg="#2E2E2E", fg="#00FF00", text=f"Stock: {data['stock']}")
                stock_label.grid(row=row+3, column=col, pady=5)

                # Bind click event to the label
                label.bind("<Button-1>", lambda event, desc=description, prod_name=name: self.show_product_details(desc, prod_name))

                # Store in the dictionary
                self.products[name] = {"label": label, "description": description, "price": price, "rating": rating,
                                       "stock": data["stock"], "stock_label": stock_label}

                # Update column and row to ensure 3 images per row
                col += 1
                if col > 2:
                    col = 0
                    row += 4
            except Exception as e:
                print(f"Error loading image for {name}: {e}")

    def show_product_details(self, description, product_name):
        # Clear the previous details frame
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        # Product name label
        name_label = tk.Label(self.details_frame, bg="#2E2E2E", fg="#00FF00", text=product_name, font=("Arial", 16, "bold"))
        name_label.pack(pady=10)

        # Product description label
        desc_label = tk.Label(self.details_frame, bg="#2E2E2E", fg="#00FF00", text=description, wraplength=300, justify="left")
        desc_label.pack(pady=10, padx=20)

        # Quantity selection
        quantity_var = tk.IntVar(value=1)
        stock = self.products[product_name]["stock"]
        quantity_spinbox = tk.Spinbox(self.details_frame, from_=1, to=stock, textvariable=quantity_var, width=5)
        quantity_spinbox.pack(pady=5)

        # Add to Cart button with image
        add_to_cart_button = ctk.CTkButton(self.details_frame, text="Add to Cart", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8, image=self.cart_icon_photo, compound="left",
                                           command=lambda: self.add_to_cart(product_name, quantity_var))
        add_to_cart_button.pack(pady=10)

    def add_to_cart(self, product_name, quantity_var):
        quantity = quantity_var.get()
        stock = self.products[product_name]["stock"]

        if stock >= quantity:
            self.selected_products.append((product_name, quantity))
            self.products[product_name]["stock"] -= quantity
            self.products[product_name]["stock_label"].config(text=f"Stock: {self.products[product_name]['stock']}")
            self.show_message(f"Added {quantity} {product_name}(s) to cart")
        else:
            self.show_message("Insufficient stock available")

    def show_cart_page(self):
        self.product_page.pack_forget()
        self.delivery_collect_page.pack_forget()
        self.cart_page.pack(fill=tk.BOTH, expand=True)

        for widget in self.cart_page.winfo_children():
            widget.destroy()

        title_label = tk.Label(self.cart_page, text="Cart", font=("Arial", 16, "bold"), bg="#2E2E2E", fg="#00FF00")
        title_label.pack(pady=10)

        if not self.selected_products:
            empty_label = tk.Label(self.cart_page, text="Your cart is empty", bg="#2E2E2E", fg="#00FF00")
            empty_label.pack(pady=20)

        total_price = 0

        for product_name, quantity in self.selected_products:
            product = self.products[product_name]
            cart_item_label = tk.Label(self.cart_page, text=f"{product_name} - Quantity: {quantity} - ${product['price'] * quantity:.2f}",
                                   bg="#2E2E2E", fg="#00FF00")
            cart_item_label.pack(pady=5)
            total_price += product['price'] * quantity

        total_label = tk.Label(self.cart_page, text=f"Total: ${total_price:.2f}", font=("Arial", 14, "bold"), bg="#2E2E2E", fg="#00FF00")
        total_label.pack(pady=10)

        checkout_button = ctk.CTkButton(self.cart_page, text="Checkout", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8,
                                    command=self.show_delivery_collect_page)
        checkout_button.pack(pady=20)

        # Always display Back to Products button
        back_button = ctk.CTkButton(self.cart_page, text="Back to Products", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8,
                                command=self.show_product_page)
        back_button.pack(pady=10)

    def show_order_history(self):
        self.product_page.pack_forget()
        self.cart_page.pack_forget()
        self.order_history_page.pack(fill=tk.BOTH, expand=True)

        for widget in self.order_history_page.winfo_children():
            widget.destroy()

        title_label = tk.Label(self.order_history_page, text="Order History", font=("Arial", 16, "bold"), bg="#2E2E2E", fg="#00FF00")
        title_label.pack(pady=10)

        if not self.order_history:
            empty_label = tk.Label(self.order_history_page, text="You have no order history", bg="#2E2E2E", fg="#00FF00")
            empty_label.pack(pady=20)
        else:
            for order in self.order_history:
                order_label = tk.Label(self.order_history_page, text=f"Order ID: {order['order_id']} - Total: ${order['total_price']:.2f}",
                                       bg="#2E2E2E", fg="#00FF00")
                order_label.pack(pady=5)

        back_button = ctk.CTkButton(self.order_history_page, text="Back to Products", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8,
                                    command=self.show_product_page)
        back_button.pack(pady=10)

    def show_delivery_collect_page(self):
        self.cart_page.pack_forget()
        self.delivery_collect_page.pack(fill=tk.BOTH, expand=True)

        for widget in self.delivery_collect_page.winfo_children():
            widget.destroy()

        delivery_collect_label = tk.Label(self.delivery_collect_page, text="Delivery or Collection", font=("Arial", 16, "bold"), bg="#2E2E2E", fg="#00FF00")
        delivery_collect_label.pack(pady=10)

        delivery_button = ctk.CTkButton(self.delivery_collect_page, text="Delivery", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8,
                                        command=self.show_delivery_time_page)
        delivery_button.pack(pady=10)

        collection_button = ctk.CTkButton(self.delivery_collect_page, text="Collection", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8,
                                          command=lambda: self.show_confirmation_page("Collection"))
        collection_button.pack(pady=10)

        back_button = ctk.CTkButton(self.delivery_collect_page, text="Back to Cart", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8,
                                    command=self.show_cart_page)
        back_button.pack(pady=10)

    def show_delivery_time_page(self):
        self.delivery_collect_page.pack_forget()
        self.delivery_time_page.pack(fill=tk.BOTH, expand=True)

        for widget in self.delivery_time_page.winfo_children():
            widget.destroy()

        delivery_time_label = tk.Label(self.delivery_time_page, text="Select Delivery Time", font=("Arial", 16, "bold"), bg="#2E2E2E", fg="#00FF00")
        delivery_time_label.pack(pady=10)

        time_slots = ["9 AM - 12 PM", "12 PM - 3 PM", "3 PM - 6 PM", "6 PM - 9 PM"]
        self.selected_time = tk.StringVar(value=time_slots[0])

        for slot in time_slots:
            radio_button = tk.Radiobutton(self.delivery_time_page, text=slot, variable=self.selected_time, value=slot, bg="#2E2E2E", fg="#00FF00", selectcolor="#00FF00")
            radio_button.pack(pady=5)

        confirm_button = ctk.CTkButton(self.delivery_time_page, text="Confirm Delivery Time", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8,
                                       command=lambda: self.show_confirmation_page("Delivery"))
        confirm_button.pack(pady=20)

        back_button = ctk.CTkButton(self.delivery_time_page, text="Back to Delivery Options", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8,
                                    command=self.show_delivery_collect_page)
        back_button.pack(pady=10)

    def show_confirmation_page(self, delivery_method):
        self.delivery_time_page.pack_forget()
        self.confirmation_page.pack(fill=tk.BOTH, expand=True)

        for widget in self.confirmation_page.winfo_children():
            widget.destroy()

        confirmation_label = tk.Label(self.confirmation_page, text="Order Confirmation", font=("Arial", 16, "bold"), bg="#2E2E2E", fg="#00FF00")
        confirmation_label.pack(pady=10)

        if delivery_method == "Delivery":
            delivery_time = self.selected_time.get()
            delivery_label = tk.Label(self.confirmation_page, text=f"Delivery Time: {delivery_time}", bg="#2E2E2E", fg="#00FF00")
            delivery_label.pack(pady=5)

        order_id = random.randint(1000, 9999)
        total_price = sum(self.products[product_name]["price"] * quantity for product_name, quantity in self.selected_products)
        self.order_history.append({"order_id": order_id, "total_price": total_price})

        order_id_label = tk.Label(self.confirmation_page, text=f"Order ID: {order_id}", bg="#2E2E2E", fg="#00FF00")
        order_id_label.pack(pady=5)

        total_label = tk.Label(self.confirmation_page, text=f"Total Price: ${total_price:.2f}", bg="#2E2E2E", fg="#00FF00")
        total_label.pack(pady=5)

        confirm_button = ctk.CTkButton(self.confirmation_page, text="Confirm Order", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8,
                                       command=self.confirm_order)
        confirm_button.pack(pady=20)

        back_button = ctk.CTkButton(self.confirmation_page, text="Back to Products", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8,
                                    command=self.show_product_page)
        back_button.pack(pady=10)

    def confirm_order(self):
        self.selected_products.clear()
        self.show_product_page()
        self.show_message("Order confirmed successfully!")

    def show_message(self, message):
        self.message_label.config(text=message)
        self.after(3000, lambda: self.message_label.config(text=""))

    def show_product_page(self):
        self.cart_page.pack_forget()
        self.delivery_collect_page.pack_forget()
        self.delivery_time_page.pack_forget()
        self.confirmation_page.pack_forget()
        self.order_history_page.pack_forget()
        self.product_page.pack(fill=tk.BOTH, expand=True)

    def setup_cart_page(self):
        self.cart_page.configure(bg="#2E2E2E")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductOrderApp(root)
    app.mainloop()
