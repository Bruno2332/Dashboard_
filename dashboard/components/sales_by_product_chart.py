from .base_chart import BaseChart

class SalesByProductChart(BaseChart):

    product_permission = False

    def __init__(self, db):
        super().__init__(db, title="Comparativo entre Produtos", color_scale="Oranges")


    def get_query(self, **filters):
        return """
            SELECT p.nome AS produto, SUM(v.valor) AS total_vendas
            FROM vendas v
            JOIN produtos p ON v.id_produto = p.id_produto
            GROUP BY p.nome
            ORDER BY total_vendas DESC;
        """


    def get_chart_type(self):
        return "bar"
    

    