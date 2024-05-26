import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import json

class ProductOrderApp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.geometry("800x600")
        self.configure(bg="#2E2E2E")
        self.parent.title("Product Order")

        # Load product data from JSON file
        with open("Project_Code_v0.1/products.json", "r") as file:
            self.product_data = json.load(file)

        # Create the main frames for the product, cart, and order history pages
        self.product_page = tk.Frame(self, bg="#2E2E2E")
        self.cart_page = tk.Frame(self, bg="#2E2E2E")
        self.order_history_page = tk.Frame(self, bg="#2E2E2E")

        # Frame to hold the top bar with cart button
        self.top_frame = tk.Frame(self.product_page, height=1000, bg="#2E2E2E")
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
        self.details_frame.pack(padx=20,pady=0)

        # Dictionary to store product images, labels, descriptions, and price widgets
        self.products = {}
        self.selected_products = []
        self.order_history = []

        # Load cart icon image
        self.cart_icon = Image.open("Project_Code_v0.1/PNGs/cart.png")
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

        # Button to confirm order
        

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
        if quantity > stock:
            messagebox.showerror("Error", f"Insufficient stock for {product_name}. Only {stock} items available.")
        else:
            # Deduct the quantity from the stock
            self.products[product_name]["stock"] -= quantity

            # Update the selected_products list
            existing_product = next((item for item in self.selected_products if item["name"] == product_name), None)
            if existing_product:
                existing_product["quantity"] += quantity
            else:
                self.selected_products.append({"name": product_name, "quantity": quantity, "price": self.products[product_name]["price"]})

            # Update the display stock
            self.update_product_display(product_name)

            # Show temporary message
            self.show_temp_message(f"Added {quantity} of {product_name} to cart")
             


    def update_product_display(self, product_name):
        stock = self.products[product_name]["stock"]
        self.products[product_name]["stock_label"].config(text=f"Stock: {stock}")

    def show_temp_message(self, message):
        self.message_label.config(text=message)
        self.parent.after(2000, lambda: self.message_label.config(text=""))

    def show_cart_page(self):
        self.product_page.pack_forget()  # Hide product page
        self.cart_page.pack(fill=tk.BOTH, expand=True)  # Show cart page
        self.update_cart_page()

    def show_product_page(self):
        self.cart_page.pack_forget()  # Hide cart page
        self.product_page.pack(fill=tk.BOTH, expand=True)  # Show product page

    def show_order_history(self):
        self.order_history_window = tk.Toplevel(self.parent)
        self.order_history_window.title("Order History")
        self.order_history_window.geometry("400x400")

        self.setup_order_history_page()

    def setup_cart_page(self):
        # Top frame for cart page
        cart_top_frame = tk.Frame(self.cart_page, height=1000, bg="#2E2E2E")
        cart_top_frame.pack(side=tk.TOP, fill=tk.X)

        # Button to go back to the product page
        back_button = ctk.CTkButton(cart_top_frame, text="Back to Products", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8,
                                command=self.show_product_page)
        back_button.pack(pady=10, padx=10, side=tk.LEFT)

        # Main frame for cart items
        self.cart_items_frame = tk.Frame(self.cart_page, bg="#2E2E2E")
        self.cart_items_frame.pack(fill=tk.BOTH, expand=True)

    def update_cart_page(self):
        # Clear the previous cart items
        for widget in self.cart_items_frame.winfo_children():
            widget.destroy()

        if not self.selected_products:
            empty_label = tk.Label(self.cart_items_frame, bg="#2E2E2E", fg="#00FF00", text="Your cart is empty.")
            empty_label.pack(pady=20)
            return

        total_price = 0

        for product in self.selected_products:
            item_frame = tk.Frame(self.cart_items_frame, bg="#2E2E2E")
            item_frame.pack(fill=tk.X, pady=5)

            name_label = tk.Label(item_frame, bg="#2E2E2E", fg="#00FF00", text=f"{product['name']} (x{product['quantity']})", font=("Arial", 12))
            name_label.pack(side=tk.LEFT, padx=10)

            price_label = tk.Label(item_frame, bg="#2E2E2E", fg="#00FF00", text=f"${product['price'] * product['quantity']:.2f}", font=("Arial", 12))
            price_label.pack(side=tk.RIGHT, padx=10)

            total_price += product['price'] * product['quantity']

        total_label = tk.Label(self.cart_items_frame, bg="#2E2E2E", fg="#00FF00", text=f"Total: ${total_price:.2f}", font=("Arial", 14, "bold"))
        total_label.pack(pady=10)

        # Confirm Order button
        confirm_button = ctk.CTkButton(self.cart_items_frame, text="Confirm Order", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8,
                                   command=self.confirm_order)
        confirm_button.pack(pady=10)
         # cancel Order button
        cancel_button = ctk.CTkButton(self.cart_items_frame, text="cancel Order", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8,
                                   command=self.cancel_order)
        cancel_button.pack(pady=10)

    def confirm_order(self):
        # Save order to order history
        if self.selected_products:
            self.order_history.append(self.selected_products.copy())
            self.selected_products.clear()
            messagebox.showinfo("Order Confirmed", "Your order has been confirmed!")
            self.show_product_page()
            self.update_cart_page()

    def cancel_order(self):
        messagebox.showinfo("Cancel", "Order canceled")
        self.show_product_page()

    def setup_order_history_page(self):
        if not self.order_history:
            empty_label = tk.Label(self.order_history_window, bg="#2E2E2E", fg="#00FF00", text="No order history available.")
            empty_label.pack(pady=20)
            return

        for order in self.order_history:
            order_frame = tk.Frame(self.order_history_window, bg="#2E2E2E")
            order_frame.pack(fill=tk.X, pady=10, padx=10, anchor="w")

            for product in order:
                product_label = tk.Label(order_frame, bg="#2E2E2E", fg="#00FF00", text=f"{product['name']} (x{product['quantity']}) - ${product['price'] * product['quantity']:.2f}")
                product_label.pack(anchor="w")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductOrderApp(root)
    root.mainloop()
