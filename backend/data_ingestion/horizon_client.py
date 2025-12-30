from stellar_sdk import Server
from config.stellar import HORIZON_URL


def get_server() -> Server:
    """
    Returns a configured Horizon server client.
    Enforced read-only usage.
    """
    return Server(horizon_url=HORIZON_URL)
