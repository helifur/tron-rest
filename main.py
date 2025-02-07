import datetime
import requests
from typing import Dict, TypedDict

from fastapi import FastAPI

from app.db.db_session import global_init
from app.db.db_session import create_session
from app.models.transactions import Transaction

app = FastAPI()

global_init()


class AccountInfo(TypedDict):
    bandwidth: int
    energy: int
    balance: float


@app.get("/")
def read_root():
    return {"Hello": 1}


@app.post("/getinfo/{address}")
def get_info(address: str) -> AccountInfo:
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
