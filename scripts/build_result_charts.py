from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RESULTS = ROOT / "results"
ASSETS = ROOT / "assets" / "results"
ASSETS.mkdir(parents=True, exist_ok=True)

towns = pd.read_csv(DATA / "poland_towns_from_dataset.csv")

def require(name):
    path = RESULTS / name
    if not path.exists():
        print(f"[skip] missing {name}")
        return None
    return pd.read_csv(path)

stores = require("selected_store_locations.csv")
coverage = require("coverage_validation.csv")
exact = require("tsp_exact_method_comparison.csv")
christ = require("christofides_vs_exact.csv")

if stores is not None:
    fig = plt.figure(figsize=(9, 8))
    plt.scatter(towns["longitude"], towns["latitude"], s=7, alpha=0.22, label="Populated places")
    plt.scatter(stores["longitude"], stores["latitude"], s=45, marker="x", label="Selected stores")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title(f"50 km Store-Covering Solution — {len(stores)} Stores")
    plt.legend()
    plt.tight_layout()
    plt.savefig(ASSETS / "coverage_map.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

if coverage is not None and "nearest_store_distance_km" in coverage.columns:
    fig = plt.figure(figsize=(9, 4))
    plt.hist(coverage["nearest_store_distance_km"].dropna(), bins=30)
    plt.axvline(50.0, linestyle="--", label="50 km requirement")
    plt.xlabel("Distance to nearest selected store (km)")
    plt.ylabel("Number of populated places")
    plt.title("Coverage Distance Distribution")
    plt.legend()
    plt.tight_layout()
    plt.savefig(ASSETS / "coverage_distance_histogram.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

if exact is not None:
    needed = {"n", "explicit_runtime_sec", "lazy_runtime_sec"}
    if needed.issubset(exact.columns):
        fig = plt.figure(figsize=(8, 5))
        plt.plot(exact["n"], exact["explicit_runtime_sec"], marker="o", label="Explicit SEC ILP")
        plt.plot(exact["n"], exact["lazy_runtime_sec"], marker="o", label="Lazy row generation")
        plt.xlabel("Number of TSP nodes")
        plt.ylabel("Runtime (seconds)")
        plt.title("Exact TSP Runtime Comparison")
        plt.legend()
        plt.tight_layout()
        plt.savefig(ASSETS / "exact_runtime_comparison.png", dpi=180, bbox_inches="tight")
        plt.close(fig)

    needed = {"n", "explicit_SEC_count", "lazy_cuts_generated"}
    if needed.issubset(exact.columns):
        fig = plt.figure(figsize=(8, 5))
        plt.semilogy(exact["n"], exact["explicit_SEC_count"], marker="o", label="Explicit SECs")
        plt.semilogy(exact["n"], np.maximum(exact["lazy_cuts_generated"], 1), marker="o", label="Lazy rows added")
        plt.xlabel("Number of TSP nodes")
        plt.ylabel("Subtour constraints (log scale)")
        plt.title("Explicit Constraints vs Lazy Row Generation")
        plt.legend()
        plt.tight_layout()
        plt.savefig(ASSETS / "constraint_growth_comparison.png", dpi=180, bbox_inches="tight")
        plt.close(fig)

if christ is not None:
    needed = {"n", "exact_optimum_km", "christofides_km"}
    if needed.issubset(christ.columns):
        fig = plt.figure(figsize=(8, 5))
        plt.plot(christ["n"], christ["exact_optimum_km"], marker="o", label="Exact optimum")
        plt.plot(christ["n"], christ["christofides_km"], marker="o", label="Christofides")
        plt.xlabel("Number of TSP nodes")
        plt.ylabel("Tour length (km)")
        plt.title("Christofides vs Exact Metric TSP")
        plt.legend()
        plt.tight_layout()
        plt.savefig(ASSETS / "christofides_vs_exact_length.png", dpi=180, bbox_inches="tight")
        plt.close(fig)

    if {"n", "approximation_ratio"}.issubset(christ.columns):
        fig = plt.figure(figsize=(8, 4))
        plt.plot(christ["n"], christ["approximation_ratio"], marker="o")
        plt.axhline(1.0, linestyle="--", label="Optimal")
        plt.axhline(1.5, linestyle="--", label="Christofides bound")
        plt.xlabel("Number of TSP nodes")
        plt.ylabel("Christofides / optimum")
        plt.title("Observed Christofides Approximation Ratio")
        plt.legend()
        plt.tight_layout()
        plt.savefig(ASSETS / "christofides_approximation_ratio.png", dpi=180, bbox_inches="tight")
        plt.close(fig)

print("Finished. Result charts are in:", ASSETS)
