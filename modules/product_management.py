import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from database_management import DatabaseManager
from datetime import date, datetime
import logging

# Logging yapılandırması
logging.basicConfig(filename='modules.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProductManagementApp:
    def __init__(self, master, user_id):
        self.master = master
        self.master.title("Ürün Yönetimi")
        self.master.geometry("600x400")
        self.master.configure(bg='#f7f7f7')

        self.db_manager = DatabaseManager(server='FEHMI\SQLEXPRESS', database='StockTracer')
        self.db_manager.connect()

        self.user_id = user_id

        self.create_widgets()
        self.show_products()

    def create_widgets(self):
        self.style_label = {"font": ("Arial", 12), "bg": "#f7f7f7"}
        self.style_entry = {"font": ("Arial", 12), "bg": "#ffffff"}
        self.style_button = {"font": ("Arial", 12), "bg": "#007BFF", "fg": "#ffffff", "activebackground": "#0056b3"}

        self.product_name_label = tk.Label(self.master, text="Ürün İsmi:", **self.style_label)
        self.product_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.product_name_entry = tk.Entry(self.master, **self.style_entry)
        self.product_name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.category_label = tk.Label(self.master, text="Kategori:", **self.style_label)
        self.category_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.category_combobox = ttk.Combobox(self.master, values=["Konserve Ürün", "Ambalajlı Ürün", "Açık Ürün", "Temizlik Ürün", "Kişisel Bakım Ürün", "İlaç Ürün"])
        self.category_combobox.grid(row=1, column=1, padx=10, pady=5)

        self.expiry_label = tk.Label(self.master, text="Son Kullanma Tarihi:", **self.style_label)
        self.expiry_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.expiry_entry = DateEntry(self.master, date_pattern='yyyy-mm-dd')
        self.expiry_entry.grid(row=2, column=1, padx=10, pady=5)

        self.submit_button = tk.Button(self.master, text="Ekle", command=self.add_product, **self.style_button)
        self.submit_button.grid(row=3, column=0, padx=10, pady=5)

        self.refresh_button = tk.Button(self.master, text="Yenile", command=self.refresh_products, **self.style_button)
        self.refresh_button.grid(row=3, column=1, padx=10, pady=5)

        self.check_button = tk.Button(self.master, text="Kontrol Et", command=self.check_products, **self.style_button)
        self.check_button.grid(row=3, column=2, padx=10, pady=5)

        self.tree = ttk.Treeview(self.master, columns=("Ürün İsmi", "Kategori", "Son Kullanma Tarihi"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("Ürün İsmi", text="Ürün İsmi")
        self.tree.heading("Kategori", text="Kategori")
        self.tree.heading("Son Kullanma Tarihi", text="Son Kullanma Tarihi")
        self.tree.column("#0", width=50)
        self.tree.column("Ürün İsmi", width=150)
        self.tree.column("Kategori", width=150)
        self.tree.column("Son Kullanma Tarihi", width=150)
        self.tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.master.grid_rowconfigure(4, weight=1)
        self.master.grid_columnconfigure(2, weight=1)

    def show_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = f"SELECT id, product_name, category, expiration_date FROM Product WHERE user_id={self.user_id}"
        rows = self.db_manager.fetch_data(query)

        logging.info(f"Sorgu: {query}")

        for row in rows:
            self.tree.insert("", "end", text=row[0], values=(row[1], row[2], row[3]))

    def check_products(self):
        today = datetime.today().date()
        warning_message = "Son kullanma tarihine kalan süre:\n\n"

        for item in self.tree.get_children():
            product_name = self.tree.item(item, "values")[0]
            expiry_date = datetime.strptime(self.tree.item(item, "values")[2], "%Y-%m-%d").date()
            remaining_days = (expiry_date - today).days
            warning_message += f"{product_name}: {remaining_days} gün kaldı.\n"

        logging.info("Urunler kontrol edildi.")
        messagebox.showinfo("Urun Uyarilari", warning_message)

    def add_product(self):
        product_name = self.product_name_entry.get()
        category = self.category_combobox.get()
        expiry_date = self.expiry_entry.get_date()
        current_date = date.today()

        if not product_name or not category:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
            logging.warning("Eksik bilgi: Lutfen tüm alanlari doldurun!")
            return

        if expiry_date < current_date:
            messagebox.showerror("Hata", "Gecmis bir tarih secemezsiniz!")
            logging.warning("Gecmis bir tarih secildi!")
            return

        query = f"INSERT INTO Product (product_name, category, expiration_date, user_id) VALUES ('{product_name}', '{category}', '{expiry_date}', {self.user_id})"
        self.db_manager.execute_query(query)
        logging.info(f"Sorgu: {query}")
        messagebox.showinfo("Başarılı", "Ürün başarıyla eklendi!")
        self.refresh_products()

    def refresh_products(self):
        self.show_products()
        logging.info("Urunler yenilendi.")

def run_product_management_app(user_id):
    root = tk.Tk()
    app = ProductManagementApp(root, user_id)
    root.mainloop()

if __name__ == "__main__":
    user_id = 1
    run_product_management_app(user_id)
