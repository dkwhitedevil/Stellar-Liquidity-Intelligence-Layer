import warnings
from urllib3.exceptions import NotOpenSSLWarning

warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

from stellar_sdk import Asset
from data_ingestion.horizon_client import get_server
from data_ingestion.snapshot_writer import write_snapshot
from data_ingestion.assets import asset_to_dict

def fetch_orderbook(selling: Asset, buying: Asset):
    server = get_server()

    response = server.orderbook(
        selling=selling,
        buying=buying
    ).call()

    snapshot = {
        "type": "orderbook",
        "selling": asset_to_dict(selling),
        "buying": asset_to_dict(buying),
        "horizon_response": response
    }

    return write_snapshot("orderbooks", snapshot)

if __name__ == "__main__":
    # ✅ Native ↔ Native (always valid)
    selling = Asset.native()
    buying = Asset.native()

    path = fetch_orderbook(selling, buying)
    print(f"Saved orderbook snapshot → {path}")
