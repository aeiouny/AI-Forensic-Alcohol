import argparse
import csv

R_FACTOR = {"male": 0.68, "female": 0.55}
DEFAULT_BETA = 0.015

def retrograde_bac(measured_bac, hours_elapsed, beta=DEFAULT_BETA):
    return measured_bac + beta * hours_elapsed

def forward_bac(grams_alcohol, weight_kg, sex, hours_since_start, beta=DEFAULT_BETA):
    r = R_FACTOR[sex.lower()]
    bac = grams_alcohol / (r * weight_kg * 1000) * 100 - beta * hours_since_start
    return max(bac, 0.0)

def run(path, measured_col, hours_col, actual_col, beta):
    errors = []
    print("row, measured, hours, estimate, actual, abs_error")
    with open(path, newline="") as f:
        for i, row in enumerate(csv.DictReader(f), 1):
            measured = float(row[measured_col])
            hours = float(row[hours_col])
            actual = float(row[actual_col])
            est = retrograde_bac(measured, hours, beta)
            err = abs(est - actual)
            errors.append(err)
            print(f"{i}, {measured:.3f}, {hours:.2f}, {est:.3f}, {actual:.3f}, {err:.3f}")
    if errors:
        print(f"\nrows: {len(errors)}   mean absolute error: {sum(errors) / len(errors):.4f} g/dL")
    return errors

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv_path")
    ap.add_argument("--measured", required=True, help="column: BAC measured at test time (g/dL)")
    ap.add_argument("--hours", required=True, help="column: hours between the event and the test")
    ap.add_argument("--actual", required=True, help="column: recorded BAC at the event time (g/dL)")
    ap.add_argument("--beta", type=float, default=DEFAULT_BETA)
    a = ap.parse_args()
    run(a.csv_path, a.measured, a.hours, a.actual, a.beta)