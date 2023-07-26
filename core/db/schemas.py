from sqlalchemy import ForeignKey, String, func
from sqlalchemy.dialects.mysql import DATETIME, DOUBLE
from sqlalchemy.orm import Mapped, as_declarative, mapped_column, relationship

from bot.common import constants


@as_declarative()
class Base:
    __name__: str
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Dates:
    created_at = mapped_column(DATETIME, default=func.now())
    updated_at = mapped_column(DATETIME, onupdate=func.now())


class Users(Base, Dates):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(unique=True, comment="Telegram id")
    username: Mapped[str] = mapped_column(String(100), comment="Telegram login")
    phone: Mapped[str] = mapped_column(String(100), nullable=True)
    is_banned: Mapped[bool] = mapped_column(default=False)

    wallet = relationship("Wallets", back_populates="user")


class UserSettings(Base, Dates):
    __tablename__ = "user_settings"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    language: Mapped[str] = mapped_column(String(2), default="RU")
    local_currency: Mapped[str] = mapped_column(String(3), default="RUB")

    user = relationship("Users", foreign_keys=[user_id])


class Wallets(Base, Dates):
    __tablename__ = "wallets"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"))
    amount = mapped_column(DOUBLE, nullable=False, default=0.00)
    frozen_amount = mapped_column(DOUBLE, nullable=False, default=0.00)

    address = relationship("Addresses", back_populates="wallet")
    user = relationship("Users", back_populates="wallet")


class Addresses(Base, Dates):
    __tablename__ = "addresses"

    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"))
    address: Mapped[str] = mapped_column(String(80), nullable=False)
    name: Mapped[str] = mapped_column(
        String(30), default=constants.DEPOSIT['main_address']
    )
    qr_code: Mapped[str] = mapped_column(String(200))

    wallet = relationship("Wallets", back_populates="address")


class Currencies(Base):
    __tablename__ = "currencies"

    name: Mapped[str] = mapped_column(String(50))


class Withdrawals(Base, Dates):
    __tablename__ = "withdrawals"

    amount = mapped_column(DOUBLE, nullable=False)
    currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"))
    address_from: Mapped[str] = mapped_column(String(80))
    address_to: Mapped[str] = mapped_column(String(80))
    aml: Mapped[str] = mapped_column(String(10), nullable=True)
    txid: Mapped[str] = mapped_column(String(100))
    tg_id_from: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))
    abs_bot_commission: Mapped[float]
    state: Mapped[bool]
    gate: Mapped[str] = mapped_column(String(50), nullable=True)
    refund: Mapped[bool]
    chat_id: Mapped[int] = mapped_column(nullable=True)
    message_id: Mapped[int] = mapped_column(nullable=True)
    chat_name: Mapped[str] = mapped_column(String(100), nullable=True)
    confirmation: Mapped[int]
    sign: Mapped[str] = mapped_column(String(50))
    is_user_notified: Mapped[bool] = mapped_column(default=False)

    currency = relationship("Currencies", foreign_keys=[currency_id])


class Deposits(Base, Dates):
    __tablename__ = "deposits"

    amount = mapped_column(DOUBLE, nullable=False)
    currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"))
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    address_from: Mapped[str] = mapped_column(String(80))
    aml: Mapped[str] = mapped_column(String(10), nullable=True)
    txid: Mapped[str] = mapped_column(String(100), comment="hash")
    state: Mapped[bool]
    sign: Mapped[str] = mapped_column(String(50))
    is_user_notified: Mapped[bool] = mapped_column(default=False)

    currency = relationship("Currencies", foreign_keys=[currency_id])


class Commissions(Base, Dates):
    __tablename__ = "commissions"

    amount = mapped_column(DOUBLE, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"))
    is_active: Mapped[bool] = mapped_column(default=True)

    user = relationship("Users", foreign_keys=[user_id])
    currency = relationship("Currencies", foreign_keys=[currency_id])


class Exchanges(Base, Dates):
    __tablename__ = "exchanges"

    amount = mapped_column(DOUBLE, nullable=False)
    rate = mapped_column(DOUBLE, nullable=False)
    address_id_from: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    address_id_to: Mapped[int] = mapped_column(ForeignKey("addresses.id"))

    address_from = relationship("Addresses", foreign_keys=[address_id_from])
    address_to = relationship("Addresses", foreign_keys=[address_id_to])


class Comments(Base, Dates):
    __tablename__ = "comments"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    comment: Mapped[str] = mapped_column(String(250))

    user = relationship("Users", foreign_keys=[user_id])


class GlobalParameters(Base):
    __tablename__ = 'global_parameters'

    name: Mapped[str] = mapped_column(String(50))
    value: Mapped[float]
