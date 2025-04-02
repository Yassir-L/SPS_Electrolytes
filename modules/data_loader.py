import pandas as pd
import os

def get_excel_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "..", "data", "LiPF6_data.xlsx")

def load_data(sheet_name):
    excel_path = get_excel_path()
    return pd.read_excel(excel_path, sheet_name=sheet_name, engine="openpyxl")

def save_data(df, sheet_name):
    excel_path = get_excel_path()
    # Load existing sheets
    with pd.ExcelWriter(excel_path, mode='a', engine='openpyxl', if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

