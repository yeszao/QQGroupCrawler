import os

TZ = os.getenv("TZ", "Asia/Shanghai")

DB_HOST = os.getenv("DB_HOST", "ls-267436b87a306125d62e5df0db4efa05b5c46247.cdq5d5kn9hp4.ap-southeast-1.rds.amazonaws.com")
DB_USER = os.getenv("DB_USER", "rllroot")
DB_PASS = os.getenv("DB_PASS", "dbrll_Admin_2023")
DB_NAME = os.getenv("DB_NAME", "runlala_clients")
DB_PORT = os.getenv("DB_PORT", 3306)
