import pandas as pd
from signal_processing.signal_schema import Signal
from signal_processing.time_alignment import align_to_window


def extract_payment_flow(snaps):
    signals = []

    for snap in snaps:
        r = snap.get("records")
        if not r:
            continue

        df = pd.DataFrame(r)
        df["ts"] = pd.to_datetime(df["created_at"])
        df = align_to_window(df, "ts")

        for w, g in df.groupby("window"):
            signals.append(
                Signal(w, "NETWORK", "flow", "payment_count", float(len(g)), "count", "payments")
            )

    return signals
