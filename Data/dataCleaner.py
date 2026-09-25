from pathlib import Path
import pandas as pandas

def load_data(filename):
    base_dir = Path(__file__).parent
    file_path = base_dir / filename

    df = pandas.read_csv(file_path)

    return df

def inspect_data(df):
    return df

def select_column(df):
    columns_needed = [
        "ST_CASE",          # Crash identifier
        "PER_NO",           # Person identifier within crash
        "AGE",              
        "SEXNAME",          
        "PER_TYPNAME",      # Driver, passenger, pedestrian, etc.
        "DRINKINGNAME",     # Was alcohol involved
        "ALC_STATUSNAME",   # Was alcohol testing performed
        "ATST_TYPNAME",     # Type of alcohol test
        "ALC_RES",          # BAC
        "ALC_RESNAME",      # Description of BAC result
        "DRUGSNAME",        # Were drugs involved
        "INJ_SEVNAME",      # Injury severity
        "LAG_HRS",          # Time lag 
        "LAG_MINS",         # Time lag
        "HOUR",             # Crash hour
        "MINUTE"            # Crash minute
    ]

    df = df[columns_needed]
    return df


def clean_numbers(df):
    numeric_columns = [
        "AGE",
        "ALC_RES",  #BAC
        "LAG_HRS",  #Hour portion of the time lag associated w record, how many hours passed before test
        "LAG_MINS", #How many minutes passed before test
        "HOUR", #time it happened
        "MINUTE"    #time it happened
    ]

    for column in numeric_columns:
        df[column] = pandas.to_numeric(df[column], errors="coerce")
    return df


def clean_text(df):
    text_columns = [
        "SEXNAME",  #Male or female
        "PER_TYPNAME",  #what kind of person ie driver, passenger, pedestrian, etc
        "DRINKINGNAME", #Was the person drinking or not
        "ALC_STATUSNAME",   #was the test given or not
        "ATST_TYPNAME", #what type of test was done ie blood, breath, etc
        "ALC_RESNAME",  #Bac
        "DRUGSNAME"    #were drugs involved
    ]

    for column in text_columns:
        df[column] = df[column].str.strip().str.lower()

    return df



def remove_duplicates(df):
    df = df.drop_duplicates()
    return df



def remove_missing_data(df):
    required_columns = [
        "AGE",
        "SEXNAME",
        "ALC_RES",
        "DRINKINGNAME"
    ]

    df = df.dropna(subset=required_columns)

    return df



def remove_invalid_data(df):
    df = df[df["AGE"] >= 0]
    df = df[df["ALC_RES"] >= 0]

    invalid_bac_values = [
        995,
        996,
        997,
        998,
        999
    ]

    df = df[~df["ALC_RES"].isin(invalid_bac_values)]

    invalid_bac_names = [
        "test not given",
        "not reported",
        "reported as unknown if tested",
        "ac test performed, results unknown",
        "positive reading with no actual value"
    ]

    df = df[~df["ALC_RESNAME"].isin(invalid_bac_names)]


    return df



def save_data(df, input_filename):
    base_dir = Path(__file__).parent
    output_folder = base_dir / "CleanedData"

    input_path = Path(input_filename)
    output_filename = "cleaned_" + input_path.name

    output_path = output_folder / output_filename

    df.to_csv(output_path, index=False)


def main():
    filename = "RawData/FARS2023NATIONALCSVPERSON.csv"

    df = load_data(filename)

    inspect_data(df)

    df = select_column(df)
    df = clean_numbers(df)
    df = clean_text(df)
    df = remove_missing_data(df)
    df = remove_invalid_data(df)
    df = remove_duplicates(df)

    save_data(df, filename)

    print("Cleaned data file created")

if __name__ == "__main__":
    main()

