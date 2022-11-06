from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

bankDatabase = SQLAlchemy()

engine = create_engine('sqlite:///data.db', connect_args={'check_same_thread': False}, echo=True)
bankDatabase.metadata.bind = engine
bank_db = scoped_session(sessionmaker(bind=engine))
