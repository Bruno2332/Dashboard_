import pandas as pd

class FilterRepository:

    def __init__(self, db):
        self.db = db


    def _fetch_options(self, query: str):
    
        try:
            df = pd.read_sql(query, self.db.conn)
            return df.iloc[:, 0].tolist() if not df.empty else []
        except Exception as e:
            print(f"Erro ao buscar opções: {e}")
            return []


    def get_sellers(self):
        return self._fetch_options("SELECT nome FROM vendedores ORDER BY nome;")


    def get_regions(self):
        return self._fetch_options("SELECT nome FROM regioes ORDER BY nome;")


    def get_products(self):
        return self._fetch_options("SELECT nome FROM produtos ORDER BY nome;")