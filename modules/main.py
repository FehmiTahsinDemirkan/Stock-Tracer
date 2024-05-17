from database_management import DatabaseManager
from login_register import run_login_register_app
from product_management import run_product_management_app
import notification

def main():
    # Veritabanı yöneticisi oluştur
    db_manager = DatabaseManager(server='FEHMI\SQLEXPRESS', database='StockTracer')
    db_manager.connect()

    # Kullanıcı kayıt ve giriş uygulamasını başlat
    run_login_register_app()

    # Ürün yönetimi uygulamasını başlatmak için giriş yaptıktan sonra kullanıcı ID'sini al
    # (Bu adım, kullanıcı giriş yaptıktan sonra gerçekleşecek)
    user_id = 1  # Örnek olarak, kullanıcı ID'sini varsayılan olarak 1 olarak ayarladık

    # Ürün yönetimi uygulamasını başlat
    run_product_management_app(user_id)

    # # Bildirim uygulamasını başlat
    # notification.run_notification_service()

    # Veritabanı bağlantısını kapat
    db_manager.disconnect()

if __name__ == "__main__":
    main()
