from pathlib import Path
from os import path, mkdir
from pathlib import Path

import argparse
import pandas as pd


def fix_missing_values(input_file, output_file):
    df = pd.read_csv(input_file)
    
    df["TYPE_ZORGINSTELLING"].fillna("Kliniek", inplace=True)
    df["WACHTTIJD"] = df.groupby("SPECIALISME")["WACHTTIJD"].apply(lambda x: x.fillna(x.mean()))

    df.to_csv(output_file, index=False)


def main():
    parser = argparse.ArgumentParser(description="Select features for the training and test set")

    parser.add_argument("--input", type=str, help="Input file")
    parser.add_argument("--output", type=str, help="Output file")

    args = parser.parse_args()

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    fix_missing_values(args.input, args.output)


if __name__ == "__main__":
    main()
