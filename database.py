from sqlalchemy import create_engine

driver =  'mysql+pymysql://'
username = "root"
password = "@"
host = "localhost/"
database = "bibo_db"

engine = create_engine(driver+username+password+host+database, echo = True)

