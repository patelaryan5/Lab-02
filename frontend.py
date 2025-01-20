import tkinter as tk
from tkinter import ttk, messagebox

class CatalogGUI:
    def __init__(self, root, backend):
        self.root = root
        self.backend = backend
        self.catalog = self.backend.read_catalog()

        # GUI Layout
        self.root.title("Catalog Management System")
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Description"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Description", text="Description")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(fill=tk.X)

        tk.Button(self.button_frame, text="Add Item", command=self.add_item).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.button_frame, text="Edit Item", command=self.edit_item).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.button_frame, text="Save Changes", command=self.save_changes).pack(side=tk.LEFT, padx=5, pady=5)

        self.populate_tree()

    def populate_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in self.catalog:
            self.tree.insert("", tk.END, values=(item["ID"], item["Name"], item["Description"]))

    def add_item(self):
        def save():
            new_item = {"ID": id_entry.get(), "Name": name_entry.get(), "Description": desc_entry.get()}
            if self.backend.add_item(self.catalog, new_item):
                self.populate_tree()
                add_window.destroy()
            else:
                messagebox.showerror("Error", "All fields are required.")

        add_window = tk.Toplevel(self.root)
        add_window.title("Add Item")
        tk.Label(add_window, text="ID").pack()
        id_entry = tk.Entry(add_window)
        id_entry.pack()
        tk.Label(add_window, text="Name").pack()
        name_entry = tk.Entry(add_window)
        name_entry.pack()
        tk.Label(add_window, text="Description").pack()
        desc_entry = tk.Entry(add_window)
        desc_entry.pack()
        tk.Button(add_window, text="Save", command=save).pack()

    def edit_item(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "No item selected.")
            return

        item_values = self.tree.item(selected)["values"]
        item_id = item_values[0]

        def save():
            updates = {"Name": name_entry.get(), "Description": desc_entry.get()}
            updates = {k: v for k, v in updates.items() if v}  # Only update non-empty fields
            if self.backend.edit_item(self.catalog, item_id, updates):
                self.populate_tree()
                edit_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to update item.")

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Item")
        tk.Label(edit_window, text="Name").pack()
        name_entry = tk.Entry(edit_window)
        name_entry.insert(0, item_values[1])
        name_entry.pack()
        tk.Label(edit_window, text="Description").pack()
        desc_entry = tk.Entry(edit_window)
        desc_entry.insert(0, item_values[2])
        desc_entry.pack()
        tk.Button(edit_window, text="Save", command=save).pack()

    def save_changes(self):
        self.backend.save_catalog(self.catalog)
        messagebox.showinfo("Success", "Changes saved successfully.")
