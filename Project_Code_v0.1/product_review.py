import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import customtkinter as ctk
from datetime import datetime


class StarRating(tk.Frame):
    def __init__(self, master=None, stars=5, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.stars = stars
        self.rating = 0
        self.stars_widgets = []

        for i in range(stars):
            star = tk.Canvas(self, width=30, height=30, bg="#000000", highlightthickness=0)
            star.grid(row=0, column=i, padx=2)
            star.bind("<Enter>", lambda e, index=i: self.on_hover(index))
            star.bind("<Leave>", lambda e, index=i: self.on_leave(index))
            star.bind("<Button-1>", lambda e, index=i: self.on_click(index))
            self.stars_widgets.append(star)
            self.draw_star(star, filled=False)

    def draw_star(self, canvas, filled):
        canvas.delete("all")
        color = "#00FF00" if filled else "#ffffff"
        points = [15, 0, 19, 11, 30, 11, 21, 18, 25, 29, 15, 22, 5, 29, 9, 18, 0, 11, 11, 11]
        canvas.create_polygon(points, fill=color, outline=color)

    def on_hover(self, index):
        for i in range(self.stars):
            if i <= index:
                self.draw_star(self.stars_widgets[i], filled=True)
            else:
                self.draw_star(self.stars_widgets[i], filled=False)

    def on_leave(self, index):
        for i in range(self.stars):
            if i < self.rating:
                self.draw_star(self.stars_widgets[i], filled=True)
            else:
                self.draw_star(self.stars_widgets[i], filled=False)

    def on_click(self, index):
        self.rating = index + 1
        self.on_leave(index)

    def get_rating(self):
        return self.rating


class ProductReviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Review")
        self.root.configure(bg="#2E2E2E")

        # Sample products list
        self.products = ["Tomato", "Potato", "Carrot", "Beetroot"]

        # Create buttons for each product
        self.product_buttons = []
        for product in self.products:
            button = ctk.CTkButton(root, text=product, fg_color="#2E2E2E", border_width=2,
                                   border_color="#00FF00", text_color="#00FF00", corner_radius=8, width=200, height=40,
                                   hover_color="#FFFFFF", command=lambda p=product: self.check_existing_review(p))
            button.pack(pady=5)
            self.product_buttons.append(button)

    def check_existing_review(self, product):
        if os.path.exists("reviews.json"):
            with open("reviews.json", "r") as file:
                reviews = json.load(file)
                reviewed_products = [review["product"] for review in reviews]

                if product in reviewed_products:
                    answer = messagebox.askyesno("Existing Review", f"{product} has already been reviewed. Do you want to review it again?")
                    if answer:
                        self.open_review_page(product)
                else:
                    self.open_review_page(product)
        else:
            self.open_review_page(product)

    def open_review_page(self, product):
        review_window = tk.Toplevel(self.root)
        review_window.title(f"Review for {product}")
        review_window.configure(bg="#2E2E2E")

        review_label = ttk.Label(review_window, text=f"Review for {product}:", background="#2E2E2E", foreground="#00FF00",
                                 font=('Helvetica', 14, 'bold'))
        review_label.pack(pady=10)

        # Textbox for review
        review_text = tk.Text(review_window, height=10, width=50, bg="#2E2E2E", fg="#FFFFFF", insertbackground="#FFFFFF",
                              highlightbackground="#FFFFFF", highlightcolor="#FFFFFF")
        review_text.pack(pady=10)

        # Label for rating
        rating_label = ttk.Label(review_window, text="Select a rating:", background="#2E2E2E", foreground="#00FF00",
                                 font=('Helvetica', 12, 'bold'))
        rating_label.pack(pady=10)

        # Star rating widget
        star_rating = StarRating(review_window)
        star_rating.pack(pady=10)

        # Submit button
        submit_button = ctk.CTkButton(review_window, text="Submit Review", fg_color="#2E2E2E", border_width=2,
                                      border_color="#00FF00", text_color="#00FF00", corner_radius=8, width=200, height=40,
                                      hover_color="#FFFFFF", command=lambda: self.submit_review(product, review_text, star_rating, review_window))
        submit_button.pack(pady=10)

    def submit_review(self, product, review_text, star_rating, review_window):
        review = review_text.get("1.0", tk.END).strip()
        rating = star_rating.get_rating()

        if rating == 0:
            messagebox.showwarning("No rating", "Please select a rating.")
            return

        # Save the review to a JSON file
        self.save_review(product, review, rating)

        answer = messagebox.askyesno("Review Submitted", f"Review for {product} submitted:\nRating: {'★' * rating}\nReview: {review}\n\nDo you want to post this review on the forum?")
        if answer:
            self.open_forum_post_page(product, review, rating)
        else:
            messagebox.showinfo("Operation Complete", "Review successful!")
            self.root.quit()

        # Close the review window after submission
        review_window.destroy()

    def open_forum_post_page(self, product, review, rating):
        forum_window = tk.Toplevel(self.root)
        forum_window.title(f"Forum Post for {product}")
        forum_window.configure(bg="#2E2E2E")

        post_label = ttk.Label(forum_window, text=f"Forum Post for {product}:", background="#2E2E2E", foreground="#00FF00",
                               font=('Helvetica', 14, 'bold'))
        post_label.pack(pady=10)

        # Textbox for forum post
        post_text = tk.Text(forum_window, height=10, width=50, bg="#2E2E2E", fg="#FFFFFF", insertbackground="#FFFFFF",
                            highlightbackground="#FFFFFF", highlightcolor="#FFFFFF")
        post_text.pack(pady=10)

        # Submit button
        post_button = ctk.CTkButton(forum_window, text="Post to Forum", fg_color="#2E2E2E", border_width=2,
                                    border_color="#00FF00", text_color="#00FF00", corner_radius=8, width=200, height=40,
                                    hover_color="#FFFFFF", command=lambda: self.submit_forum_post(product, review, rating, post_text.get("1.0", tk.END).strip(), forum_window))
        post_button.pack(pady=10)

    def submit_forum_post(self, product, review, rating, forum_text, forum_window):
        post_data = {
            "product": product,
            "review": review,
            "rating": rating,
            "forum_text": forum_text,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Read existing forum posts
        if os.path.exists("forum_posts.json"):
            with open("forum_posts.json", "r") as file:
                forum_posts = json.load(file)
        else:
            forum_posts = []

        # Add new post
        forum_posts.append(post_data)

        # Write updated posts back to the file
        with open("forum_posts.json", "w") as file:
            json.dump(forum_posts, file, indent=4)

        messagebox.showinfo("Forum Post Submitted", "Your review has been posted to the forum.")
        forum_window.destroy()
        messagebox.showinfo("Operation Complete", "Review successful!")
        self.root.quit()

    def save_review(self, product, review, rating):
        review_data = {
            "product": product,
            "review": review,
            "rating": rating,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Read existing reviews
        if os.path.exists("reviews.json"):
            with open("reviews.json", "r") as file:
                reviews = json.load(file)
        else:
            reviews = []

        # Add new review
        reviews.append(review_data)

        # Write updated reviews back to the file
        with open("reviews.json", "w") as file:
            json.dump(reviews, file, indent=4)


if __name__ == "__main__":
    root = ctk.CTk()
    app = ProductReviewApp(root)
    root.mainloop()