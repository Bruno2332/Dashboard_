import streamlit as st
from db.connection import DatabaseConnection
from dashboard.components.top_selling_products_chart import TopSellingProductsChart
from dashboard.components.sales_over_time_chart import SalesOverTimeChart
from dashboard.components.sales_by_seller_chart import SalesBySellerChart
from dashboard.components.sales_by_product_chart import SalesByProductChart
from dashboard.components.sales_by_region_chart import SalesByRegionChart
from dashboard.components.sales_growth_index_chart import SalesGrowthIndexChart 
from dashboard.components.filter_repository import FilterRepository
from dashboard.components.sales_average_ticket_seller_chart import SalesAverageTicketSellerChart
from dashboard.components.sales_average_ticket_region_chart import SalesAverageTicketRegionChart


st.set_page_config(page_title="Dashboard de Vendas", layout="wide")
st.title("Dashboard de Vendas")

try:
    with DatabaseConnection() as db:

        filters_repository = FilterRepository(db)

        sellers_option = filters_repository.get_sellers()
        region_option = filters_repository.get_regions()
        products_option = filters_repository.get_products()


        st.sidebar.header("Filtros")

        period = st.sidebar.selectbox(
            "Selecione o período:",
            ["Todo o período", "Último mês", "Últimos 3 meses", "Últimos 6 meses", "Último ano"]
        )

        
        sellers = st.sidebar.selectbox("Selecione o vendedor", options=["Todos"] + sellers_option)
        regions = st.sidebar.selectbox("Selecione a região", options=["Todas"] + region_option)
        products = st.sidebar.selectbox("Selecione o produto", options=["Todos"] + products_option)

        chart_option = st.sidebar.radio(
            "Escolha o gráfico",
            ["Produtos mais vendidos",
                "Vendas por período",
                "Comparativo entre vendedores",
                "Comparativo entre produtos",
                "Comparativo entre regiões",
                "Índice de crescimento",
                "Ticket médio por vendedor",
                "Ticket médio por região"]
        )

        chart_map = {
                "Produtos mais vendidos": TopSellingProductsChart(db),
                "Vendas por período": SalesOverTimeChart(db),
                "Comparativo entre vendedores": SalesBySellerChart(db),
                "Comparativo entre produtos": SalesByProductChart(db),
                "Comparativo entre regiões": SalesByRegionChart(db),
                "Índice de crescimento": SalesGrowthIndexChart(db),
                "Ticket médio por vendedor": SalesAverageTicketSellerChart(db),
                "Ticket médio por região": SalesAverageTicketRegionChart(db)
            }
        
        selected_chart = chart_map[chart_option]
        selected_chart.render(
            period=period,
            sellers=sellers,
            regions=regions,
            products=products
        )
except Exception as e:
    st.error(f'Erro ao conectar ou executar o app: {e}')