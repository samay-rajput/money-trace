from typing import TypedDict


class Transaction(TypedDict, total=False):
    date: str
    description: str
    merchant: str
    amount: float
    transaction_type: str
    category: str
