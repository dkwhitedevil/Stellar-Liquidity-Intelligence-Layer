def apply_policies(paths, max_hops=3):
    return [p for p in paths if len(p) - 1 <= max_hops]
