import json

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

    def get_wallet_id_by_address(self, address):
        with self.session() as session:
            stmt = select(Wallets.id).where(Wallets.address == address)
            return session.execute(stmt).scalar()

    def get_wallet_id_by_tg_id(self, tg_id):
        with self.session() as session:
            stmt = (
                select(Wallets.id)
                .join(Users)
                .where(Users.tg_id == tg_id)
            )
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

    def insert_withdrawal(self, data, currency_id, actual_wallet_id):
        with self.session() as session:
            label_data = json.loads(data['label'])
            params = {
                'amount': data['amount'],
                'currency_id': currency_id,
                'wallet_id': actual_wallet_id,
                'address_from': data['from'],
                'address_to': data['to'],
                'txid': data['txid'],
                'tg_id_from': label_data['tg_id'],
                'abs_bot_commission': label_data['bot_commission'],
                'state': True,
                'refund': False,
                'confirmation': data['confirmation'],
                'sign': data['sign'],
            }
            session.execute(insert(Withdrawals), params)

            total_amount = float(data['amount']) + float(label_data['bot_commission'])
            stmt = (
                update(Wallets)
                .where(
                    Wallets.user_id == Users.id,
                    Users.tg_id == label_data['tg_id'],
                    Wallets.currency_id == currency_id,
                )
                .values(frozen_amount=Wallets.frozen_amount - total_amount)
            )
            session.execute(stmt)

            session.commit()


database = Database()
