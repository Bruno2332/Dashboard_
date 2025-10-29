from connection import DatabaseConnection
from import_csv import CsvImporter


path = "C:/Users/55169/Documents/Python/Projeto_Dados/data/uploads/dados_vendas_ficticios.csv"


with DatabaseConnection() as db:
    importer = CsvImporter(db)
    importer.import_sales(path)