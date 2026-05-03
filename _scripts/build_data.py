"""
Regenerate textbook datasets from their original sources.

Run from the Sample/ directory:
    python _scripts/build_data.py

Requires:
    pip install wooldridge

Outputs CSVs into Sample/data/ ready to be committed alongside the book.
"""

from pathlib import Path

import wooldridge as woo


# Wooldridge datasets used in the book.
# Add new entries here when you start using another dataset.
WOOLDRIDGE_DATASETS = [
    "wage1",
]


def main() -> None:
    here = Path(__file__).resolve().parent
    data_dir = here.parent / "data"
    data_dir.mkdir(exist_ok=True)

    for name in WOOLDRIDGE_DATASETS:
        df = woo.dataWoo(name)
        out = data_dir / f"{name}.csv"
        df.to_csv(out, index=False)
        print(f"Wrote {out}  ({df.shape[0]} rows, {df.shape[1]} cols)")


if __name__ == "__main__":
    main()
