import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from database_management import DatabaseManager

class NotificationManager:
    def __init__(self, server, database, sender_email, sender_password):
        self.db_manager = DatabaseManager(server, database)
        self.sender_email = sender_email
        self.sender_password = sender_password

    def add_user_for_notifications(self, email):
        # Kullanıcıyı bildirimler için kaydet
        query = f"INSERT INTO NotificationUsers (email) VALUES ('{email}')"
        self.db_manager.execute_query(query)

    def send_notification(self):
        # Bugünkü tarihi al
        today = datetime.now().date()

        # Son kullanma tarihi yaklaşan ürünleri al
        query = f"SELECT * FROM Product WHERE expiration_date = '{today}'"
        self.db_manager.connect()
        products = self.db_manager.fetch_data(query)
        self.db_manager.disconnect()

        # Eğer son kullanma tarihi yaklaşan ürünler varsa, bildirim gönder
        if products:
            subject = "Son Kullanma Tarihi Yaklaşan Ürünler"
            body = "Aşağıdaki ürünlerin son kullanma tarihi bugündür:\n\n"
            for product in products:
                body += f"Ürün Adı: {product[1]}, Son Kullanma Tarihi: {product[2]}\n"

            self.send_email(subject, body)

            print("Bildirim gönderildi.")

    def send_email(self, subject, body):
        try:
            # E-posta gönderme işlemi
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.sender_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, self.sender_email, msg.as_string())
            server.quit()
        except Exception as e:
            print("E-posta gönderirken hata oluştu:", e)

def run_notification_service():
    # Bildirim servisini başlat
    sender_email = 'dfehmitahsin@gmail.com'  
    sender_password = 'flko lpqg kzdn tioq'

    manager = NotificationManager(server='FEHMI\SQLEXPRESS', database='stocktracer',
                                  sender_email=sender_email, sender_password=sender_password)
    manager.send_notification()
