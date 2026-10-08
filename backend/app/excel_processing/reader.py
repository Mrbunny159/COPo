import io
import pandas as pd
from fastapi import UploadFile

def read_excel_file(upload_file: UploadFile) -> pd.DataFrame:
    """
    Reads an uploaded Excel file (.xlsx or .xls) and returns a pandas DataFrame.
    Raises ValueError if file reading fails or extension is unsupported.
    """
    filename = upload_file.filename.lower()
    if not (filename.endswith(".xlsx") or filename.endswith(".xls")):
        raise ValueError(f"Invalid file format for '{upload_file.filename}'. Only .xlsx and .xls are supported.")

    try:
        contents = upload_file.file.read()
        df = pd.read_excel(io.BytesIO(contents))
        # Strip string column headers whitespace
        df.columns = [str(col).strip() for col in df.columns]
        return df
    except Exception as e:
        raise ValueError(f"Failed to read Excel file '{upload_file.filename}': {str(e)}")
