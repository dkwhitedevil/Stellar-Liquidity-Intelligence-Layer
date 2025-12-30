import warnings
from urllib3.exceptions import NotOpenSSLWarning

warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

from data_ingestion.horizon_client import get_server
from data_ingestion.snapshot_writer import write_snapshot
from config.stellar import DEFAULT_LIMIT, MAX_PAGES
import requests


def fetch_payments():
    server = get_server()
    records = []

    response = server.payments().limit(DEFAULT_LIMIT).order(desc=True).call()

    for _ in range(MAX_PAGES):
        records.extend(response["_embedded"]["records"])
        next_link = response["_links"]["next"]["href"]
        response = requests.get(next_link).json()

    snapshot = {
        "type": "payments",
        "count": len(records),
        "records": records
    }

    return write_snapshot("payments", snapshot)


if __name__ == "__main__":
    path = fetch_payments()
    print(f"Saved payments snapshot → {path}")