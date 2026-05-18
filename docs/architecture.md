# AI-Powered Real-Time Fraud Detection Lakehouse Platform

```mermaid
flowchart LR

    A[Python Faker Transaction Generator] --> B[(PostgreSQL OLTP Database)]

    B --> C[Debezium CDC Connector]
    C --> D[Apache Kafka Topics]

    D --> E[Spark Structured Streaming]

    E --> F[(MinIO / S3 Data Lake)]

    F --> G[Bronze Layer - Raw CDC Events]
    G --> H[Silver Layer - Cleaned Transactions]
    H --> I[Gold Layer - Fraud Features & Aggregates]

    I --> J[ML Training Pipeline]
    J --> K[MLflow Model Registry]

    D --> L[Real-Time Inference Service]
    K --> L

    L --> M[(Fraud Predictions Table)]

    I --> N[Analytics Dashboard]
    M --> N

    O[Apache Airflow] --> E
    O --> J
    O --> N

    P[GitHub Actions CI/CD] --> O