# 📊 Dashboard de Vendas — Streamlit + PostgreSQL

Aplicação interativa desenvolvida em **Python (Streamlit)** para análise de dados de vendas em múltiplas dimensões — produto, vendedor, região e período.  
O sistema oferece visualização dinâmica e filtrável dos indicadores, integração com banco de dados **PostgreSQL** através de consulta em SQL nativo e importação automatizada via arquivos **CSV**.

---

## 🚀 Funcionalidades Principais

✅ Importação de dados via arquivo `.csv`  
✅ Armazenamento automático no banco PostgreSQL  
✅ Dashboard interativo com gráficos dinâmicos  
✅ Filtros por período, vendedor, região e produto  
✅ Cálculo de ticket médio e índice de crescimento  
✅ Layout modular e escalável com orientação a objetos  

---

📦 Projeto_Dashboard/
│
├── app.py                                ***# Main da aplicação***
│
├── requirements.txt                       ***# Dependências do projeto***
├── README.md                              ***# Documentação do projeto***
│
├── docker/
│   └── docker-compose.yml                 ***# Configuração dos containers (PostgreSQL + PgAdmin)***
│
├── db/
│   ├── connection.py                     ***# Classe de conexão com o banco PostgreSQL***
│   ├── create_tables.sql                 ***# Script de criação das tabelas do banco de dados***
│   ├── import_csv.py                     ***# Classe para importar e validar arquivos CSV***
│   └── upload_manager.py                 ***# Classe que gerencia uploads e organização dos arquivos***
│
├── data/
│   ├── processed/                        ***# Armazena CSVs já importados para o banco***
│   │
│   └── uploads/                          ***# Armazena CSVs recém-enviados (aguardando importação)***
│
├── dashboard/
│   ├── components/                       
│   │   ├── base_chart.py                           ***# Super Classe para a consulta SQL e renderização de gráficos***
│   │   ├── filter_repository.py                   ***# Classe que busca opções de filtros no banco (vendedores, produtos, regiões)***
│   │   ├── sales_average_ticket_region_chart.py    ***# Gráfico de ticket médio por região***
│   │   ├── sales_average_ticket_seller_chart.py   ***# Gráfico de ticket médio por vendedor***
│   │   ├── sales_by_product_chart.py     ***# Gráfico comparativo de vendas por produto***
│   │   ├── sales_by_region_chart.py      ***# Gráfico comparativo de vendas por região***
│   │   ├── sales_by_seller_chart.py      ***# Gráfico comparativo de vendas por vendedor***
│   │   ├── sales_growth_index_chart.py   ***# Gráfico de índice de crescimento percentual***
│   │   ├── sales_over_time_chart.py      ***# Gráfico de vendas ao longo do tempo***
│   │   └── top_selling_products_chart.py ***# Gráfico de produtos mais vendidos***
│   │
│   ├── css/
│   │   └── styles.css                     ***# Arquivo de estilo (Personalização da página inicial do streamlit)***
│   │
│   ├── dashboard_manager.py               ***# Classe que controla os gráficos e filtros do dashboard principal***
│   └── home_screen.py                     ***# Tela inicial do sistema (menu principal e navegação)***

---
## 🗄️ Estrutura do Banco de Dados

![Diagrama do Banco de Dados](db/estrutura_banco.png)

---

## 📈 Gráficos Disponíveis

| **Gráfico** | **Descrição** |
|--------------|---------------|
| **Produtos mais vendidos** | Soma de vendas por produto. |
| **Vendas por período** | Evolução temporal das vendas. |
| **Comparativo entre vendedores** | Ranking de desempenho. |
| **Comparativo entre produtos** | Comparação de volume e valor. |
| **Comparativo entre regiões** | Distribuição geográfica das vendas. |
| **Índice de crescimento** | Crescimento percentual mês a mês. |
| **Ticket médio por vendedor** | Valor médio das vendas por vendedor. |
| **Ticket médio por região** | Valor médio das vendas por região. |

---

## 💾 CSV Suportado

O arquivo .csv deve ter a seguinte estrutura de colunas para ser importado com sucesso no projeto

| Data da Venda | Vendedor | Produto | Região | Valor |
|---------------|----------|---------|--------|-------|

Dados de novos vendedores, produtos ou região são incorporados automaticamente ao banco caso existam.

---
## ⚙️ Modo de Execução

O projeto é executado em modo híbrido, combinando containers Docker para os serviços de banco de dados e administração, enquanto o aplicativo Streamlit é executado localmente nas dependências do Python.

Os serviços de **PostgreSQL** e **PgAdmin 4** são inicializados a partir do arquivo `docker/docker-compose.yml`

```bash  
docker-compose up -d
```

***PostgreSQL:*** `localhost:5432`  
***PgAdmin:*** `http://localhost:5050`


Execução do app:
```bash 
pip install -r requirements.txt
streamlit run app.py 
```
---
#### 🧩 Requisitos

***Python 3.10 ou superior
Streamlit
Pandas
Plotly
Psycopg2
Docker***

---

#### 🧑‍💻 Autor

Bruno Flor de Lys
📍 Ribeirão Preto — SP
💼 Desenvolvedor
📧 brunolys23@gmail.com

---
#### 📜 Licença
Distribuído sob a licença MIT.
Você é livre para usar, modificar e distribuir este projeto com os devidos créditos.

---
#### ✨ Observação

Este projeto foi estruturado seguindo princípios de:
Arquitetura limpa e modular (OOP)
Responsabilidade única (cada classe cumpre uma função)
Extensibilidade fácil — adicionar novos gráficos requer apenas uma nova subclasse.

---