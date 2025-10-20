
from typing import List, Dict, Tuple
import pandas as pd
import re

def barcode_to_ecomm_sku(barcode: str) -> str:
    digits = ''.join(ch for ch in str(barcode) if ch.isdigit())
    return f"CKC_00{int(digits):08d}"

def validate_price_input(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    required = ['Bar Code','Diamond Cost','Stone Cost','Making','Wastage',
                'Accessories Cost','Metal Cost','GST','Selling Price w/o Promotion','Selling Price with Promotion']
    missing_cols = [c for c in required if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    errors = []
    for idx, row in df.iterrows():
        bc = str(row['Bar Code'])
        if not re.fullmatch(r"\d{8}", ''.join(ch for ch in bc if ch.isdigit())[-8:]):
            errors.append({'row': idx, 'field': 'Bar Code', 'issue': 'Bar Code should resolve to 8 digits'})
    err_df = pd.DataFrame(errors) if errors else pd.DataFrame(columns=['row','field','issue'])
    return df, err_df

def validate_stone_input(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    required = ['Main Batch Number','Stone Batch Number','Article Type','Article Code','Article Description',
                'Stone  No. of Pieces','Stone Origin','Stone Appearance','Stone Shape','Stone Weight',
                'Stone Units','Stone Cut','Stone Clarity','Stone Color','Stone Amount']
    missing_cols = [c for c in required if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    errors = []
    # numeric checks
    for idx, row in df.iterrows():
        for f in ['Stone  No. of Pieces','Stone Weight','Stone Amount']:
            val = row[f]
            try:
                float(str(val).replace(',',''))
            except Exception:
                errors.append({'row': idx, 'field': f, 'issue': 'Should be numeric'})
    err_df = pd.DataFrame(errors) if errors else pd.DataFrame(columns=['row','field','issue'])
    return df, err_df
