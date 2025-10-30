import streamlit as st

class HomeScreen:

    def __init__(self):
        self._inject_styles()

    def _inject_styles(self):
        with open("dashboard/css/styles.css") as file:
            st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)




    def render(self):
        st.markdown('<h1>📊 Sistema de Análise de Vendas</h1>', unsafe_allow_html=True)
        st.markdown('<p>Escolha uma das opções abaixo</p>', unsafe_allow_html=True)
        st.button("Ir para o Dashboard",
                on_click=lambda: st.session_state.update({"page": "dashboard"}),
                key="btn_dashboard")
        st.button("Importar novos dados",
                on_click=lambda: st.session_state.update({"page": "upload"}),
                key="btn_upload")
        


