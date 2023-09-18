from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


from config import DB_USER, DB_PASS, DB_HOST, DB_NAME, DB_PORT


# Create an engine to connect to the MySQL database
DbEngine = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4',
                         pool_pre_ping=True,
                         pool_size=10,
                         pool_recycle=3600)

# Create a session factory
DbSession = sessionmaker(bind=DbEngine)

# Create a base class for declarative models
Base = declarative_base()

