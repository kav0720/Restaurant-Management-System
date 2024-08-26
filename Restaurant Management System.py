import tkinter as tk
from tkinter import messagebox, ttk

class RestaurantManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Snack Attack")

        self.customer_name = tk.StringVar()
        self.customer_contact = tk.StringVar()

        self.items = {
            "🍔 Burger": 100,
            "🍕 Pizza": 200,
            "🍝 Pasta": 150,
            "🥪 Sandwich": 80,
            "🥗 Salad": 90,
            "🧋 Boba Tea": 120,
            "🥟 Korean Bao": 150,
        }

        self.orders = {}
        self.past_bills = []  # List to store past bills

        self.gst_percentage = 18

        self.create_gui()

    def create_gui(self):
        # Title with specific font, size, and style
        title_label = tk.Label(self.root, text="Snack Attack", font=("Arial", 24, "bold"), fg="green")
        title_label.pack(pady=10)

        details_frame = tk.LabelFrame(self.root, text="Customer Details", font=("Arial", 14, "bold"))
        details_frame.pack(fill="x", padx=10, pady=10)

        name_label = tk.Label(details_frame, text="Name:", font=("Arial", 12))
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(details_frame, textvariable=self.customer_name, font=("Arial", 12))
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        contact_label = tk.Label(details_frame, text="Contact:", font=("Arial", 12))
        contact_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        contact_entry = tk.Entry(details_frame, textvariable=self.customer_contact, font=("Arial", 12))
        contact_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        contact_entry.configure(validate="key")
        contact_entry.configure(validatecommand=(contact_entry.register(self.validate_contact), "%P"))

        menu_frame = tk.LabelFrame(self.root, text="Menu", font=("Arial", 14, "bold"))
        menu_frame.pack(fill="both", expand=True, padx=10, pady=10)

        item_header = tk.Label(menu_frame, text="Items", font=("Arial", 12, "bold"))
        item_header.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        quantity_header = tk.Label(menu_frame, text="Quantity", font=("Arial", 12, "bold"))
        quantity_header.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        row = 1
        for item, price in self.items.items():
            item_var = tk.IntVar()
            item_label = tk.Label(menu_frame, text=f"{item} - {self.convert_to_inr(price)}", font=("Arial", 12))
            item_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

            quantity_entry = tk.Entry(menu_frame, width=5, font=("Arial", 12))
            quantity_entry.grid(row=row, column=1, padx=5, pady=5, sticky="w")

            self.orders[item] = {"var": item_var, "quantity": quantity_entry}

            row += 1

        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(fill="x", padx=10, pady=10)

        print_bill_button = tk.Button(buttons_frame, text="Print Bill", command=self.show_bill_popup, font=("Arial", 12, "bold"))
        print_bill_button.pack(side="left", padx=5)

        past_record_button = tk.Button(buttons_frame, text="Past Records", command=self.past_records, font=("Arial", 12, "bold"))
        past_record_button.pack(side="left", padx=5)

        clear_selection_button = tk.Button(buttons_frame, text="Clear Selection", command=self.clear_selection, font=("Arial", 12, "bold"))
        clear_selection_button.pack(side="left", padx=5)

        self.sample_bill_text = tk.Text(self.root, height=10, font=("Arial", 12))
        self.sample_bill_text.pack(fill="x", padx=10, pady=10)

        # Update sample bill when quantity or item is selected
        for item, info in self.orders.items():
            info["quantity"].bind("<FocusOut>", lambda event, item=item: self.update_sample_bill(item))
            info["quantity"].bind("<Return>", lambda event, item=item: self.update_sample_bill(item))
            info["quantity"].bind("<KeyRelease>", lambda event, item=item: self.update_sample_bill(item))
            info["var"].trace("w", lambda *args, item=item: self.update_sample_bill(item))

    def show_bill_popup(self):
        # Check if customer name is provided
        if not self.customer_name.get().strip():
            self.highlight_message("Please enter customer name.")
            return

        contact = self.customer_contact.get().strip()
        if not contact or not contact.isdigit() or len(contact) != 10:
            self.highlight_message("Please enter a valid 10-digit contact number.")
            return

        selected_items = []
        total_price = 0

        for item, info in self.orders.items():
            quantity = info["quantity"].get()
            if quantity:
                selected_items.append((item, int(quantity)))
                total_price += self.items[item] * int(quantity)

        if not selected_items:
            self.highlight_message("Please select at least one item.")
            return

        gst_amount = (total_price * self.gst_percentage) / 100

        bill = f"Customer Name: {self.customer_name.get()}\n"
        bill += f"Customer Contact: {contact}\n\n"
        bill += "Selected Items:\n"
        for item, quantity in selected_items:
            bill += f"{item} x {quantity} - {self.convert_to_inr(self.items[item] * quantity)}\n"
        bill += f"\nTotal Price: {self.convert_to_inr(total_price)}\n"
        bill += f"GST ({self.gst_percentage}%): {self.convert_to_inr(gst_amount)}\n"
        bill += f"Grand Total: {self.convert_to_inr(total_price + gst_amount)}"

        self.past_bills.append(bill)  # Store the bill in past records
        messagebox.showinfo("Bill", bill)

    def past_records(self):
        if not self.past_bills:
            messagebox.showinfo("Past Records", "No past records available.")
        else:
            past_records_text = "\n\n".join(self.past_bills)
            messagebox.showinfo("Past Records", past_records_text)

    def clear_selection(self):
        for item, info in self.orders.items():
            info["var"].set(0)
            info["quantity"].delete(0, tk.END)
            

    def update_sample_bill(self, item):
        selected_items = []
        total_price = 0

        for item, info in self.orders.items():
            quantity = info["quantity"].get()
            if quantity:
                selected_items.append((item, int(quantity)))
                total_price += self.items[item] * int(quantity)

        gst_amount = (total_price * self.gst_percentage) / 100

        bill = f"Customer Name: {self.customer_name.get()}\n"
        bill += f"Customer Contact: {self.customer_contact.get()}\n\n"
        bill += "Selected Items:\n"
        for item, quantity in selected_items:
            bill += f"{item} x {quantity} - {self.convert_to_inr(self.items[item] * quantity)}\n"
        bill += f"\nTotal Price: {self.convert_to_inr(total_price)}\n"
        bill += f"GST ({self.gst_percentage}%): {self.convert_to_inr(gst_amount)}\n"
        bill += f"Grand Total: {self.convert_to_inr(total_price + gst_amount)}"

        self.sample_bill_text.delete("1.0", tk.END)  # Clear previous contents
        self.sample_bill_text.insert(tk.END, bill)

    def validate_contact(self, value):
        return value.isdigit() or value == ""

    @staticmethod
    def convert_to_inr(amount):
        return "₹" + str(amount)

    def highlight_message(self, message):
        # Create a pop-up with a colored message
        popup = tk.Toplevel(self.root)
        popup.title("Warning")
        label = tk.Label(popup, text=message, font=("Arial", 12, "bold"), fg="red")
        label.pack(padx=10, pady=10)
        ok_button = tk.Button(popup, text="OK", command=popup.destroy, font=("Arial", 12))
        ok_button.pack(pady=5)

root = tk.Tk()
restaurant_system = RestaurantManagementSystem(root)
root.mainloop()
  
