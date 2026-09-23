from pathlib import Path
import pandas as pandas

def load_data(filename):
    dataFrame = pandas.read_csv(filename)
    return dataFrame

def inspect_dat(df):
    return df

def select_column(df):
    return df


def clean_numbers(df):
    return df

def clean_text(df):
    return df

def remove_duplicates(df):
    return df

def remove_missing_data(df):
    return df

def remove_invalid_data(df):
    return df

def save_data(df, filename):
    input_path = Path(filename)
    output_folder = Path(__file__).parent/"CleanedData"
    output_filename = "Cleaned_" + input_path.name
    output_path = output_folder / output_filename
    df.to_csv(output_path, index = False)
    return df

def main():
    print("Cleaned data file created")

if __name__ == "__main__":
    main()

