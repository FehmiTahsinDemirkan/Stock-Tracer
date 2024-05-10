import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from database_management import DatabaseManager

class ProductManagementApp:
    def __init__(self, master, user_id):
        self.master = master
        master.title("Ürün Yönetimi")

        # Veritabanı bağlantısı
        self.db_manager = DatabaseManager(server='FEHMI\SQLEXPRESS', database='StockTracer')
        self.db_manager.connect()

        # Kullanıcı ID'si
        self.user_id = user_id

        # Ürün girişi widget'leri
        self.product_name_label = tk.Label(master, text="Ürün İsmi:")
        self.product_name_label.grid(row=0, column=0, padx=10, pady=5)
        self.product_name_entry = tk.Entry(master)
        self.product_name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.category_label = tk.Label(master, text="Kategori:")
        self.category_label.grid(row=1, column=0, padx=10, pady=5)
        self.category_combobox = ttk.Combobox(master,
                                              values=["Konserve Ürün", "Ambalajlı Ürün", "Açık Ürün", "Temizlik Ürün",
                                                      "Kişisel Bakım Ürün", "İlaç Ürün"])
        self.category_combobox.grid(row=1, column=1, padx=10, pady=5)

        self.expiry_label = tk.Label(master, text="Son Kullanma Tarihi:")
        self.expiry_label.grid(row=2, column=0, padx=10, pady=5)
        self.expiry_entry = DateEntry(master, date_pattern='yyyy-mm-dd')
        self.expiry_entry.grid(row=2, column=1, padx=10, pady=5)

        # Ekle ve Yenile butonları
        self.submit_button = tk.Button(master, text="Ekle", command=self.add_product)
        self.submit_button.grid(row=3, column=0, padx=10, pady=5)

        self.refresh_button = tk.Button(master, text="Yenile", command=self.refresh_products)
        self.refresh_button.grid(row=3, column=1, padx=10, pady=5)

        # Ürünleri göstermek için Treeview widget'i oluştur
        self.tree = ttk.Treeview(master, columns=("Ürün İsmi", "Kategori", "Son Kullanma Tarihi"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("Ürün İsmi", text="Ürün İsmi")
        self.tree.heading("Kategori", text="Kategori")
        self.tree.heading("Son Kullanma Tarihi", text="Son Kullanma Tarihi")
        self.tree.grid(row=4, column=0, padx=10, pady=5, columnspan=2)



        # Ürünleri göster
        self.show_products(user_id)

    def show_products(self, user_id):
        # Kullanıcının ürünlerini veritabanından al
        query = f"SELECT id, product_name, category, expiration_date FROM Product WHERE user_id={user_id}"
        rows = self.db_manager.fetch_data(query)

        # Treeview'de ürünleri göster
        for row in rows:
            self.tree.insert("", "end", text=row[0], values=(row[1], row[2], row[3]))

    def add_product(self):
        product_name = self.product_name_entry.get()
        category = self.category_combobox.get()
        expiry_date = self.expiry_entry.get_date().strftime('%Y-%m-%d')

        query = f"INSERT INTO Product (product_name, category, expiration_date, user_id) " \
                f"VALUES ('{product_name}', '{category}', '{expiry_date}', {self.user_id})"
        self.db_manager.execute_query(query)
        messagebox.showinfo("Başarılı", "Ürün başarıyla eklendi!")

    def refresh_products(self):
        # Mevcut verileri temizle
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Yeniden ürünleri göster
        self.show_products(self.user_id)
def run_product_management_app(user_id):
    root = tk.Tk()
    app = ProductManagementApp(root, user_id)
    root.mainloop()

if __name__ == "__main__":
    # Kullanıcı ID'sini belirtin
    user_id = 1  # Örnek olarak 1 olarak belirtildi, gerçek kullanıcı ID'si ile değiştirin
    run_product_management_app(user_id)
