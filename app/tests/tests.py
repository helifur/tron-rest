from fastapi.testclient import TestClient
import datetime
from unittest.mock import MagicMock, patch

from app.db.db_session import create_session
from main import app, write_info
from app.models.transactions import Transaction

client = TestClient(app)


@patch("main.create_session")
@patch("main.requests.get")
def test_write_info(mock_requests_get: MagicMock, mock_create_session: MagicMock):
    """
    Unit test: check if the item is added to the database.
    Args:
        mock_requests_get: mock for requests.get method
        mock_create_session: mock for create_session function
    """
    mock_session = MagicMock()
    mock_create_session.return_value.__enter__.return_value = mock_session
    address = "test_address"

    mock_requests_get.return_value.json.return_value = {
        "bandwidth": {
            "netRemaining": 500,
            "freeNetRemaining": 600,
            "energyRemaining": 400,
        },
        "balance": 156000,
    }

    print(write_info(address))

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

    transaction = mock_session.add.call_args[0][0]

    assert isinstance(transaction, Transaction)
    assert transaction.address == address


def test_read_info():
    """Integration test for checking list of transactions with pagination"""

    candidates = [
        Transaction(address=f"address_{i}", time=datetime.datetime.now())
        for i in range(5)
    ]

    with create_session() as session:
        session.add_all(candidates)
        session.commit()

        # get db len
        db_len = session.query(Transaction).count()

    res = client.get(f"/info/?limit=5&offset={db_len - 5}")
    assert res.status_code == 200

    res = res.json()
    assert "transactions" in res

    res = res["transactions"]

    assert len(res) == 5
    assert res[1]["address"] == "address_1"

    # delete test transactions
    with create_session() as session:
        for elem in candidates:
            session.delete(elem)

        session.commit()
