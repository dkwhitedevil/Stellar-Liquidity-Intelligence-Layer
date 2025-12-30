def risk_penalty(route_metrics):
    # Higher uncertainty -> higher penalty
    uncertainties = [m.get("uncertainty", 0.0) for m in route_metrics]
    if not uncertainties:
        return 0.0
    return float(sum(uncertainties) / len(uncertainties))
