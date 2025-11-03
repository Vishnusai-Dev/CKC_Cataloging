from typing import List, Dict, Tuple
import pandas as pd
from .common import barcode_to_ecomm_sku, validate_catalog_input

# ---------------------------------------------------------------------
# 1. Catalog Template Headers
# ---------------------------------------------------------------------
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

# ---------------------------------------------------------------------
# 2. Template Meta Rows (first 4)
# ---------------------------------------------------------------------
CATALOG_TEMPLATE_ROWS: List[Dict[str, str]] = [
    {h: f"CR_{h.replace(' ', '_')}" for h in CATALOG_HEADERS},
    {h: h for h in CATALOG_HEADERS},
    {h: "TextField" for h in CATALOG_HEADERS},
    {h: "" for h in CATALOG_HEADERS},
]

# ---------------------------------------------------------------------
# 3. ERP → Catalog Mapping
# ---------------------------------------------------------------------
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
    "Pieces UOM": "UOM",
    "Length": "Length"
}

# ---------------------------------------------------------------------
# 4. Transformer Function
# ---------------------------------------------------------------------
def transform_catalog(input_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Transforms ERP catalog input to upload-ready catalog format with defaults, images & highlights."""
    df, err = validate_catalog_input(input_df.copy())

    # Base setup
    out = pd.DataFrame(columns=CATALOG_HEADERS)
    meta = pd.DataFrame(CATALOG_TEMPLATE_ROWS)
    out = pd.concat([meta, out], ignore_index=True)

    # Map ERP fields
    mapped = pd.DataFrame(columns=CATALOG_HEADERS)
    for col in CATALOG_HEADERS:
        if col in ERP_TO_CATALOG_MAP:
            src = ERP_TO_CATALOG_MAP[col]
            mapped[col] = df[src] if src in df.columns else ""
        else:
            mapped[col] = ""

    # -----------------------------------------------------------------
    # Field-level Overrides and Custom Logic
    # -----------------------------------------------------------------

    # (1) Brand Code constant
    if "Brand Code" in mapped.columns:
        mapped["Brand Code"] = "CKC"

    # (2) Is Price on Request empty
    if "Is Price on Request" in mapped.columns:
        mapped["Is Price on Request"] = ""

    # (3) Length direct mapping
    if "Length" in df.columns:
        mapped["Length"] = df["Length"]

    # (4) SKU exact — preserve all digits, including leading zeros
    if "SKU Code" in mapped.columns and "Bar Code" in df.columns:
        mapped["SKU Code"] = df["Bar Code"].apply(barcode_to_ecomm_sku)

    # Use full exact barcode for image generation
    if "Bar Code" in df.columns:
        mapped["_sku_exact"] = df["Bar Code"].astype(str)

    # (4) PDP image placeholders using exact SKU
    for i in range(1, 16):
        col = f"PDP Image {i}"
        if col in mapped.columns:
            mapped[col] = mapped["_sku_exact"] + f"_{i}.jpg"

    # (5) PLP preview images blank
    for i in range(1, 4):
        col = f"PLP Preview Image {i} "
        if col in mapped.columns:
            mapped[col] = ""

    # -----------------------------------------------------------------
    # Default Field Values
    # -----------------------------------------------------------------
    defaults = {
        "Tags Keyword": "gold ring, Rhodolite Garnet ring, diamond gold ring, elegant gemstone ring, luxury jewelry, garnet diamond ring, statement gold ring, precious gemstone jewelry, garnet and diamond ring, timeless gold ring",
        "Meta Keyword": "gold ring, Rhodolite Garnet ring, diamond gold ring, elegant gemstone ring, luxury jewelry, garnet diamond ring, statement gold ring, precious gemstone jewelry, garnet and diamond ring, timeless gold ring",
        "Location Group": "India,America,Oceania,Asia",
        "Is Active(Y/N)": "Yes",
        "Is Publish(Y/N)": "Yes",
        "Is customizable? (Y/N)": "Yes",
        "Is 'New Arrival'": "Yes",
        "Is Try at Store": "Yes",
        "Is Try at Home": "Yes",
        "Is Free Shipping?": "Yes",
        "Product Net weight Unit": "Gms",
        "Product Gross Weight Unit": "Gms",
        "Min Quantity allowed in shopping cart": 1,
        "Max Quantity allowed in shopping cart": 1,
        "Delivery Type": "STANDARD",
        "Store Code": "S102",
        "Is Gift Wrap": "Yes",
        "Is inscription": "Yes",
        "Is Pick Up at store": "Yes",
        "Is EMI available": "No",
        "Is 'Trendy Fashion'": "Yes",
        "Is Returnable": "Yes",
        "Is Cancellable": "Yes"
    }
    for k, v in defaults.items():
        if k in mapped.columns:
            mapped[k] = v

    # (6) HighJewellery Flag empty
    if "HighJewellery Flag " in mapped.columns:
        mapped["HighJewellery Flag "] = ""

    # (7) Metal Type from Metal Name (input)
    if "Metal Type" in mapped.columns and "Metal Name" in df.columns:
        mapped["Metal Type"] = df["Metal Name"]

    # (8) Metal Name cleared
    if "Metal Name" in mapped.columns:
        mapped["Metal Name"] = ""

    # (9) pieces from input Pieces
    if "pieces" in mapped.columns and "Pieces" in df.columns:
        mapped["pieces"] = df["Pieces"]

    # -----------------------------------------------------------------
    # Product Highlights (based on Metal Name)
    # -----------------------------------------------------------------
    highlight_template = (
        "This product is made in {metal} gold verified by BIS hallmark, "
        "Product dimensions mentioned are on approximation closest to the actual size. "
        "The bill is your certificate, please produce the bill for future transactions "
        "on all jewellery, silverware, giftware you purchase. "
        "Diamond solitaires over quarter carat and certain rare gems may additionally "
        "have an external laboratory certificate."
    )

    if "Product Highlights" in mapped.columns:
        mapped["Product Highlights"] = df.get("Metal Name", "").fillna("").apply(
            lambda m: highlight_template.format(metal=m.strip()) if m.strip() else ""
        )

    # -----------------------------------------------------------------
    # Final Cleanup and Combine
    # -----------------------------------------------------------------
    mapped = mapped.drop(columns=["_sku_exact"], errors="ignore")

    final = pd.concat([out, mapped], ignore_index=True)
    return final, err
