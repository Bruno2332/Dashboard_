import os
import shutil
from datetime import datetime
import streamlit as st
from .import_csv import CsvImporter
from .connection import DatabaseConnection

class UploadManager:

    def __init__(self, uploads_dir="data/uploads", processed_dir="data/processed"):
        self.uploads_dir = uploads_dir
        self.processed_dir = processed_dir

        os.makedirs(uploads_dir, exist_ok=True)
        os.makedirs(processed_dir, exist_ok=True)

    def process_csv(self, csv_file):

        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"vendas_{timestamp}"
            upload_path = os.path.join(self.uploads_dir, filename)
            processed_path = os.path.join(self.processed_dir, filename)

            with open(upload_path, "wb") as file:
                file.write(csv_file.read())

            with DatabaseConnection() as db:
                importer = CsvImporter(db)
                importer.import_sales(upload_path)

            shutil.move(upload_path, processed_path)

            st.success(f"Dados importados com sucesso!")

        except Exception as e:
            st.error(f"Erro ao processar csv: Colunas faltando ou diferente do padrão")
            