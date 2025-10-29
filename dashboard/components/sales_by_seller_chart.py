from .base_chart import BaseChart

class SalesBySellerChart(BaseChart):
    
    sellers_permission = False

    def __init__(self, db):
        super().__init__(db, title="Comparativo entre Vendedores", color_scale="Purples")
    
    
    def get_query(self, **filters):
        return """
            SELECT vdr.nome AS vendedor, SUM(v.valor) AS total_vendas
            FROM vendas v
            JOIN vendedores vdr ON v.id_vendedor = vdr.id_vendedor
            GROUP BY vdr.nome
            ORDER BY total_vendas DESC;
        """

    def get_chart_type(self):
        return "bar"
    
    