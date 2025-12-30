import numpy as np
from forecasting.forecast_schema import Forecast
from forecasting.baseline_models import ema_forecast
from forecasting.uncertainty import estimate_uncertainty


def forecast_metric(entity, metric, timestamps, values):
    # values assumed ordered by timestamps
    if not values:
        return None

    expected = ema_forecast(values)
    unc = estimate_uncertainty(values)

    return Forecast(
        timestamp=max(timestamps),
        entity=entity,
        metric=metric,
        horizon="next_window",
        expected=float(expected),
        lower_bound=float(expected - unc),
        upper_bound=float(expected + unc),
        uncertainty=float(unc),
        model="EMA"
    )
