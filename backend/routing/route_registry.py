def validate_advisories(advisories):
    for a in advisories:
        assert 0.0 <= a.score <= 1.0, f"Advisory score out of bounds: {a}"
        assert isinstance(a.path, list), f"Advisory path must be a list: {a}"
