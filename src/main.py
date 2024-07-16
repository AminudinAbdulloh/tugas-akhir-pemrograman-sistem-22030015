import tkinter as tk
from tkinter import messagebox, ttk
from product import Product
from category import Category
from unit import Unit

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Dashboard CRUD - Aminudin Abdulloh (22030015)")
        self.geometry("800x600")
        self.configure(bg="lightblue")
        
        self.units = []
        self.categories = []
        self.products = []

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TNotebook', background="lightblue", foreground="black")
        style.configure('TNotebook.Tab', background="lightgreen", foreground="black")
        style.map('TNotebook.Tab', background=[('selected', 'lightblue')], foreground=[('selected', 'blue')])

        style.configure('addButton.TButton', foreground="black", background="blue")    
        style.configure('editButton.TButton', foreground="black", background="green")
        style.configure('deleteButton.TButton', foreground="black", background="orange")
        style.configure('exitButton.TButton', foreground="black", background="red")

        self.tab_control = ttk.Notebook(self)
        
        self.tab_products = ttk.Frame(self.tab_control)
        self.tab_categories = ttk.Frame(self.tab_control)
        self.tab_units = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab_products, text="Products")
        self.tab_control.add(self.tab_categories, text="Categories")
        self.tab_control.add(self.tab_units, text="Units")
        
        self.tab_control.pack(expand=1, fill="both")
        
        self.create_product_tab()
        self.create_category_tab()
        self.create_unit_tab()
        
    def create_product_tab(self):
        frame = ttk.Frame(self.tab_products)
        frame.pack(padx=10, pady=10, fill='x')
        
        lbl_name = ttk.Label(frame, text="Product Name:")
        lbl_name.grid(column=0, row=0, padx=5, pady=5)
        self.ent_product_name = ttk.Entry(frame)
        self.ent_product_name.grid(column=1, row=0, padx=5, pady=5)

        lbl_category = ttk.Label(frame, text="Category:")
        lbl_category.grid(column=0, row=1, padx=5, pady=5)
        self.cmb_category = ttk.Combobox(frame, values=[cat.name for cat in self.categories])
        self.cmb_category.grid(column=1, row=1, padx=5, pady=5)

        lbl_unit = ttk.Label(frame, text="Unit:")
        lbl_unit.grid(column=0, row=2, padx=5, pady=5)
        self.cmb_unit = ttk.Combobox(frame, values=[unit.name for unit in self.units])
        self.cmb_unit.grid(column=1, row=2, padx=5, pady=5)
        
        btn_add_product = ttk.Button(frame, text="Add Product", command=self.add_product, style="addButton.TButton")
        btn_add_product.grid(column=0, row=3, columnspan=2, padx=5, pady=5)
        
        btn_edit_product = ttk.Button(frame, text="Edit Product", command=self.edit_product, style="editButton.TButton")
        btn_edit_product.grid(column=0, row=4, columnspan=2, padx=5, pady=5)

        btn_delete_product = ttk.Button(frame, text="Delete Product", command=self.delete_product, style="deleteButton.TButton")
        btn_delete_product.grid(column=0, row=5, columnspan=2, padx=5, pady=5)

        btn_exit = ttk.Button(frame, text="Exit", command=self.exit_application, style='exitButton.TButton')
        btn_exit.grid(column=0, row=6, columnspan=2, padx=5, pady=5)
        
        self.tree_products = ttk.Treeview(self.tab_products, columns=("Name", "Category", "Unit"), show="headings")
        self.tree_products.heading("Name", text="Name")
        self.tree_products.heading("Category", text="Category")
        self.tree_products.heading("Unit", text="Unit")
        self.tree_products.pack(padx=10, pady=10, fill='both', expand=True)

    def add_product(self):
        name = self.ent_product_name.get()
        category_name = self.cmb_category.get()
        unit_name = self.cmb_unit.get()
        
        category = next((cat for cat in self.categories if cat.name == category_name), None)
        unit = next((un for un in self.units if un.name == unit_name), None)
        
        if name and category and unit:
            product = Product(name, category, unit)
            self.products.append(product)
            self.tree_products.insert('', 'end', values=(product.name, product.category.name, product.unit.name))
            self.ent_product_name.delete(0, tk.END)
            self.cmb_category.set('')
            self.cmb_unit.set('')
        else:
            messagebox.showwarning("Validation Error", "All fields must be filled correctly.")

    def edit_product(self):
        selected_item = self.tree_products.selection()
        if selected_item:
            item = self.tree_products.item(selected_item)
            values = item['values']
            name = values[0]
            
            self.ent_product_name.delete(0, tk.END)
            self.ent_product_name.insert(0, name)
            self.cmb_category.set(values[1])
            self.cmb_unit.set(values[2])

            self.products = [product for product in self.products if product.name != name]
            self.tree_products.delete(selected_item)
        else:
            messagebox.showwarning("Selection Error", "Please select a product to edit.")
    
    def delete_product(self):
        selected_item = self.tree_products.selection()
        if selected_item:
            item = self.tree_products.item(selected_item)
            values = item['values']
            name = values[0]
            
            self.products = [product for product in self.products if product.name != name]
            self.tree_products.delete(selected_item)
        else:
            messagebox.showwarning("Selection Error", "Please select a product to delete.")

    def create_category_tab(self):
        frame = ttk.Frame(self.tab_categories)
        frame.pack(padx=10, pady=10, fill='x')
        
        lbl_name = ttk.Label(frame, text="Category Name:")
        lbl_name.grid(column=0, row=0, padx=5, pady=5)
        self.ent_category_name = ttk.Entry(frame)
        self.ent_category_name.grid(column=1, row=0, padx=5, pady=5)
        
        btn_add_category = ttk.Button(frame, text="Add Category", command=self.add_category, style="addButton.TButton")
        btn_add_category.grid(column=0, row=1, columnspan=2, padx=5, pady=5)

        btn_edit_category = ttk.Button(frame, text="Edit Category", command=self.edit_category, style="editButton.TButton")
        btn_edit_category.grid(column=0, row=2, columnspan=2, padx=5, pady=5)

        btn_delete_category = ttk.Button(frame, text="Delete Category", command=self.delete_category, style="deleteButton.TButton")
        btn_delete_category.grid(column=0, row=3, columnspan=2, padx=5, pady=5)

        btn_exit = ttk.Button(frame, text="Exit", command=self.exit_application, style='exitButton.TButton')
        btn_exit.grid(column=0, row=6, columnspan=2, padx=5, pady=5)
        
        self.tree_categories = ttk.Treeview(self.tab_categories, columns=("Name",), show="headings")
        self.tree_categories.heading("Name", text="Name")
        self.tree_categories.pack(padx=10, pady=10, fill='both', expand=True)

    def add_category(self):
        name = self.ent_category_name.get()
        if name:
            category = Category(name)
            self.categories.append(category)
            self.tree_categories.insert('', 'end', values=(category.name,))
            self.cmb_category['values'] = [cat.name for cat in self.categories]
            self.ent_category_name.delete(0, tk.END)
        else:
            messagebox.showwarning("Validation Error", "Category name must not be empty.")

    def edit_category(self):
        selected_item = self.tree_categories.selection()
        if selected_item:
            item = self.tree_categories.item(selected_item)
            values = item['values']
            name = values[0]

            self.ent_category_name.delete(0, tk.END)
            self.ent_category_name.insert(0, name)

            self.categories = [category for category in self.categories if category.name != name]
            self.tree_categories.delete(selected_item)
            self.cmb_category['values'] = [cat.name for cat in self.categories]
        else:
            messagebox.showwarning("Selection Error", "Please select a category to edit.")
    
    def delete_category(self):
        selected_item = self.tree_categories.selection()
        if selected_item:
            item = self.tree_categories.item(selected_item)
            values = item['values']
            name = values[0]

            self.categories = [category for category in self.categories if category.name != name]
            self.tree_categories.delete(selected_item)
            self.cmb_category['values'] = [cat.name for cat in self.categories]
        else:
            messagebox.showwarning("Selection Error", "Please select a category to delete.")
    
    def create_unit_tab(self):
        frame = ttk.Frame(self.tab_units)
        frame.pack(padx=10, pady=10, fill='x')
        
        lbl_name = ttk.Label(frame, text="Unit Name:")
        lbl_name.grid(column=0, row=0, padx=5, pady=5)
        self.ent_unit_name = ttk.Entry(frame)
        self.ent_unit_name.grid(column=1, row=0, padx=5, pady=5)
        
        btn_add_unit = ttk.Button(frame, text="Add Unit", command=self.add_unit, style="addButton.TButton")
        btn_add_unit.grid(column=0, row=1, columnspan=2, padx=5, pady=5)

        btn_edit_unit = ttk.Button(frame, text="Edit Unit", command=self.edit_unit, style="editButton.TButton")
        btn_edit_unit.grid(column=0, row=2, columnspan=2, padx=5, pady=5)

        btn_delete_unit = ttk.Button(frame, text="Delete Unit", command=self.delete_unit, style="deleteButton.TButton")
        btn_delete_unit.grid(column=0, row=3, columnspan=2, padx=5, pady=5)
        
        btn_exit = ttk.Button(frame, text="Exit", command=self.exit_application, style='exitButton.TButton')
        btn_exit.grid(column=0, row=6, columnspan=2, padx=5, pady=5)

        self.tree_units = ttk.Treeview(self.tab_units, columns=("Name",), show="headings")
        self.tree_units.heading("Name", text="Name")
        self.tree_units.pack(padx=10, pady=10, fill='both', expand=True)
    
    def add_unit(self):
        name = self.ent_unit_name.get()
        if name:
            unit = Unit(name)
            self.units.append(unit)
            self.tree_units.insert('', 'end', values=(unit.name,))
            self.cmb_unit['values'] = [unit.name for unit in self.units]
            self.ent_unit_name.delete(0, tk.END)
        else:
            messagebox.showwarning("Validation Error", "Unit name must not be empty.")

    def edit_unit(self):
        selected_item = self.tree_units.selection()
        if selected_item:
            item = self.tree_units.item(selected_item)
            values = item['values']
            name = values[0]

            self.ent_unit_name.delete(0, tk.END)
            self.ent_unit_name.insert(0, name)

            self.units = [unit for unit in self.units if unit.name != name]
            self.tree_units.delete(selected_item)
            self.cmb_unit['values'] = [unit.name for unit in self.units]
        else:
            messagebox.showwarning("Selection Error", "Please select a unit to edit.")
    
    def delete_unit(self):
        selected_item = self.tree_units.selection()
        if selected_item:
            item = self.tree_units.item(selected_item)
            values = item['values']
            name = values[0]

            self.units = [unit for unit in self.units if unit.name != name]
            self.tree_units.delete(selected_item)
            self.cmb_unit['values'] = [unit.name for unit in self.units]
        else:
            messagebox.showwarning("Selection Error", "Please select a unit to delete.")

    def exit_application(self):
        self.quit()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
