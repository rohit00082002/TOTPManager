import tkinter as tk
import json
import pyotp

class TOTPManager(tk.Tk):
    def clock_ever(self):
        self.clock_counter.set( int(self.clock_counter.get()) - 1 )
        self.update_label.after(1000, self.clock_ever)
        
        if int(self.clock_counter.get()) <= 0:
            self.table_reload()
            self.clock_counter.set("30")
    def table_reload(self):
        try:
            with open("data.json", "r") as f:
                ddt = json.load(f)
                self.table.delete(1.0, tk.END)
                # Populate the table with the JSON data
                for keyww, valueww in ddt.items():
                    vlww = pyotp.TOTP(valueww).now()
                    self.table.insert(tk.END, f"{keyww}:   {vlww}\n")
        except Exception:
            pass

    def __init__(self, data):
        super().__init__()
        self.geometry("520x330")
        self.minsize(width=520, height=330)
        self.title("TOTP Manager")
        self.data = data

        # Create a scrollable frame for the table
        scrollable_frame = tk.Frame(self)
        scrollable_frame.grid(row=0, column=0, columnspan=3, padx=20, pady=20)
        scrollbar = tk.Scrollbar(scrollable_frame, orient="vertical")
        scrollbar.grid(row=0, column=0, columnspan=3)

        # Create the table
        self.table = tk.Text(scrollable_frame, height=10, width=50, yscrollcommand=scrollbar.set, font=('Georgia 10'))
        self.table.grid(row=0, column=0, columnspan=3)
        scrollbar.config(command=self.table.yview)

        self.clock_counter = tk.StringVar()
        self.clock_counter.set("30")
        self.update_label = tk.Label(self, textvariable=self.clock_counter, fg="blue")
        self.update_label.after(1000, self.clock_ever)
        # Populate the table with the JSON data
        self.table_reload()

        # Make the table values copyable
        self.table.bind("<Button-3>", self.copy_text)
        self.clipboard = tk.StringVar()

        # Create a button to add new key-value pairs to the JSON file
        self.key_label = tk.Label(self, text="Key:", font=('Georgia 14'))
        self.key_entry = tk.Entry(self, font=('Georgia 14'))
        self.value_label = tk.Label(self, text="Value:", font=('Georgia 14'))
        self.value_entry = tk.Entry(self, font=('Georgia 14'))
        self.lbt = tk.StringVar()
        self.lbt.set("")
        self.error_label = tk.Label(self,textvariable=self.lbt , fg="red")
        self.add_button = tk.Button(self, text="Add", command=self.add_data, font=('Georgia 14'))

        # Place widgets in the window
        self.update_label.grid(row=0, column=3)
        self.error_label.grid(row=1, column=1)
        self.key_label.grid(row=2, column=0)
        self.key_entry.grid(row=2, column=1)
        self.value_label.grid(row=3, column=0)
        self.value_entry.grid(row=3, column=1)
        self.add_button.grid(row=4, column=1)

    def copy_text(self, event=None):
        """Copy the selected text to the clipboard."""
        self.clipboard.set(self.table.selection_get())
        self.table.clipboard_clear()
        self.table.clipboard_append(self.clipboard.get())

    def add_data(self):
        """Add a new key-value pair to the data and update the table and JSON file."""
        key = self.key_entry.get()
        value = self.value_entry.get()
        self.error_label = tk.Label(self, text="")

        if (not key) or (len(key.strip()) == 0) or (not value) or (len(value.strip()) <= 1):
            self.lbt.set("Key or value cannot be empty.")
            return
        
        self.lbt.set("")
        self.data[key] = value

        # Save the updated data to the JSON file
        with open('data.json', 'w') as f:
            json.dump(self.data, f, indent=2)

        self.table_reload()
try:
    with open("data.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}
except json.JSONDecodeError:
    # If the file is empty or contains invalid JSON data, insert an empty dictionary
    data = {}

# Create and run the window
window = TOTPManager(data)
window.mainloop()