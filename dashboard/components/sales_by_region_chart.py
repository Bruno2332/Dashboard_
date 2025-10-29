from .base_chart import BaseChart

class SalesByRegionChart(BaseChart):

    region_permission = False

    def __init__(self, db):
        super().__init__(db, title="Faturamento por Região")


    def get_query(self, **filters):
        return """
            SELECT r.nome AS regiao, SUM(v.valor) AS total_vendas
            FROM vendas v
            JOIN regioes r ON v.id_regiao = r.id_regiao
            GROUP BY r.nome
            ORDER BY total_vendas DESC;
        """


    def get_chart_type(self):
        return "pie"
    

    