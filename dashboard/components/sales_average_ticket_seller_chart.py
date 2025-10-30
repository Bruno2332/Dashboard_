from .base_chart import BaseChart

class SalesAverageTicketSellerChart(BaseChart):

    sellers_permission = False

    def __init__(self, db):
        super().__init__(db, title="Ticket Médio por Vendedor", color_scale="Viridis")

    def get_query(self, **filters):
        query = """
            SELECT 
                vdr.nome AS vendedor,
                ROUND(SUM(v.valor) / COUNT(v.id_venda), 2) AS ticket_medio
            FROM vendas v
            JOIN vendedores vdr ON v.id_vendedor = vdr.id_vendedor
            GROUP BY vdr.nome
            ORDER BY ticket_medio DESC;
        """
        return query
    

    def get_chart_type(self):
        return "bar"
