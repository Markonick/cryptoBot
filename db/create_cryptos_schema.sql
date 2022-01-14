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
    active BOOLEAN,
    UNIQUE (name)
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
    clientOrder_id INT,
    transactTime BIGINT,
    price FLOAT,
    origQty INTEGER,
    executedQty INTEGER,
    cummulativeQuoteQty INTEGER,
    status TEXT,
    timeInForce TEXT,
    type TEXT,
    side TEXT,
    CONSTRAINT fk_order_cryptos_symbol FOREIGN KEY (symbol_id) REFERENCES cryptos.symbol(id)
);
CREATE INDEX IF NOT EXISTS ix_cryptos_order_symbol ON cryptos.order(symbol_id);

CREATE TABLE IF NOT EXISTS cryptos.fill(
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    qty INTEGER,
    commission FLOAT,
    commissionAsset TEXT,
    CONSTRAINT fk_cryptos_fill_order FOREIGN KEY (order_id) REFERENCES cryptos.order(id)
);
CREATE INDEX IF NOT EXISTS ix_cryptos_fill_order ON cryptos.fill(order_id);

CREATE TABLE IF NOT EXISTS cryptos.signal(
    id SERIAL PRIMARY KEY,
    symbol_id INT NOT NULL,
    order_id INT,
    value TEXT,
    curr_rsi FLOAT,
    prev_rsi FLOAT,
    created_at BIGINT,
    CONSTRAINT fk_cryptos_signal_symbol FOREIGN KEY (symbol_id) REFERENCES cryptos.symbol(id),
    CONSTRAINT fk_cryptos_signal_order FOREIGN KEY (order_id) REFERENCES cryptos.order(id)
);
CREATE INDEX IF NOT EXISTS ix_cryptos_signal_symbol ON cryptos.signal(symbol_id);
CREATE INDEX IF NOT EXISTS ix_cryptos_signal_order ON cryptos.signal(order_id);
