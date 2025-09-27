import pandas as pd
from sqlalchemy import create_engine

# --- Database connection ---
# Example: MySQL
engine = create_engine("mysql+pymysql://root:pass123@localhost/nura")

# Read Excel file with two sheets
excel_file = r"C:\Users\ASUS\Downloads\Data Engineer Task Assignment.xlsx"

# Load all sheets as dictionary {sheet_name: dataframe}
sheets = pd.read_excel(excel_file, sheet_name=None)

# Loop through sheets and save each as a table
for sheet_name, df in sheets.items():
    table_name = sheet_name.lower().replace(" ", "_")  # clean table name
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"✅ Imported sheet '{sheet_name}' into table '{table_name}'")