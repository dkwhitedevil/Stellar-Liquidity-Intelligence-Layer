# Stellar-Liquidity-Intelligence-Layer

[![CI](https://github.com/<owner>/<repo>/actions/workflows/ci.yml/badge.svg)](https://github.com/<owner>/<repo>/actions/workflows/ci.yml)

An infrastructure-level intelligence service that models Stellar as a dynamic economic graph to improve payment reliability.

## CI
This repository is configured with a GitHub Actions workflow in `.github/workflows/ci.yml` that runs backend tests and builds the frontend on push/PR. Replace the badge owner/repo placeholder above with your repository path to enable a live badge.

## Analysis
- Sensitivity analysis script: `backend/analysis/scoring_sensitivity.py` — run this to sweep scoring hyperparameters and generate a CSV report in `backend/artifacts/`.
