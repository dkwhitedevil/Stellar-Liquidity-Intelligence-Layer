from fastapi import FastAPI

app = FastAPI(
    title="SLIL Backend",
    description="Stellar Liquidity Intelligence Layer – Backend",
    version="0.1.0"
)

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "layer": "backend",
        "phase": "Phase 1 - Data Ingestion"
    }
