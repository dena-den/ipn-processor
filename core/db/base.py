from sqlalchemy import select, insert, update, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from core.db.schemas import *
from core.config import settings


class Database:
    def __init__(self):
        engine = create_engine(settings.DB_URL)
        self.session = scoped_session(sessionmaker(bind=engine))

    def get_currency_id(self, name):
        with self.session() as session:
            stmt = select(Currencies.id).where(Currencies.name == name)
            return session.execute(stmt).scalar()

    def get_wallet_id(self, address):
        with self.session() as session:
            stmt = select(Wallets.id).where(Wallets.address == address)
            return session.execute(stmt).scalar()

    def insert_deposit(self, data, currency_id, wallet_id):
        with self.session() as session:
            params = {
                'amount': data['amount'],
                'currency_id': currency_id,
                'wallet_id': wallet_id,
                'address_from': data['from'],
                'address_to': data['to'],
                'txid': data['txid'],
                'state': True,
                'confirmation': data['confirmation'],
                'sign': data['sign'],
            }
            session.execute(insert(Deposits), params)

            stmt = update(Wallets).where(Wallets.id == wallet_id)\
                .values(amount=Wallets.amount + data['amount'])
            session.execute(stmt)

            session.commit()

    def insert_withdrawal(self, data, currency_id, wallet_id):
        with self.session() as session:
            params = {
                'amount': data['amount'],
                'currency_id': currency_id,
                'wallet_id': wallet_id,
                'address_from': data['from'],
                'address_to': data['to'],
                'txid': data['txid'],
                'tg_id_from': data['label'],
                'state': True,
                'refund': False,
                'confirmation': data['confirmation'],
                'sign': data['sign'],
            }
            session.execute(insert(Withdrawals), params)

            stmt = update(Wallets).where(Wallets.id == wallet_id)\
                .values(frozen_amount=Wallets.frozen_amount - data['amount'])
            session.execute(stmt)

            session.commit()


database = Database()
