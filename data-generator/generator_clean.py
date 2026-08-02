import random
import time
from datetime import datetime
from faker import Faker
import psycopg2

fake = Faker()

DB_CONFIG = {
    
    "host": "localhost",
    "port": 5432,
    "database": "fraud_db",
    "user": "fraud_user",
    "password": "fraud_password",
}

ACCOUNT_TYPES = ["checking", "savings", "business"]
TXN_TYPES = ["deposit", "withdrawal", "transfer", "payment"]
MERCHANT_CATEGORIES = ["grocery", "fuel", "travel", "electronics", "restaurant", "online"]
STATUSES = ["success", "failed", "pending"]
CURRENCIES = ["EUR", "USD", "INR"]


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def create_customer(cur):
    cur.execute(
        """
        INSERT INTO customers 
        (first_name, last_name, email, phone, country, city)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING customer_id;
        """,
        (
            fake.first_name(),
            fake.last_name(),
            fake.unique.email(),
            fake.phone_number()[:30],
            fake.country(),
            fake.city(),
        ),
    )
    return cur.fetchone()[0]


def create_account(cur, customer_id):
    cur.execute(
        """
        INSERT INTO accounts 
        (customer_id, account_type, balance, currency, status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING account_id;
        """,
        (
            customer_id,
            random.choice(ACCOUNT_TYPES),
            round(random.uniform(100, 50000), 2),
            random.choice(CURRENCIES),
            "active",
        ),
    )
    return cur.fetchone()[0]


def create_transaction(cur, customer_id, account_id):
    amount = round(random.uniform(5, 5000), 2)

    is_fraud = amount > 4000 or random.random() < 0.03

    cur.execute(
        """
        INSERT INTO transactions
        (
            account_id,
            customer_id,
            transaction_type,
            amount,
            currency,
            merchant,
            merchant_category,
            transaction_status,
            transaction_timestamp,
            country,
            city,
            is_fraud
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """,
        (
            account_id,
            customer_id,
            random.choice(TXN_TYPES),
            amount,
            random.choice(CURRENCIES),
            fake.company(),
            random.choice(MERCHANT_CATEGORIES),
            random.choice(STATUSES),
            datetime.now(),
            fake.country(),
            fake.city(),
            is_fraud,
        ),
    )


def seed_initial_data(num_customers=20):
    conn = get_connection()
    cur = conn.cursor()

    customers_accounts = []

    for _ in range(num_customers):
        customer_id = create_customer(cur)
        account_id = create_account(cur, customer_id)
        customers_accounts.append((customer_id, account_id))

    conn.commit()
    cur.close()
    conn.close()

    return customers_accounts


def stream_transactions(customers_accounts):
    conn = get_connection()
    cur = conn.cursor()

    while True:
        customer_id, account_id = random.choice(customers_accounts)
        create_transaction(cur, customer_id, account_id)
        conn.commit()
        print(f"Inserted transaction for customer={customer_id}")
        time.sleep(2)


if __name__ == "__main__":
    customers_accounts = seed_initial_data()
    stream_transactions(customers_accounts)
