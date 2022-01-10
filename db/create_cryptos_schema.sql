CREATE DATABASE cryptos;
\c cryptos

CREATE SCHEMA cryptos;

CREATE TABLE cryptos.exchange (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE cryptos.symbol (
    id SERIAL PRIMARY KEY,
    name TEXT,
    active BOOLEAN
);

CREATE TABLE cryptos.exchange_symbol (
    exchange_id INT NOT NULL REFERENCES cryptos.exchange ON DELETE CASCADE,
    symbol_id INT NOT NULL REFERENCES cryptos.symbol ON DELETE CASCADE,
    name TEXT,
    PRIMARY KEY (exchange_id, symbol_id)
);

CREATE TABLE IF NOT EXISTS cryptos.order(
    id SERIAL PRIMARY KEY,
    symbol_id INT NOT NULL,
    clientOrder_id TEXT,
    transactTime BIGINT,
    price FLOAT,
    origQty INTEGER,
    executedQty INTEGER,
    cummulativeQuoteQty INTEGER,
    status TEXT,
    timeInForce TEXT,
    type TEXT,
    side TEXT,
    CONSTRAINT fk_cryptos_symbol FOREIGN KEY (symbol_id) REFERENCES cryptos.symbol(id)
);

CREATE TABLE IF NOT EXISTS cryptos.fill(
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    qty INTEGER,
    commission FLOAT,
    commissionAsset TEXT,
    CONSTRAINT fk_cryptos_order FOREIGN KEY (order_id) REFERENCES cryptos.order(id)
);

CREATE TABLE IF NOT EXISTS cryptos.signal(
    id SERIAL PRIMARY KEY,
    symbol_id INT NOT NULL,
    signal TEXT,
    created_at BIGINT,
    rsi FLOAT,
    prev_rsi FLOAT,
    prev_created_at BIGINT,
    CONSTRAINT fk_cryptos_order FOREIGN KEY (symbol_id) REFERENCES cryptos.symbol(id)
);


