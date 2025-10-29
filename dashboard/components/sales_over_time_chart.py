from .base_chart import BaseChart

class SalesOverTimeChart(BaseChart):

    period_permission = False

    def __init__(self, db):
        super().__init__(db, title="Vendas por Período", color_scale="Greens")


    def get_query(self, period="Mensal", **filters):
       
        trunc_map = {
            "Mensal": "month",
            "Trimestral": "quarter",
            "Semestral": "month",  
            "Anual": "year",
            "Todo o Período": None,
        }

        trunc = trunc_map.get(period, "month")

        if trunc is None:
            return """
                SELECT 'Total' AS periodo, SUM(v.valor) AS total_vendas
                FROM vendas v;
            """

        query = f"""
            SELECT DATE_TRUNC('{trunc}', v.data_venda) AS periodo,
                SUM(v.valor) AS total_vendas
            FROM vendas v
            GROUP BY DATE_TRUNC('{trunc}', v.data_venda)
            ORDER BY periodo;
        """

        if period == "Semestral":
            query = """
                SELECT 
                    CONCAT(EXTRACT(YEAR FROM v.data_venda), '-', 
                        CASE WHEN EXTRACT(MONTH FROM v.data_venda) <= 6 THEN '1º Semestre' ELSE '2º Semestre' END
                    ) AS periodo,
                    SUM(v.valor) AS total_vendas
                FROM vendas v
                GROUP BY 1
                ORDER BY periodo;
            """

        return query


    def get_chart_type(self):
        return "line"