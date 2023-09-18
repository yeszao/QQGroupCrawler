import os

TZ = os.getenv("TZ", "Asia/Shanghai")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "12345678")
DB_NAME = os.getenv("DB_NAME", "runlala_clients")
DB_PORT = os.getenv("DB_PORT", 3306)

