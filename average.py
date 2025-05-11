import pandas as pd


def get_original_column_name(adjusted_name: str):
    parts = adjusted_name.split(".")

    if len(parts) > 2:
        raise ValueError("Column names must not contain a dot (.)!")

    return parts[0].strip()


def main():
    df = pd.read_csv("DATA.csv")

    data_columns = df.columns[1:]  # removes the "time" column

    batches: dict[str, list[pd.Series]] = {}

    for column in data_columns:

        name = get_original_column_name(column)

        if name in batches:
            batches[name].append(df[column])

        else:
            batches[name] = [df[column]]

    out = pd.DataFrame()

    for name, batch in batches.items():
        batch_df = pd.DataFrame(batch)
        out[name] = batch_df.mean(axis=0)

    out.to_csv("AVERAGES.csv")


if __name__ == "__main__":
    main()
