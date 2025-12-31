# SLIL Frontend

This frontend implements the **Stellar Liquidity Intelligence Layer (SLIL)** frontend specification — submission-grade, research-focused, and conservative.

## Top-level structure

- Header / Navbar
- Project Overview
- Corridor Selection (User Input)
- System State Dashboard
  - Reliability & Stability
  - Forecasts & Risk
  - Routing Advisories (handles empty state)
- Graph & Data Transparency
- Simulation & Evaluation
- Limitations & Conservatism
- Future Work
- Footer

## Important guardrails
- No wallet connect UI
- No amount inputs
- No execute/send/confirm buttons
- No fee optimization UI
- No best-path selector or auto-routing

## Submission checklist
- Corridor selector exists
- Empty states are explained
- 0 advisories handled gracefully
- Scores & forecasts explained
- Conservatism clearly stated
- No execution UI
- Research framing present
- Future work section included

## Development
Run:

```
cd frontend
npm install
npm run dev
```

Run the backend in a separate terminal:

```
cd backend
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

The frontend will query `http://localhost:8000/api/corridor` by default. You can override the backend base URL by setting `VITE_API_BASE` in the frontend environment (e.g., `VITE_API_BASE=http://localhost:8000 npm run dev`).

This app is intentionally read-only and provides research-grade transparency, clear empty states, and conservative advisory logic per the specification.
## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
