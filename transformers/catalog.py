
from typing import List, Dict, Tuple
import pandas as pd

def transform_catalog(input_df: pd.DataFrame, output_template: pd.DataFrame) -> pd.DataFrame:
    """Generic catalog transformer.
    Until the official template is provided, this function aligns columns by name.
    Steps:
      - Uses output_template columns as the target order.
      - For any missing columns, creates blanks.
      - For extra input columns, they're ignored (unless they match target names).
    """
    target_cols = list(output_template.columns)
    out = pd.DataFrame(columns=target_cols)
    # Try to map same-named columns, else fill empty
    for col in target_cols:
        if col in input_df.columns:
            out[col] = input_df[col]
        else:
            out[col] = ""
    # Preserve first 4 template rows if present in output_template
    meta = output_template.iloc[:4] if len(output_template) >= 4 else pd.DataFrame(columns=target_cols)
    final = pd.concat([meta, out], ignore_index=True)
    return final
