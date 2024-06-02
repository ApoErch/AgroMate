import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
import random

class SellProductsApp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.geometry("600x400")
        self.configure(bg="#2E2E2E")
        self.parent.title("Ads")
        self.user_ads = {}  # Dictionary to store user ads history
        self.all_ads = [
            {"product": "Apples", "price": 2.5},
            {"product": "Bananas", "price": 1.8},
            {"product": "Oranges", "price": 2.0},
            {"product": "Grapes", "price": 3.5},
            {"product": "Tomatoes", "price": 1.0}
        ]
        self.username = self.generate_random_username()
        
        self.main_menu_frame = tk.Frame(self, bg="#2E2E2E")
        self.main_menu_frame.pack(expand=True, fill=tk.BOTH)
        self.main_menu(self.main_menu_frame)

    def check_user_ads(self):
        return self.username in self.user_ads

    def save_ad(self, ad_content):
        if self.username not in self.user_ads:
            self.user_ads[self.username] = []
        self.user_ads[self.username].append(ad_content)

    def recommend_price(self, product):
        prices = [ad["price"] for ad in self.all_ads if ad["product"] == product]
        if prices:
            avg_price = sum(prices) / len(prices)
            return round(avg_price * 1.2, 2)  # Recommended price is 20% higher than average
        else:
            return None

    def generate_random_ad(self):
        products = ["Apples", "Bananas", "Oranges", "Grapes", "Tomatoes"]
        random_product = random.choice(products)
        random_price = round(random.uniform(1.0, 5.0), 2)
        return {"product": random_product, "price": random_price}

    def create_ad_form(self, parent_frame, coupon=None):
        parent_frame.destroy()
        self.ad_form_frame = tk.Frame(self, bg="#2E2E2E")
        self.ad_form_frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(self.ad_form_frame, text="Ad Name:", bg="#2E2E2E", fg="#00FF00").pack()
        self.ad_name_entry = tk.Entry(self.ad_form_frame)
        self.ad_name_entry.pack()

        tk.Label(self.ad_form_frame, text="Select Product:", bg="#2E2E2E", fg="#00FF00").pack()
        products = ["Apples", "Bananas", "Oranges", "Grapes", "Tomatoes"]
        self.product_dropdown = ttk.Combobox(self.ad_form_frame, values=products, state="readonly")
        self.product_dropdown.pack()

        tk.Label(self.ad_form_frame, text="Kilos:", bg="#2E2E2E", fg="#00FF00").pack()
        self.kilos_entry = tk.Entry(self.ad_form_frame)
        self.kilos_entry.pack()

        tk.Label(self.ad_form_frame, text="Price:", bg="#2E2E2E", fg="#00FF00").pack()
        self.price_entry = tk.Entry(self.ad_form_frame)
        self.price_entry.pack()

        ctk.CTkButton(self.ad_form_frame, text="Submit Ad", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8, command=self.submit_ad).pack(pady=10)
        # Back button to go back to main menu
        ctk.CTkButton(self.ad_form_frame, text="Back", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8, command=lambda: self.main_menu(self.ad_form_frame)).pack(pady=10)

    def submit_ad(self):
        ad_name = self.ad_name_entry.get()
        product = self.product_dropdown.get()
        kilos = self.kilos_entry.get()
        price = self.price_entry.get()

        if not ad_name or not product or not kilos or not price:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Recommend price if possible
        recommended_price = self.recommend_price(product)
        if recommended_price:
            response = messagebox.askyesno("Recommended Price", f"The recommended price for {product} is ${recommended_price}. Do you want to use this price?")
            if response:
                price = recommended_price

        ad_content = f"Ad Name: {ad_name}, Product: {product}, Kilos: {kilos}, Price: {price}"
        self.save_ad(ad_content)
        
       

        # Add the new ad to the list of all ads
        self.all_ads.append({"product": product, "price": float(price)})

        # Add a random ad to the list of all ads
        random_ad = self.generate_random_ad()
        self.all_ads.append(random_ad)

        # Check if this is the user's first ad
        if len(self.user_ads[self.username]) == 1:
            coupon_code = self.generate_coupon()
            messagebox.showinfo("Congratulations!", f"This is your first ad! Here is a coupon code for you: {coupon_code}")

        # Display the user's ad and the random ad
        self.display_ad_with_random(ad_content, random_ad)

    def display_ad_with_random(self, user_ad, random_ad):
        self.ad_form_frame.destroy()
        self.display_frame = tk.Frame(self, bg="#2E2E2E")
        self.display_frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(self.display_frame, text="Your Ad:", bg="#2E2E2E", fg="#00FF00").pack(pady=10)
        tk.Label(self.display_frame, text=user_ad, bg="#2E2E2E", fg="#00FF00").pack(pady=5)

        tk.Label(self.display_frame, text="Random Ad:", bg="#2E2E2E", fg="#00FF00").pack(pady=10)
        random_ad_text = f"Product: {random_ad['product']}, Price: ${random_ad['price']}"
        tk.Label(self.display_frame, text=random_ad_text, bg="#2E2E2E", fg="#00FF00").pack(pady=5)

        # Add public post and choose friends buttons
        ctk.CTkButton(self.display_frame, text="Public Post", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8, command=lambda: self.public_post(user_ad)).pack(pady=10)
        ctk.CTkButton(self.display_frame, text="Choose Friends",fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8, command=self.choose_friends).pack(pady=10)

        # Back button to go back to main menu
        ctk.CTkButton(self.display_frame, text="Back", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8, command=lambda: self.main_menu(self.display_frame)).pack(pady=20)

    def public_post(self, user_ad):
        self.display_frame.destroy()
        self.summary_frame = tk.Frame(self, bg="#2E2E2E")
        self.summary_frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(self.summary_frame, text="Ad Summary:", bg="#2E2E2E", fg="#00FF00").pack(pady=10)
        tk.Label(self.summary_frame, text=user_ad, bg="#2E2E2E", fg="#00FF00").pack(pady=5)

        ctk.CTkButton(self.summary_frame, text="Confirm", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8, command=lambda: self.confirm_ad(user_ad)).pack(pady=20)

    def confirm_ad(self, user_ad):
        self.save_ad(user_ad)
        messagebox.showinfo("Ad Saved", "Your ad has been saved to your history.")
        self.main_menu(self.summary_frame)

    def choose_friends(self):
        self.display_frame.destroy()
        self.friends_frame = tk.Frame(self, bg="#2E2E2E")
        self.friends_frame.pack(expand=True, fill=tk.BOTH)

        friends = ["Alice", "Bob", "Charlie", "David"]
        if friends:
            tk.Label(self.friends_frame, text="Choose Friends:", bg="#2E2E2E", fg="#00FF00").pack(pady=10)
            self.friend_listbox = tk.Listbox(self.friends_frame, selectmode=tk.MULTIPLE)
            for friend in friends:
                self.friend_listbox.insert(tk.END, friend)
            self.friend_listbox.pack(pady=5)
            ctk.CTkButton(self.friends_frame, text="Send Ad", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8, command=self.send_ad_to_friends).pack(pady=10)
        else:
            tk.Label(self.friends_frame, text="No friends available.", bg="#2E2E2E", fg="#00FF00").pack(pady=10)

        ctk.CTkButton(self.friends_frame, text="Back", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8, command=lambda: self.main_menu(self.friends_frame)).pack(pady=20)

    def send_ad_to_friends(self):
        selected_friends = [self.friend_listbox.get(i) for i in self.friend_listbox.curselection()]
        if selected_friends:
            messagebox.showinfo("Ad Sent", f"Your ad has been sent to: {', '.join(selected_friends)}")
        else:
            messagebox.showwarning("No Friends Selected", "Please select at least one friend.")
        self.main_menu(self.friends_frame)

        
    def display_ad_history(self, parent_frame):
        parent_frame.destroy()
        self.ad_history_frame = tk.Frame(self, bg="#2E2E2E")
        self.ad_history_frame.pack(expand=True, fill=tk.BOTH)

        if self.check_user_ads():
            ad_list_label = tk.Label(self.ad_history_frame, text="Your Ad History:", bg="#2E2E2E", fg="#00FF00")
            ad_list_label.pack()

            for ad in self.user_ads[self.username]:
                tk.Label(self.ad_history_frame, text=ad, bg="#2E2E2E", fg="#00FF00").pack()
        else:
            tk.Label(self.ad_history_frame, text="No ads created yet.", bg="#2E2E2E", fg="#00FF00").pack()

        # Back button to go back to main menu
        ctk.CTkButton(self.ad_history_frame, text="Back", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8, command=lambda: self.main_menu(self.ad_history_frame)).pack(side=tk.TOP, anchor=tk.NE)

    def main_menu(self, parent_frame):
        parent_frame.destroy()
        self.main_frame = tk.Frame(self, bg="#2E2E2E")
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(self.main_frame, text="Agromate", bg="#2E2E2E", fg="#00FF00").pack(pady=20)

        def create_ad():
            self.create_ad_form(self.main_frame)

        def check_history():
            self.display_ad_history(self.main_frame)

        # Sidebar with buttons
        sidebar_frame = tk.Frame(self.main_frame, bg="#2E2E2E", width=150)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(sidebar_frame, text="Sidebar", bg="#2E2E2E", fg="#00FF00").pack(fill=tk.X)
        ctk.CTkButton(sidebar_frame, text="Create Ad", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8, command=create_ad).pack(pady=10)
        ctk.CTkButton(sidebar_frame, text="Check History", fg_color="#00FF00", text_color="#2E2E2E", corner_radius=8, command=check_history).pack(pady=10)

        tk.Label(self.main_frame, text=f"Welcome, {self.username}!", bg="#2E2E2E", fg="#00FF00").pack(pady=20)

    def generate_random_username(self):
        adjectives = ["Cool", "Fast", "Smart", "Bright", "Brave", "Kind"]
        nouns = ["Lion", "Tiger", "Bear", "Eagle", "Shark", "Wolf"]
        return random.choice(adjectives) + random.choice(nouns) + str(random.randint(1, 100))

    def generate_coupon(self):
        return "COUPON" + str(random.randint(1000, 9999))

if __name__ == "__main__":
    root = tk.Tk()
    app = SellProductsApp(root)
    root.mainloop()
