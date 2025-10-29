from .base_chart import BaseChart

class SalesGrowthIndexChart(BaseChart):

    period_permission = False

    def __init__(self, db):
        super().__init__(db, title="Crescimento Percentual", color_scale="Blues")

    def get_query(self, **filters):
        return """
            SELECT 
                DATE_TRUNC('month', data_venda) AS periodo,
                SUM(v.valor) AS total_vendas
            FROM vendas v
            GROUP BY 1
            ORDER BY 1;
        """
    

    def process_data(self, df):
        df = df.sort_values("periodo").reset_index(drop=True)

        crescimento = [0]  
        for i in range(1, len(df)):
            valor_anterior = df.loc[i - 1, "total_vendas"]
            valor_atual = df.loc[i, "total_vendas"]

            if valor_anterior == 0:
                variacao = 0
            else:
                variacao = ((valor_atual - valor_anterior) / valor_anterior) * 100

            crescimento.append(round(variacao, 2))

        df["crescimento_%"] = crescimento

        df = df.iloc[2:].reset_index(drop=True)

        return df[["periodo", "crescimento_%"]]


    def get_chart_type(self):
        return "bar"
