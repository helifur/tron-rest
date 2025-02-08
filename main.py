import datetime
import requests
from typing import Dict, TypedDict

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.db.db_session import global_init
from app.db.db_session import create_session
from app.models.transactions import Transaction

app = FastAPI()

global_init()


class AccountInfo(TypedDict):
    """
    Object representing a dict with bandwidth, energy and balance (TRON account parameters)
    Attributes:
        bandwidth: TRON account bandwidth remaining
        energy: TRON account energy remaining
        balance: TRON account balance
    """

    bandwidth: int
    energy: int
    balance: float


@app.get("/info")
def read_info(limit: int = 0, offset: int = 0):
    """
    Get list of last transactions with pagination
    Args:
        limit: number of entries
        offset: number representing the shift

    Returns:
        Dict with limit, offset and transactions
    """
    statement = select(Transaction).offset(offset)

    if limit:
        statement = statement.limit(limit)

    with create_session() as session:
        res = session.scalars(statement).all()

    return {"limit": limit, "offset": offset, "transactions": res}


@app.post("/info/{address}")
def write_info(address: str) -> AccountInfo:
    """
    Get account information and write the address in the database
    Args:
        address: TRON account address

    Returns:
        Dict with bandwidth, energy and account balance
    """
    data: AccountInfo = {"bandwidth": 0, "energy": 0, "balance": 0.0}
    response: Dict = requests.get(
        f"https://apilist.tronscanapi.com/api/accountv2?address={address}"
    ).json()

    data["bandwidth"] = (
        response["bandwidth"]["netRemaining"]
        + response["bandwidth"]["freeNetRemaining"]
    )
    data["energy"] = response["bandwidth"]["energyRemaining"]
    data["balance"] = response["balance"] / 1_000_000

    with create_session() as session:
        test = Transaction(
            address=address,
            time=datetime.datetime.now(),
        )

        session.add(test)
        session.commit()

    return data
