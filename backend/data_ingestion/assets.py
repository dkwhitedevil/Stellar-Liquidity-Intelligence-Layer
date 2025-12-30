from stellar_sdk import Asset

def native_asset():
    return Asset.native()

def credit_asset(code: str, issuer: str):
    """
    Create a credit asset with validation.
    """
    return Asset(code, issuer)

def asset_to_dict(asset: Asset) -> dict:
    if asset.is_native():
        return {"type": "native", "code": "XLM"}
    return {
        "type": "credit_alphanum",
        "code": asset.code,
        "issuer": asset.issuer
    }
