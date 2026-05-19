CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE customers (
    customer_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(30),
    country VARCHAR(80),
    city VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE accounts (
    account_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID NOT NULL REFERENCES customers(customer_id),
    account_type VARCHAR(50),
    balance NUMERIC(15,2),
    currency VARCHAR(10),
    status VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    transaction_id UUID DEFAULT uuid_generate_v4(),
    account_id UUID NOT NULL,
    customer_id UUID NOT NULL,
    transaction_type VARCHAR(50),
    amount NUMERIC(15,2),
    currency VARCHAR(10),
    merchant VARCHAR(150),
    merchant_category VARCHAR(100),
    transaction_status VARCHAR(30),
    transaction_timestamp TIMESTAMP NOT NULL,
    country VARCHAR(80),
    city VARCHAR(100),
    is_fraud BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (transaction_id, transaction_timestamp)
) PARTITION BY RANGE (transaction_timestamp);

CREATE TABLE transactions_2026_05 PARTITION OF transactions
FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');

CREATE TABLE transactions_2026_06 PARTITION OF transactions
FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');

CREATE INDEX idx_transactions_customer_id
ON transactions(customer_id);

CREATE INDEX idx_transactions_account_id
ON transactions(account_id);

CREATE INDEX idx_transactions_timestamp
ON transactions(transaction_timestamp);