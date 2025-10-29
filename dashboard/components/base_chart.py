from abc import ABC, abstractmethod
import pandas as pd
import streamlit as st
import plotly.express as px
import re
from datetime import datetime, timedelta


class BaseChart(ABC):

    period_permission = True
    sellers_permission = True
    region_permission = True
    product_permission = True

    def __init__(self, db, title, color_scale="Blues"):
        self.db = db
        self.title = title
        self.color_scale = color_scale
        

    
    @abstractmethod
    def get_query(self, **kwargs):
        pass


    @abstractmethod
    def get_chart_type(self):
        pass


    def filter_permission(self, period=True, sellers=True, region=True, product=True):
        return


    def _inject_where_before_group_order(self, sql, where_sql):
        s = sql.strip().rstrip(";")
        m = re.search(r"\b(GROUP\s+BY|ORDER\s+BY|LIMIT)\b", s, flags=re.IGNORECASE)
        if m:
            idx = m.start()
            return f"{s[:idx].rstrip()} {where_sql} {s[idx:].lstrip()}"
        else:
            return f"{s} {where_sql}"


    def fetch_data(self, **filters):
        base_query = self.get_query(**filters)
        where_clauses = []
        params = []

        period = filters.get("period")
        if period and period != "Todo o período" and self.period_permission:
            map_days = {"Último mês": 30, 
                        "Últimos 3 meses": 90, 
                        "Últimos 6 meses": 180, 
                        "Último ano": 365}
            days = map_days.get(period, 0)
            limit_date = datetime.now() - timedelta(days=days)
            where_clauses.append("v.data_venda >= %s")
            params.append(limit_date)
            
        
        sellers = filters.get("sellers") or []
        regions = filters.get("regions") or []
        products = filters.get("products") or []

        if sellers and "Todos" not in sellers and self.sellers_permission:
            where_clauses.append(
                "v.id_vendedor IN (SELECT id_vendedor FROM vendedores WHERE nome = %s)"
            )
            params.append(sellers)

        if regions and "Todas" not in regions and self.region_permission:
            where_clauses.append(
                "v.id_regiao IN (SELECT id_regiao FROM regioes WHERE nome = %s)"
            )
            params.append(regions)

        if products and "Todos" not in products and self.product_permission:
            where_clauses.append(
                "v.id_produto IN (SELECT id_produto FROM produtos WHERE nome = %s)"
            )
            params.append(products)

       
        final_query = base_query.strip().rstrip(";")

        if where_clauses:
            where_sql = "WHERE " + " AND ".join(where_clauses)
            
            if re.search(r"\bWHERE\b", final_query, flags=re.IGNORECASE):
                
                final_query = re.sub(
                    r"\bWHERE\b",
                    "WHERE " + " AND ".join(where_clauses) + " AND ",
                    final_query,
                    count=1,
                    flags=re.IGNORECASE,
                )
            else:
                final_query = self._inject_where_before_group_order(final_query, where_sql)

        final_query = final_query.strip().rstrip(";") + ";"

        try:
            df = pd.read_sql(final_query, self.db.conn, params=params)
        except Exception as e:
            st.error(f"Erro ao buscar dados: {e}\n\nSQL gerada:\n{final_query}\nParams: {params}")
            return pd.DataFrame()

        return df


    def render(self, **kwargs):
        df = self.fetch_data(**kwargs)

        if not isinstance(df, pd.DataFrame) or df.empty:
            st.warning("Nenhum dado disponível para exibir")
            return
        
        if hasattr(self, "process_data"):
            df = self.process_data(df)
        
        chart_type = self.get_chart_type()

        if chart_type == "bar":
            fig = px.bar(df, x=df.columns[0], y=df.columns[1], text_auto=True,
                     title=self.title, color=df.columns[1], color_continuous_scale=self.color_scale)

        elif chart_type == "line":
            fig = px.line(df, x=df.columns[0], y=df.columns[1], markers=True, title=self.title)

        elif chart_type == "pie":
            fig = px.pie(df, names=df.columns[0], values=df.columns[1],
                        hole=0.4, title=self.title)

        elif chart_type == "area":
            fig = px.area(df, x=df.columns[0], y=df.columns[1], title=self.title)

        elif chart_type == "histogram":
            fig = px.histogram(df, x=df.columns[0], y=(df.columns[1] if len(df.columns) > 1 else None),
                            title=self.title, color=df.columns[0])

        else:
            raise ValueError(f"Tipo de gráfico não suportado: {chart_type}")

        st.plotly_chart(fig, use_container_width=True)


    
    

