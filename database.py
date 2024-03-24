from sqlalchemy import create_engine, URL


database_url = URL.create(
    "mysql+pymysql", username="root", password="", host="localhost", database="bibo_db"
)

engine = create_engine(database_url, echo=True)
