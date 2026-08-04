#Modul_4\Cinescope\db_requester\models.py
# Модель для таблицы accounts_transaction_template
from sqlalchemy import Column, String, Boolean, DateTime, ARRAY, Enum as SAEnum,INTEGER,Float, Integer
from sqlalchemy.orm import declarative_base
from typing import Dict, Any
from constants.roles import Roles

Base = declarative_base()
class AccountTransactionTemplate(Base):
    __tablename__ = 'accounts_transaction_template'
    user = Column(String, primary_key=True)
    balance = Column(Integer, nullable=False)