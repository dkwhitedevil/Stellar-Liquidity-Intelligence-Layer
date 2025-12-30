import pandas as pd
from signal_processing.signal_schema import Signal


def extract_ledger_dynamics(snaps):
    signals = []

    for snap in snaps:
        r = snap.get("records")
        if not r:
            continue

        df = pd.DataFrame(r)
        df["ts"] = pd.to_datetime(df["closed_at"])

        signals.append(
            Signal(
                df["ts"].max(),
                "NETWORK",
                "throughput",
                "ledger_count",
                float(len(df)),
                "count",
                "ledgers",
            )
        )

    return signals
