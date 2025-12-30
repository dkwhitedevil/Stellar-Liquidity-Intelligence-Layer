import pandas as pd
import numpy as np
from signal_processing.signal_schema import Signal
from signal_processing.time_alignment import align_to_window


def extract_trade_microstructure(trade_snaps):
    signals = []

    for snap in trade_snaps:
        r = snap.get("records")
        if not r:
            continue

        df = pd.DataFrame(r)
        df["ts"] = pd.to_datetime(df["ledger_close_time"])
        # price is a rational object with n/d
        df["price"] = df["price"].apply(lambda p: float(p["n"]) / float(p["d"]))
        df["amount"] = df["base_amount"].astype(float)

        df = align_to_window(df, "ts")

        for w, g in df.groupby("window"):
            pair = f"{g.iloc[0]['base_asset_type']}/{g.iloc[0]['counter_asset_type']}"

            trade_count = float(len(g))
            trade_volume = float(g["amount"].sum())
            vwap = float(((g["price"] * g["amount"]).sum() / g["amount"].sum())) if g["amount"].sum() != 0 else float('nan')
            price_std = float(g["price"].std(ddof=0)) if len(g) > 1 else float('nan')

            signals.extend([
                Signal(w, pair, "activity", "trade_count", trade_count, "count", "trades"),
                Signal(w, pair, "liquidity", "trade_volume", trade_volume, "units", "trades"),
                Signal(w, pair, "price", "vwap", vwap, "price", "trades"),
                Signal(w, pair, "volatility", "price_std", price_std, "price", "trades"),
            ])

    return signals
