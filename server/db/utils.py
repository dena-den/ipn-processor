from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import insert, select
from os import getenv

from schemas import *
from datetime import datetime


class Database:
    engine = create_async_engine(url=getenv('DB_URL'), echo=True)
    session_pool = async_sessionmaker(engine, expire_on_commit=False)

    async def put_data(self, data):
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
        async with self.session_pool() as session:
            await session.execute(insert(Transaction), params)
            await session.commit()


database = Database()
