from .base_chart import BaseChart

class SalesAverageTicketRegionChart(BaseChart):

    region_permission = False
    
    def __init__(self, db):
        super().__init__(db, title="Ticket Médio por Região", color_scale="Cividis")

    def get_query(self, **filters):
        query = """
            SELECT 
                r.nome AS regiao,
                ROUND(SUM(v.valor) / COUNT(v.id_venda), 2) AS ticket_medio
            FROM vendas v
            JOIN regioes r ON v.id_regiao = r.id_regiao
            GROUP BY r.nome
            ORDER BY ticket_medio DESC;
        """
        return query
    

    def get_chart_type(self):
        return "bar"
