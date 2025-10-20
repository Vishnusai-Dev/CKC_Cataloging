
from typing import List, Dict, Tuple
import pandas as pd
from .common import validate_stone_input

STONE_HEADERS: List[str] = [
  "SKU_Code_Bar_Code",
  "Stone Number",
  "Stone Type",
  "Stone Name",
  "Stone Description",
  "Stone(No. of Pieces)",
  "Stone Origin",
  "Stone Appearance",
  "Stone Shape",
  "Stone Weight",
  "Stone Units",
  "Stone Cut",
  "Stone Clarity",
  "Stone Color",
  "Stone Price"
]
STONE_TEMPLATE_ROWS: List[Dict[str, str]] = [
  {
    "SKU_Code_Bar_Code": "CR_SKU_Code_Bar_Code",
    "Stone Number": "CR_Stone Number",
    "Stone Type": "CR_Stone Type",
    "Stone Name": "CR_Stone Name",
    "Stone Description": "CR_Stone Description",
    "Stone(No. of Pieces)": "CR_Stone(No. of Pieces)",
    "Stone Origin": "CR_Stone Origin",
    "Stone Appearance": "CR_Stone Appearance",
    "Stone Shape": "CR_Stone Shape",
    "Stone Weight": "CR_Stone Weight",
    "Stone Units": "CR_Stone Units",
    "Stone Cut": "CR_Stone Cut",
    "Stone Clarity": "CR_Stone Clarity",
    "Stone Color": "CR_Stone Color",
    "Stone Price": "CR_Stone Price"
  },
  {
    "SKU_Code_Bar_Code": "Unique SKU/Variant Code",
    "Stone Number": "Stone number associated with respective SKU code",
    "Stone Type": "Diamond or Gemstone?",
    "Stone Name": "Name of the stone",
    "Stone Description": "Description of the stone",
    "Stone(No. of Pieces)": "No of stone pieces in a jewelery",
    "Stone Origin": "Stone's origin (from country)",
    "Stone Appearance": "Natural stone or enhanced",
    "Stone Shape": "Shape of the stone",
    "Stone Weight": "Weight of the stone",
    "Stone Units": "Unit of the Stone",
    "Stone Cut": "Cut type of the stone",
    "Stone Clarity": "Clarity of the stone",
    "Stone Color": "Color of the stone",
    "Stone Price": "Price of the stone"
  },
  {
    "SKU_Code_Bar_Code": "String",
    "Stone Number": "String",
    "Stone Type": "String",
    "Stone Name": "String",
    "Stone Description": "String",
    "Stone(No. of Pieces)": "Number",
    "Stone Origin": "String",
    "Stone Appearance": "String",
    "Stone Shape": "String",
    "Stone Weight": "Number",
    "Stone Units": "String",
    "Stone Cut": "String",
    "Stone Clarity": "String",
    "Stone Color": "String",
    "Stone Price": "Number"
  },
  {
    "SKU_Code_Bar_Code": "50",
    "Stone Number": "50",
    "Stone Type": "20",
    "Stone Name": "50",
    "Stone Description": "200",
    "Stone(No. of Pieces)": "4",
    "Stone Origin": "50",
    "Stone Appearance": "50",
    "Stone Shape": "20",
    "Stone Weight": "10",
    "Stone Units": "10",
    "Stone Cut": "10",
    "Stone Clarity": "10",
    "Stone Color": "10",
    "Stone Price": "20"
  }
]

def transform_stone(input_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df, err = validate_stone_input(input_df.copy())
    out = pd.DataFrame(columns=STONE_HEADERS)
    meta = pd.DataFrame(STONE_TEMPLATE_ROWS)
    out = pd.concat([meta, out], ignore_index=True)

    mapped = pd.DataFrame({
        'SKU_Code_Bar_Code': df['Main Batch Number'],
        'Stone Number': df['Stone Batch Number'],
        'Stone Type': df['Article Type'],
        'Stone Name': df['Article Description'],
        'Stone Description': df['Article Description'],
        'Stone(No. of Pieces)': df['Stone  No. of Pieces'],
        'Stone Origin': df['Stone Origin'],
        'Stone Appearance': df['Stone Appearance'],
        'Stone Shape': df['Stone Shape'],
        'Stone Weight': df['Stone Weight'],
        'Stone Units': df['Stone Units'],
        'Stone Cut': df['Stone Cut'],
        'Stone Clarity': df['Stone Clarity'],
        'Stone Color': df['Stone Color'],
        'Stone Price': df['Stone Amount']
    })
    for c in ['Stone(No. of Pieces)', 'Stone Weight', 'Stone Price']:
        mapped[c] = pd.to_numeric(mapped[c], errors='coerce')
    out = pd.concat([out, mapped], ignore_index=True)
    return out, err
