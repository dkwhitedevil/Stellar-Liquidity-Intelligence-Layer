from collections import defaultdict
from forecasting.risk_model import forecast_metric
from forecasting.forecast_registry import validate_forecasts
from signal_processing.extract_all_signals import get_all_signals


def get_all_forecasts():
    signals = get_all_signals()

    grouped = defaultdict(lambda: defaultdict(list))

    for s in signals:
        grouped[s.entity][s.metric].append((s.timestamp, float(s.value)))

    forecasts = []

    for entity, metrics in grouped.items():
        for metric, tv in metrics.items():
            tv = sorted(tv, key=lambda x: x[0])
            timestamps = [t for t, _ in tv]
            values = [v for _, v in tv]

            if len(values) >= 3:
                f = forecast_metric(entity, metric, timestamps, values)
                if f:
                    forecasts.append(f)

    validate_forecasts(forecasts)
    return forecasts


if __name__ == "__main__":
    forecasts = get_all_forecasts()
    print(f"Phase 5 complete. Generated {len(forecasts)} forecasts.")
    for f in forecasts:
        print(f)
