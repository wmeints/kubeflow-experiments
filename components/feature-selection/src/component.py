from pathlib import Path
from os import path, mkdir
from pathlib import Path

import argparse
import pandas as pd


def select_features(input_file, output_file):
    columns = ['ID',
        'TYPE_WACHTTIJD',
        'WACHTTIJD',
        'SPECIALISME',
        'ROAZ_REGIO',
        'TYPE_ZORGINSTELLING'
    ]

    df = pd.read_csv(input_file, encoding='iso-8859-1', sep=';')
    df[columns].to_csv(output_file, index=False)


def main():
    parser = argparse.ArgumentParser(description="Select features for the training and test set")

    parser.add_argument("--input", type=str, help="Input file")
    parser.add_argument("--output", type=str, help="Output file")

    args = parser.parse_args()

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    select_features(args.input, args.output)


if __name__ == "__main__":
    main()
