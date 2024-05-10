import pyodbc

class DatabaseManager:
    def __init__(self, server, database):
        self.server = server
        self.database = database
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = pyodbc.connect('Driver={SQL Server};'
                                       f'Server={self.server};'
                                       f'Database={self.database};'
                                       'Trusted_Connection=yes;')
            self.cursor = self.conn.cursor()
            print("Veritabanına bağlantı başarılı.")
        except Exception as e:
            print("Veritabanına bağlanırken hata oluştu:", e)

    def disconnect(self):
        try:
            if self.conn:
                self.conn.close()
                print("Veritabanı bağlantısı kapatıldı.")
            else:
                print("Bağlantı zaten kapalı.")
        except Exception as e:
            print("Veritabanı bağlantısını kapatırken hata oluştu:", e)

    def execute_query(self, query):
        try:
            if not self.conn:
                print("Bağlantı yok.")
                return
            self.cursor.execute(query)
            self.conn.commit()
            print("Sorgu başarıyla çalıştırıldı.")
        except Exception as e:
            print("Sorgu çalıştırılırken hata oluştu:", e)

    def fetch_data(self, query):
        try:
            if not self.conn:
                print("Bağlantı yok.")
                return []
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            print("Veri alınırken hata oluştu:", e)
            return []

