import pandas as pd
from .connection import DatabaseConnection


class CsvImporter:

    EXPECTED_COLUMNS = ["Data da Venda", "Vendedor", "Produto", "Região", "Valor"]

    TABLE_MAPPING = {
        "Vendedor": {"tabela": "vendedores", "coluna_id": "id_vendedor"},
        "Produto": {"tabela": "produtos", "coluna_id": "id_produto"},
        "Região": {"tabela": "regioes", "coluna_id": "id_regiao"},
        "Venda": {
            "tabela": "vendas",
            "colunas": ["data_venda", "id_vendedor", "id_produto", "id_regiao", "valor"]
        }
    }


    def __init__(self, db: DatabaseConnection):
        self.db = db

    
    def import_sales(self, csv_path):

        try:
            df = pd.read_csv(csv_path)
        except Exception:
            raise ValueError("Erro ao ler o arquivo CSV")
        
        self._csv_validate(df)

        for _, row in df.iterrows():
            sale_date = row["Data da Venda"]
            seller = row["Vendedor"]
            product = row["Produto"]
            region = row["Região"]
            value = row["Valor"]

            seller_id = self._get_or_create("Vendedor", seller)
            product_id = self._get_or_create("Produto", product)
            region_id = self._get_or_create("Região", region)

            try:
                sales_table = self.TABLE_MAPPING["Venda"]["tabela"]
                sales_column = ", ".join(self.TABLE_MAPPING["Venda"]["colunas"])

                self.db.cur.execute(
                    f"""INSERT INTO {sales_table} ({sales_column})
                     VALUES (%s, %s, %s, %s, %s)""",
                     (sale_date, seller_id, product_id, region_id, value)
                )
            except Exception:
                print(f"Erro ao inserir venda ({seller}: {product})")

        self.db.commit()
        print("Dados importados com sucesso")    


    def _csv_validate(self, df):

        missing_columns = set(self.EXPECTED_COLUMNS) - set(df.columns)
        if missing_columns:
            print(f'CSV inválido. Existem colunas faltando ou diferente do padrão')

        df = df[self.EXPECTED_COLUMNS]

        try:
            df["Valor"] = df["Valor"].astype(float)
            df["Data da Venda"] = pd.to_datetime(df["Data da Venda"], errors="raise")
        except Exception as e:
            print(f'Tipos de dados incorretos: {e}')
        

    def _get_or_create(self, csv_field, name):

        try:
            mapping = self.TABLE_MAPPING[csv_field]
            table = mapping["tabela"]
            id_column = mapping["coluna_id"]

            self.db.cur.execute(
                f"SELECT {id_column} FROM {table} WHERE nome = %s", (name.strip(),))
            result = self.db.cur.fetchone()

            if result:
                return result[0]
            
            self.db.cur.execute(
                f"INSERT INTO {table} (nome) VALUES (%s) RETURNING {id_column};", (name.strip(),))
            self.db.commit()
            return self.db.cur.fetchone()[0]


        except KeyError:
            print(f"Campo {csv_field} não mapeado em Mapeamento de tabelas")
        except Exception:
            print(f"Erro ao inserir/consultar {name} em {csv_field}")
            

            