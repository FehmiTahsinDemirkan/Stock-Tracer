import tkinter as tk
from tkinter import messagebox
from database_management import DatabaseManager
from product_management import run_product_management_app

class LoginRegisterApp:
    def __init__(self, master):
        self.master = master
        master.title("Giriş ve Kayıt")
        # Veritabanı bağlantısı
        self.db_manager = DatabaseManager(server='FEHMI\SQLEXPRESS', database='StockTracer')
        self.db_manager.connect()

        # Giriş sayfası widget'leri
        self.email_label_login = tk.Label(master, text="Giriş E-posta:")
        self.email_label_login.grid(row=0, column=0, padx=10, pady=5)
        self.email_entry_login = tk.Entry(master)
        self.email_entry_login.grid(row=0, column=1, padx=10, pady=5)

        self.password_label_login = tk.Label(master, text="Giriş Şifre:")
        self.password_label_login.grid(row=1, column=0, padx=10, pady=5)
        self.password_entry_login = tk.Entry(master, show="*")
        self.password_entry_login.grid(row=1, column=1, padx=10, pady=5)

        self.login_button = tk.Button(master, text="Giriş", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # Kayıt sayfası widget'leri
        self.email_label_register = tk.Label(master, text="Kayıt E-posta:")
        self.email_label_register.grid(row=3, column=0, padx=10, pady=5)
        self.email_entry_register = tk.Entry(master)
        self.email_entry_register.grid(row=3, column=1, padx=10, pady=5)

        self.password_label_register = tk.Label(master, text="Kayıt Şifre:")
        self.password_label_register.grid(row=4, column=0, padx=10, pady=5)
        self.password_entry_register = tk.Entry(master, show="*")
        self.password_entry_register.grid(row=4, column=1, padx=10, pady=5)

        self.name_label = tk.Label(master, text="İsim:")
        self.name_label.grid(row=5, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=5, column=1, padx=10, pady=5)

        self.surname_label = tk.Label(master, text="Soyisim:")
        self.surname_label.grid(row=6, column=0, padx=10, pady=5)
        self.surname_entry = tk.Entry(master)
        self.surname_entry.grid(row=6, column=1, padx=10, pady=5)

        self.phone_label = tk.Label(master, text="Telefon:")
        self.phone_label.grid(row=7, column=0, padx=10, pady=5)
        self.phone_entry = tk.Entry(master)
        self.phone_entry.grid(row=7, column=1, padx=10, pady=5)

        self.register_button = tk.Button(master, text="Kayıt Ol", command=self.register)
        self.register_button.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

    def login(self):
        email = self.email_entry_login.get()
        password = self.password_entry_login.get()

        query = f"SELECT id FROM Users WHERE email='{email}' AND password='{password}'"
        rows = self.db_manager.fetch_data(query)

        if rows:
            messagebox.showinfo("Başarılı", "Giriş başarılı!")
            user_id = rows[0][0]  # Kullanıcı ID'sini al
            run_product_management_app(user_id)  # Ürün yönetimi uygulamasını başlat
        else:
            messagebox.showerror("Hata", "E-posta veya şifre yanlış!")

    def register(self):
        email = self.email_entry_register.get()
        password = self.password_entry_register.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        phone = self.phone_entry.get()

        query = f"INSERT INTO Users (first_name, last_name, phone_number, email, password) " \
                f"VALUES ('{name}', '{surname}', '{phone}', '{email}', '{password}')"
        self.db_manager.execute_query(query)
        messagebox.showinfo("Başarılı", "Kayıt başarıyla tamamlandı!")

def run_login_register_app():
    root = tk.Tk()
    app = LoginRegisterApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_login_register_app()
