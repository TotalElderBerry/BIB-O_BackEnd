from sqlalchemy import create_engine,text


driver =  'mysql+pymysql://'
username = "root"
password = "@"
host = "localhost/"
database = "bibo_db"

engine = create_engine(driver+username+password+host+database, echo = True)

