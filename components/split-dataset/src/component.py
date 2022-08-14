from pathlib import Path
from os import path, mkdir
from pathlib import Path

import argparse
import pandas as pd
from sklearn.model_selection import train_test_split


def split_dataset(input_file, train_output_file, validation_output_file, test_size):
    df = pd.read_csv(input_file)
    df_train, df_validate = train_test_split(df, test_size=test_size)

    df_train.to_csv(train_output_file, index=False)
    df_validate.to_csv(validation_output_file, index=False)


def main():
    parser = argparse.ArgumentParser(description="Select features for the training and test set")

    parser.add_argument("--input", type=str, help="Input file")
    parser.add_argument("--train-output", type=str, help="Location where to store the training set")
    parser.add_argument("--validation-output", type=str, help="Location where to store the validation set")

    args = parser.parse_args()

    Path(args.train_output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.validation_output).parent.mkdir(parents=True, exist_ok=True)

    split_dataset(args.input, args.train_output, args.validation_output, args.test_size)


if __name__ == "__main__":
    main()
