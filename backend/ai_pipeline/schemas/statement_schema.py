from typing import List, Optional, Literal

from pydantic import BaseModel, Field


class Transaction(BaseModel):
    date: str

    description: str

    amount: float = Field(gt=0)

    type: Literal["debit", "credit"]

    balance: Optional[float] = None


class Account(BaseModel):
    account_number: Optional[str] = None

    transactions: List[Transaction]


class Statement(BaseModel):
    accounts: List[Account]