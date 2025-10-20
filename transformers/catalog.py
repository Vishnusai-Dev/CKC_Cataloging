from typing import List, Dict, Tuple
import pandas as pd
from .common import barcode_to_ecomm_sku, validate_catalog_input

# ------------------------------------------
# 1. Catalog Template Headers (embedded)
# ------------------------------------------
CATALOG_HEADERS: List[str] = [
    "Entity Identifier", "SKU Code", "Product Name", "Category Code", "Brand Code",
    "Product Subtitle", "Tax Applicable", "TaxOrHSN Code", "Product Description",
    "Article Description", "Article Code", "Article Type", "Tags Keyword",
    "Meta Title", "Meta Keyword", "Meta Description", "Location Group", "Vendor",
    "Is Active(Y/N)", "Is Publish(Y/N)", "Is customizable? (Y/N)", "Is 'New Arrival'",
    "Is Try at Store", "Is Try at Home", "Is Try On", "Is Price on Request",
    "Is Free Shipping?", "Product Net weight", "Product Net weight Unit", "Length",
    "Item Display Width", "Item Display Height", "Unit of LWH Dimension",
    "Min Quantity allowed in shopping cart", "Max Quantity allowed in shopping cart",
    "Delivery Type", "Store Code", "Is Gift Wrap", "Is inscription",
    "Is Pick Up at store", "Is EMI available", "Product Video",
    "PDP Image 1", "PDP Image 2", "PDP Image 3", "PDP Image 4", "PDP Image 5",
    "PDP Image 6", "PDP Image 7", "PDP Image 8", "PDP Image 9", "PDP Image 10",
    "PDP Image 11", "PDP Image 12", "PDP Image 13", "PDP Image 14", "PDP Image 15",
    "PLP Preview Image 1 ", "PLP Preview Image 2", "PLP Preview Image 3",
    "Collection", "HighJewellery Flag ", "Parent Theme", "Child Theme", "Segment",
    "Gender", "Certitificate Codes", "Jewel Type", "Product Gross Weight",
    "Product Gross Weight Unit", "Item Diameter", "Item Diameter Units",
    "Bracelet Length", "Ring Size", "Bangle Sizes", "Purity", "Polish Type",
    "Screw Type", "Setting Type", "Finish", "Style or Season or Occasion",
    "Metal Type", "Metal Name", "Metal Color", "Is 'Trendy Fashion'",
    "Pendant Loop Type", "Hook Type", "Bangle Shape", "Pattern", "Rows",
    "Attribute 1", "Attribute 2", "Attribute 3", "Attribute 4", "Attribute 5",
    "Attribute 6", "Attribute 7", "Attribute 8", "Attribute 9", "Attribute_10",
    "Product Highlights", "pieces", "Pieces UOM", "Is Returnable", "Is Cancellable"
]

# ------------------------------------------
# 2. Meta (first 4 template rows)
# ------------------------------------------
# In production you can keep this minimal—here it preserves format consistency.
CATALOG_TEMPLATE_ROWS: List[Dict[str, str]] = [
    {h: f"CR_{h.replace(' ', '_')}" for h in CATALOG_HEADERS},  # metadata 1
    {h: h for h in CATALOG_HEADERS},                            # metadata 2
    {h: "TextField" for h in CATALOG_HEADERS},                  # metadata 3
    {h: "" for h in CATALOG_HEADERS},                           # metadata 4
]

# ------------------------------------------
# 3. Logical ERP → Catalog Mapping
# ------------------------------------------
ERP_TO_CATALOG_MAP: Dict[str, str] = {
    "Entity Identifier": "Entity",
    "SKU Code": "Bar Code",
    "Product Name": "Article Description",
    "Product Subtitle": "Article Description",
    "Tax Applicable": "Tax Applicable",
    "TaxOrHSN Code": "HSN Code",
    "Article Description": "Article Description",
    "Article Code": "Article Number",
    "Article Type": "Article Type",
    "Vendor": "Vendor",
    "Product Net weight": "Net Metal Weight",
    "Product Net weight Unit": "Net Metal Weight Units",
    "Product Gross Weight": "Gross Item Weight",
    "Product Gross Weight Unit": "Gross Item Weight Unit",
    "Collection": "Collection",
    "Purity": "Purity",
    "Metal Type": "Metal Type",
    "Metal Name": "Metal Name",
    "Gender": "Gender Description",
    "Parent Theme": "Parent Theme",
    "Child Theme": "Child Theme",
    "Segment": "Segment",
    "Jewel Type": "Jewel Type",
    "Polish Type": "Polish Type Description",
    "Setting Type": "Setting Type Description",
    "Bangle Sizes": "Bangle Size",
    "Bangle Shape": "Bangle Shape",
    "Hook Type": "Hook Type Description",
    "Pieces": "Pieces",
    "Pieces UOM": "UOM"
}

# ------------------------------------------
# 4. Transformer Function
# ------------------------------------------
def transform_catalog(input_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Transforms ERP catalog input to upload-ready catalog format."""
    df, err = validate_catalog_input(input_df.copy())

    # Initialize output
    out = pd.DataFrame(columns=CATALOG_HEADERS)
    meta = pd.DataFrame(CATALOG_TEMPLATE_ROWS)
    out = pd.concat([meta, out], ignore_index=True)

    # Map ERP columns to output headers
    mapped = pd.DataFrame(columns=CATALOG_HEADERS)
    for col in CATALOG_HEADERS:
        if col in ERP_TO_CATALOG_MAP:
            src = ERP_TO_CATALOG_MAP[col]
            mapped[col] = df[src] if src in df.columns else ""
        else:
            mapped[col] = ""

    # Generate SKU Code with prefix logic
    if "SKU Code" in mapped.columns and "Bar Code" in df.columns:
        mapped["SKU Code"] = df["Bar Code"].apply(barcode_to_ecomm_sku)

    # Default flags
    for fld in ["Is Active(Y/N)", "Is Publish(Y/N)", "Is Returnable", "Is Cancellable"]:
        if fld in mapped.columns:
            mapped[fld] = "Y"

    # Combine metadata + mapped data
    final = pd.concat([out, mapped], ignore_index=True)
    return final, err
