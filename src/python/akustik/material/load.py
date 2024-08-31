import numpy as np
import pandas as pd


def load_materials(file) -> pd.DataFrame:
    """Loads the materials from the Excel spreadsheet as a pandas dataframe.
    Only the octaves (125, 250, 500, 1000, 2000, 4000) are loaded. Rows that
    do not contain coefficients for these frequencies are dropped.

    The Room Acoustics Absorption Coefficient Database:
    https://www.ptb.de/cms/ptb/fachabteilungen/abt1/fb-16/ag-163/absorption-coefficient-database.html
    """
    bands = [63, 125, 250, 500, 1000, 2000, 4000]

    character_df = pd.read_excel(
        file,
        sheet_name=["selection_table"],
        skiprows=3,
        nrows=5,
        usecols=[33, 39],
        index_col=1,
    )["selection_table"]

    def to_character(id): return character_df.iloc[int(id) - 1][
        "character of absorption (column AQ + AR)"
    ]

    criteria_df = pd.read_excel(
        file,
        sheet_name=["selection_table"],
        skiprows=2,
        nrows=12,
        usecols=[41, 48],
        index_col=1,
    )["selection_table"]

    def to_criteria(id): return criteria_df.iloc[int(id) - 1][
        "material criteria: (column AS + AT)"
    ]

    df = pd.read_excel(
        file,
        sheet_name=["selection_table"],
        skiprows=19,
        nrows=2574,
        index_col=0,
        dtype={"No.": np.int32},
    )["selection_table"]

    for freq in bands:
        df = df[pd.to_numeric(df[freq], errors="coerce").notnull()]
        df[freq] = df[freq].astype(np.float64)

    material_col = "material criteria"
    df = df.dropna(subset=[material_col])
    df["criteria"] = df[material_col].apply(
        to_criteria).astype(dtype="category")

    character_col = "character of absorption"
    df = df[df[character_col] != 12.0]
    df = df.dropna(subset=[character_col])
    df["character"] = df[character_col].apply(
        to_character).astype(dtype="category")

    # df["octave_mean"] = df[bands].mean(axis=1)
    df["max"] = df[bands].max(axis=1)
    df = df[df["max"] <= 1.0]

    return df[["description", "criteria", "character"] + bands]


def main(filename):
    materials: pd.DataFrame = load_materials(filename)
    materials["description"] = materials["description"].str.replace("\n", " ")
    # materials = materials[materials["description"].str.contains("floor")]
    materials.to_csv("materials.csv")
    print(materials.info(verbose=True, memory_usage=True))
