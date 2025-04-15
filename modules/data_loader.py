import pandas as pd
import os

DEFAULT_FILE = "LiPF6_data.xlsx"

def get_excel_path(file_name=DEFAULT_FILE):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "..", "data", file_name)

def load_data(sheet_name, file_name=DEFAULT_FILE):
    excel_path = get_excel_path(file_name)
    return pd.read_excel(excel_path, sheet_name=sheet_name, engine="openpyxl")

def save_data(df, sheet_name, file_name=DEFAULT_FILE):
    excel_path = get_excel_path(file_name)
    with pd.ExcelWriter(excel_path, mode='a', engine='openpyxl', if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
