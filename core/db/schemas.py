from sqlalchemy import ForeignKey, String, func
from sqlalchemy.dialects.mysql import DATETIME, DOUBLE
from sqlalchemy.orm import Mapped, as_declarative, mapped_column, relationship


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
    phone: Mapped[str] = mapped_column(String(100), default='')
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
    address: Mapped[str] = mapped_column(String(34), default='')

    user = relationship("Users", back_populates="wallet")


class Currencies(Base):
    __tablename__ = "currencies"

    name: Mapped[str] = mapped_column(String(50))


class Withdrawals(Base, Dates):
    __tablename__ = "withdrawals"

    amount = mapped_column(DOUBLE, nullable=False)
    currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"))
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"))
    address_from: Mapped[str] = mapped_column(String(34))
    address_to: Mapped[str] = mapped_column(String(34))
    aml: Mapped[str] = mapped_column(String(10), default='')
    txid: Mapped[str] = mapped_column(String(100), comment="hash")
    tg_id_from: Mapped[int]
    state: Mapped[bool]
    gate: Mapped[str] = mapped_column(String(50), default='')
    refund: Mapped[bool]
    chat_id: Mapped[int] = mapped_column(default=0)
    message_id: Mapped[int] = mapped_column(default=0)
    chat_name: Mapped[str] = mapped_column(String(100), default='')
    sign: Mapped[str] = mapped_column(String(50))
    is_user_notified: Mapped[bool] = mapped_column(default=False)

    currency = relationship("Currencies", foreign_keys=[currency_id])
    wallet = relationship("Wallets", foreign_keys=[wallet_id])


class Deposits(Base, Dates):
    __tablename__ = "deposits"

    amount = mapped_column(DOUBLE, nullable=False)
    currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"))
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"))
    address_from: Mapped[str] = mapped_column(String(34))
    address_to: Mapped[str] = mapped_column(String(34))
    aml: Mapped[str] = mapped_column(String(10), default='')
    txid: Mapped[str] = mapped_column(String(100), comment="hash")
    state: Mapped[bool]
    sign: Mapped[str] = mapped_column(String(50))
    is_user_notified: Mapped[bool] = mapped_column(default=False)

    currency = relationship("Currencies", foreign_keys=[currency_id])
    wallet = relationship("Wallets", foreign_keys=[wallet_id])


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
    wallet_id_from: Mapped[int] = mapped_column(ForeignKey("wallets.id"))
    wallet_id_to: Mapped[int] = mapped_column(ForeignKey("wallets.id"))

    wallet_from = relationship("Wallets", foreign_keys=[wallet_id_from])
    wallet_to = relationship("Wallets", foreign_keys=[wallet_id_to])


class Comments(Base, Dates):
    __tablename__ = "comments"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    comment: Mapped[str] = mapped_column(String(250))

    user = relationship("Users", foreign_keys=[user_id])
