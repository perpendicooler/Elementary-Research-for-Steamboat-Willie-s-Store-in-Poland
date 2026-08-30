# Results

Copy the CSV outputs downloaded from the executed Kaggle notebook into this folder.

Expected files:

- `selected_store_locations.csv`
- `coverage_validation.csv`
- `tsp_exact_method_comparison.csv`
- `christofides_vs_exact.csv`
- `assignment_task_summary.csv`
- optionally `full_lazy_tsp_tour.csv`
- optionally `full_christofides_tour.csv`

Then run:

```bash
python scripts/build_result_charts.py
```

The generated PNG files will be written to `assets/results/`.

Do not hard-code numerical claims in the main README until the corresponding solver run has completed and, where relevant, optimality has been proven.
