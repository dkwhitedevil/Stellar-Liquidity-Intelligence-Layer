from signal_processing.snapshot_loader import load
from signal_processing.trade_microstructure import extract_trade_microstructure
from signal_processing.orderbook_microstructure import extract_orderbook_microstructure
from signal_processing.payment_flow import extract_payment_flow
from signal_processing.ledger_dynamics import extract_ledger_dynamics
from signal_processing.signal_registry import validate


def get_all_signals():
    signals = []
    signals += extract_trade_microstructure(load("trades"))
    signals += extract_orderbook_microstructure(load("orderbooks"))
    signals += extract_payment_flow(load("payments"))
    signals += extract_ledger_dynamics(load("ledgers"))

    validate(signals)
    return signals


if __name__ == "__main__":
    signals = get_all_signals()
    print(f"Phase 2 complete. Extracted {len(signals)} signals.")
    # Print small sample for manual inspection
    for s in signals[:5]:
        print(s)
