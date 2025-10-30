import streamlit as st
from db.connection import DatabaseConnection
from db.upload_manager import UploadManager
from dashboard.dashboard_manager import DashboardManager
from dashboard.home_screen import HomeScreen


st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to_dashboard():
    st.session_state.page = "dashboard"

def upload_csv():
    st.session_state.page = "upload"

if st.session_state.page == "home":
    HomeScreen().render()

elif st.session_state.page == "upload":
    st.title("Importar Dados de Vendas")

    csv_file = st.file_uploader("Selecione o arquivo", type=["csv"])

    if csv_file is not None:
        UploadManager().process_csv(csv_file)

    st.button("Voltar", on_click=lambda: st.session_state.update({"page": "home"}))


elif st.session_state.page == "dashboard":
    try:
        with DatabaseConnection() as db:
            dashboard = DashboardManager(db)
            dashboard.render()
    except Exception as e:
        st.error(f"Erro ao conectar ou renderizar o dashboard: {e}")

    st.sidebar.button("Voltar ao inicio", on_click=lambda: st.session_state.update({"page": "home"}))