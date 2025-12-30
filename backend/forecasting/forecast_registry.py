def validate_forecasts(forecasts):
    for f in forecasts:
        assert f.lower_bound <= f.expected <= f.upper_bound, f"Forecast bounds invalid: {f}"
        assert f.uncertainty >= 0.0, f"Forecast uncertainty negative: {f}"
