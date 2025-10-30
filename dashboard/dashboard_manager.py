import streamlit as st
from dashboard.components.filter_repository import FilterRepository
from dashboard.components.top_selling_products_chart import TopSellingProductsChart
from dashboard.components.sales_over_time_chart import SalesOverTimeChart
from dashboard.components.sales_by_seller_chart import SalesBySellerChart
from dashboard.components.sales_by_product_chart import SalesByProductChart
from dashboard.components.sales_by_region_chart import SalesByRegionChart
from dashboard.components.sales_growth_index_chart import SalesGrowthIndexChart
from dashboard.components.sales_average_ticket_seller_chart import SalesAverageTicketSellerChart
from dashboard.components.sales_average_ticket_region_chart import SalesAverageTicketRegionChart


class DashboardManager:

    def __init__(self, db):
        self.db = db
        self.filter_repo = FilterRepository(db)

        self.chart_map = {
            "Produtos mais vendidos": TopSellingProductsChart(db),
            "Vendas por período": SalesOverTimeChart(db),
            "Comparativo entre vendedores": SalesBySellerChart(db),
            "Comparativo entre produtos": SalesByProductChart(db),
            "Comparativo entre regiões": SalesByRegionChart(db),
            "Índice de crescimento": SalesGrowthIndexChart(db),
            "Ticket médio por vendedor": SalesAverageTicketSellerChart(db),
            "Ticket médio por região": SalesAverageTicketRegionChart(db),
        }

    def render(self):
        
        st.title("Dashboard de Vendas")

        try:
            st.sidebar.header("Filtros")

            sellers_option = self.filter_repo.get_sellers()
            region_option = self.filter_repo.get_regions()
            products_option = self.filter_repo.get_products()

            period = st.sidebar.selectbox(
                "Selecione o período:",
                ["Todo o período", "Último mês", "Últimos 3 meses", "Últimos 6 meses", "Último ano"]
            )

            sellers = st.sidebar.selectbox("Selecione o vendedor", options=["Todos"] + sellers_option)
            regions = st.sidebar.selectbox("Selecione a região", options=["Todas"] + region_option)
            products = st.sidebar.selectbox("Selecione o produto", options=["Todos"] + products_option)

            chart_option = st.sidebar.radio(
                "Escolha o gráfico",
                list(self.chart_map.keys())
            )

            selected_chart = self.chart_map[chart_option]
            selected_chart.render(
                period=period,
                sellers=sellers,
                regions=regions,
                products=products
            )

        except Exception as e:
            st.error(f"Erro ao renderizar dashboard: {e}")