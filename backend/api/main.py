from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from routing.advise_routes import run_advisory

app = FastAPI(
    title="SLIL Backend",
    description="Stellar Liquidity Intelligence Layer – Backend",
    version="0.1.0"
)

# Allow local frontend dev (vite) to access API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "layer": "backend",
        "phase": "Phase 1 - Data Ingestion"
    }

@app.get("/api/corridor")
def corridor_info(source: Optional[str] = Query(None), dest: Optional[str] = Query(None)):
    """Return mock corridor metrics, forecasts, graph summary and advisories.

    - If source or dest missing -> returns minimal metadata and indicates insufficient data
    - Otherwise returns plausible mock metrics
    """
    if not source or not dest or source == dest:
        return {
            "source": source,
            "dest": dest,
            "message": "Insufficient corridor specification or invalid corridor (source == dest).",
            "reliability": None,
            "stability": None,
            "forecasts": [],
            "advisories": [],
            "graph": {"nodes": 0, "edges": 0, "snapshot": None}
        }

    # Simple deterministic mock values based on asset names
    base = (sum(ord(c) for c in source) + sum(ord(c) for c in dest)) % 100
    reliability = round(0.4 + (base % 30) / 100, 2)
    stability = round(0.5 + (base % 20) / 100, 2)

    forecasts = []
    if base % 7 != 0:  # pretend sometimes there's insufficient history
        forecasts = [
            {"metric": "Liquidity depth", "expected": f"{1000 + base*5} XLM", "uncertainty": "±15%"},
            {"metric": "Estimated slippage", "expected": f"{(base%10)/100:.2%}", "uncertainty": "±0.5%"}
        ]

    advisories = []
    if base % 11 == 0:
        advisories = [
            {"score": 0.72, "risk": "Medium", "explain": "Candidate path shows moderate reliability but elevated slippage risk."}
        ]

    graph = {"nodes": 120 + (base % 50), "edges": 400 + (base % 200), "snapshot": "2025-12-30T19:14:55Z"}

    return {
        "source": source,
        "dest": dest,
        "reliability": reliability,
        "stability": stability,
        "forecasts": forecasts,
        "advisories": advisories,
        "graph": graph
    }

@app.get('/scores')
def scores():
    # Return mock scores for entities
    return [
        {"entity":"Connector A","score_type":"reliability","value":0.72,"explanation":"Sufficient history, stable connectivity."},
        {"entity":"Connector B","score_type":"stability","value":0.51,"explanation":"Limited data; neutral score."}
    ]


@app.get('/scores/compute')
def scores_compute():
    """Compute live scores by running the scoring engine and persist a snapshot."""
    from scoring.runner import compute_and_save_scores
    data = compute_and_save_scores()
    return {"computed": True, "count": len(data), "scores": data}


@app.get('/scores/latest')
def scores_latest():
    """Return the latest computed scores snapshot, if any."""
    from scoring.runner import load_latest_scores
    data = load_latest_scores()
    return {"count": len(data), "scores": data}


@app.get('/stability/compute')
def stability_compute(window_size: int = 6, window_minutes: int = 5):
    """Compute temporal stability snapshots and persist."""
    from stability.runner import compute_and_save_stability
    data = compute_and_save_stability(window_size=window_size, window_minutes=window_minutes)
    return {"computed": True, "count": len(data), "stability": data}


@app.get('/stability/latest')
def stability_latest():
    from stability.runner import load_latest_stability
    data = load_latest_stability()
    return {"count": len(data), "stability": data}

@app.get('/forecasts')
def forecasts():
    # Return mock forecasts
    return [
        {"entity":"Corridor X→Y","metric":"Liquidity depth","expected":1200,"uncertainty":15},
        {"entity":"Corridor X→Y","metric":"Slippage","expected":0.02,"uncertainty":0.5}
    ]

@app.get('/advisories')
def advisories(src: Optional[str] = Query(None, alias='from'), dst: Optional[str] = Query(None, alias='to')):
    # Simple advisory generation (note: query params are 'from' and 'to' but function names avoid reserved words)
    if not src or not dst or src == dst:
        return []
    base = (sum(ord(c) for c in src) + sum(ord(c) for c in dst)) % 100
    if base % 11 == 0:
        return [
            {"source": src, "destination": dst, "score": 0.72, "risk": "Medium", "explanation": "Candidate path shows moderate reliability but elevated slippage risk."}
        ]
    return []

@app.get('/graph/summary')
def graph_summary():
    return {"nodes": 142, "edges": 523, "timestamp": "2025-12-30T19:14:55Z"}


@app.get('/graph/paths')
def graph_paths(src: Optional[str] = Query(None, alias='from'), dst: Optional[str] = Query(None, alias='to'), max_hops: int = 3):
    """Return routing advisories (paths) between src and dst by calling the advisory runner."""
    if not src or not dst or src == dst:
        return []

    advisories = run_advisory(src, dst, max_hops=max_hops)

    # Convert dataclass objects into JSON-serializable dicts
    out = []
    for a in advisories:
        out.append({
            "timestamp": a.timestamp.isoformat(),
            "source": a.source,
            "destination": a.destination,
            "path": a.path,
            "score": a.score,
            "risk": a.risk,
            "explanation": a.explanation,
        })

    return out


@app.get('/routes/recommend')
def routes_recommend(src: Optional[str] = Query(None, alias='from'), dst: Optional[str] = Query(None, alias='to'), max_hops: int = 3, banned: Optional[str] = None, min_liq: Optional[float] = None):
    """Return recommended routes with additional metadata and optional policy filters.

    Query params:
    - from, to: source and destination entities
    - max_hops: maximum hops to enumerate
    - banned: comma-separated list of entities to exclude
    - min_liq: minimum per-edge liquidity threshold (if available from graph)
    """
    if not src or not dst or src == dst:
        return []

    banned_list = []
    if banned:
        banned_list = [b.strip() for b in banned.split(",") if b.strip()]

    from routing.recommendation import run_recommendation

    recs = run_recommendation(src, dst, max_hops=max_hops, banned=banned_list, min_liquidity=min_liq)

    out = []
    for r in recs:
        a = r["advisory"]
        out.append({
            "timestamp": a.timestamp.isoformat(),
            "source": a.source,
            "destination": a.destination,
            "path": a.path,
            "score": a.score,
            "risk": a.risk,
            "explanation": a.explanation,
            "edge_penalty": r.get("edge_penalty"),
            "min_liquidity": r.get("min_liquidity"),
            "metrics": r.get("metrics"),
        })

    return out
