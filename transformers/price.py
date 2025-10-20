
from typing import List, Dict, Tuple
import pandas as pd
from .common import barcode_to_ecomm_sku, validate_price_input

PRICE_HEADERS: List[str] = [
  "CR_EcommSKUCode",
  "CR_DiamondCost",
  "CR_GemstoneCost",
  "CR_MakingCharges",
  "CR_WastageCharges",
  "CR_AccessoriesCost",
  "CR_MetalCost",
  "CR_GSTCharges",
  "CR_Price_without_Promotion",
  "CR_Price_with_Promotion",
  "Price_Group_Code"
]
PRICE_TEMPLATE_ROWS: List[Dict[str, str]] = [
  {
    "CR_EcommSKUCode": "Unique SKU code by Ecomm system",
    "CR_DiamondCost": "Cost price of Particular Diamond",
    "CR_GemstoneCost": "Cost price of paticular gemstone",
    "CR_MakingCharges": "Making charges pf particular product",
    "CR_WastageCharges": "Loss of material while finishing the product",
    "CR_AccessoriesCost": " ",
    "CR_MetalCost": "Weight of Product * Metal Cost",
    "CR_GSTCharges": "Taxes = gemstone cost+ making charges + wastage charges + accessories cost + metal cost",
    "CR_Price_without_Promotion": "Selling price of the product",
    "CR_Price_with_Promotion": "Selling price after discount value",
    "Price_Group_Code": "Price Group Code(SELR/STOR/LOCZ/CSTG/ALL)"
  },
  {
    "CR_EcommSKUCode": "Mandatory",
    "CR_DiamondCost": "Mandatory",
    "CR_GemstoneCost": "Mandatory",
    "CR_MakingCharges": "Mandatory",
    "CR_WastageCharges": "Mandatory",
    "CR_AccessoriesCost": "Mandatory",
    "CR_MetalCost": "Mandatory",
    "CR_GSTCharges": "Mandatory",
    "CR_Price_without_Promotion": "Mandatory",
    "CR_Price_with_Promotion": "Mandatory",
    "Price_Group_Code": "Non-Mandatory"
  },
  {
    "CR_EcommSKUCode": "String",
    "CR_DiamondCost": "Number",
    "CR_GemstoneCost": "Number",
    "CR_MakingCharges": "Number",
    "CR_WastageCharges": "Number",
    "CR_AccessoriesCost": "Number",
    "CR_MetalCost": "Number",
    "CR_GSTCharges": "Number",
    "CR_Price_without_Promotion": "Number",
    "CR_Price_with_Promotion": "Number",
    "Price_Group_Code": "String"
  },
  {
    "CR_EcommSKUCode": "50",
    "CR_DiamondCost": "20",
    "CR_GemstoneCost": "20",
    "CR_MakingCharges": "20",
    "CR_WastageCharges": "20",
    "CR_AccessoriesCost": "20",
    "CR_MetalCost": "20",
    "CR_GSTCharges": "20",
    "CR_Price_without_Promotion": "20",
    "CR_Price_with_Promotion": "20",
    "Price_Group_Code": "20"
  }
]

def transform_price(input_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df, err = validate_price_input(input_df.copy())
    out = pd.DataFrame(columns=PRICE_HEADERS)
    meta = pd.DataFrame(PRICE_TEMPLATE_ROWS)
    out = pd.concat([meta, out], ignore_index=True)

    mapped_rows = pd.DataFrame({
        'CR_EcommSKUCode': df['Bar Code'].apply(barcode_to_ecomm_sku),
        'CR_DiamondCost': df['Diamond Cost'],
        'CR_GemstoneCost': df['Stone Cost'],
        'CR_MakingCharges': df['Making'],
        'CR_WastageCharges': df['Wastage'],
        'CR_AccessoriesCost': df.get('Accessories Cost'),
        'CR_MetalCost': df['Metal Cost'],
        'CR_GSTCharges': df['GST'],
        'CR_Price_without_Promotion': df['Selling Price w/o Promotion'],
        'CR_Price_with_Promotion': df['Selling Price with Promotion'],
        'Price_Group_Code': ""
    })
    for c in ['CR_DiamondCost','CR_GemstoneCost','CR_MakingCharges','CR_WastageCharges',
              'CR_AccessoriesCost','CR_MetalCost','CR_GSTCharges',
              'CR_Price_without_Promotion','CR_Price_with_Promotion']:
        mapped_rows[c] = pd.to_numeric(mapped_rows[c], errors='coerce')
    mapped_rows['Price_Group_Code'] = mapped_rows['Price_Group_Code'].fillna("")
    out = pd.concat([out, mapped_rows], ignore_index=True)
    return out, err
