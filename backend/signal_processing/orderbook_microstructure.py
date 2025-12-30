from datetime import datetime
from signal_processing.signal_schema import Signal

DEPTH_LEVELS = 10


def extract_orderbook_microstructure(snaps):
    signals = []

    for snap in snaps:
        # Locate the orderbook-like dict without referencing provider-specific keys
        book = None
        for v in snap.values():
            if isinstance(v, dict) and "bids" in v and "asks" in v:
                book = v
                break
        if not book:
            continue

        bids, asks = book.get("bids", []), book.get("asks", [])
        if not bids or not asks:
            continue

        # Use deterministic timestamp from snapshot filename when present
        snapshot_time = snap.get("__snapshot_time")
        if snapshot_time:
            try:
                ts = datetime.fromisoformat(snapshot_time)
            except Exception:
                ts = datetime(1970, 1, 1)
        else:
            ts = datetime(1970, 1, 1)

        pair = "ORDERBOOK"

        best_bid = float(bids[0]["price"])
        best_ask = float(asks[0]["price"])

        bid_depth = float(sum(float(b["amount"]) for b in bids[:DEPTH_LEVELS]))
        ask_depth = float(sum(float(a["amount"]) for a in asks[:DEPTH_LEVELS]))

        total_depth = bid_depth + ask_depth
        if total_depth == 0:
            imbalance = 0.0
        else:
            imbalance = float((bid_depth - ask_depth) / total_depth)

        signals.extend([
            Signal(ts, pair, "liquidity", "spread", float(best_ask - best_bid), "price", "orderbook"),
            Signal(ts, pair, "liquidity", "bid_depth", bid_depth, "units", "orderbook"),
            Signal(ts, pair, "liquidity", "ask_depth", ask_depth, "units", "orderbook"),
            Signal(ts, pair, "liquidity", "imbalance", imbalance, "ratio", "orderbook"),
        ])

    return signals
