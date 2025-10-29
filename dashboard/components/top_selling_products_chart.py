from .base_chart import BaseChart


class TopSellingProductsChart(BaseChart):

    product_permission = False

    def __init__(self, db):
        super().__init__(db, title="Produtos mais vendidos", color_scale="Blues")


    def get_query(self, **kwargs):
        return """
            SELECT p.nome AS produto, COUNT(v.id_venda) AS quantidade_vendida
            FROM vendas v
            JOIN produtos p ON v.id_produto = p.id_produto
            GROUP BY p.nome
            ORDER BY quantidade_vendida DESC;
        """
    

    def get_chart_type(self):
        return "bar"
    

