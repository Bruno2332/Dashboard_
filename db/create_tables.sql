CREATE TABLE regioes (
    id_regiao SERIAL PRIMARY KEY,
    nome VARCHAR(50) UNIQUE NOT NULL
);


CREATE TABLE produtos (
    id_produto SERIAL PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL
);


CREATE TABLE vendedores (
    id_vendedor SERIAL PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL
);


CREATE TABLE vendas (
    id_venda SERIAL PRIMARY KEY,
    data_venda DATE NOT NULL,
    id_vendedor INT NOT NULL REFERENCES vendedores(id_vendedor),
    id_produto INT NOT NULL REFERENCES produtos(id_produto),
    id_regiao INT NOT NULL REFERENCES regioes(id_regiao),
    valor NUMERIC(10,2) NOT NULL
);