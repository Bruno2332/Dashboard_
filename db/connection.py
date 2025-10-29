import psycopg2
from psycopg2 import OperationalError

class DatabaseConnection:

    def __init__(self, host="localhost", database="dashboard_vendas", user="postgres", password="123456", port="5432"):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.conn = None
        self.cur = None


    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            self.cur = self.conn.cursor()
        except OperationalError as e:
            print(f'Erro ao conectar ao banco: {e}')

    
    def commit(self):
        if self.conn:
            self.conn.commit()


    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print("Conexão encerrada")


    def __enter__(self):
        self.connect()
        return self
    

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()    
        