from sqlalchemy import insert, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime

from core.db.schemas import Transaction
from core.config import settings


class Database:
    def __init__(self):
        engine = create_engine(settings.DB_URL)
        self.session = scoped_session(sessionmaker(bind=engine))

    def put_data(self, data):
        params = {
            'user_id': 12,
            'currency': data['currency'],
            'date': datetime.fromtimestamp(data['date']),
            'from_': data['from'],
            'to': data['to'],
            'amount': data['amount'],
            'fee': data['fee'],
            'txid': data['txid'],
            'confirmation': data['confirmation'],
            'sign': data['sign'],
        }
        with self.session() as session:
            session.execute(insert(Transaction), params)
            session.commit()


database = Database()
