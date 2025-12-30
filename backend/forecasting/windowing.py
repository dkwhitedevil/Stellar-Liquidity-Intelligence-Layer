def sliding_windows(values, size=3):
    if len(values) < size:
        return []
    return [values[i:i+size] for i in range(len(values)-size+1)]
