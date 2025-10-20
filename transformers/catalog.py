from typing import List, Dict, Tuple
import pandas as pd
from .common import barcode_to_ecomm_sku, validate_catalog_input

# ---------------------------------------------------------------------
# 1. Catalog Template Headers (embedded)
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
# 3. Logical ERP → Catalog Mapping
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
    "Pieces UOM": "UOM"
}

# ---------------------------------------------------------------------
# 4. Transformer Function
# ---------------------------------------------------------------------
def transform_catalog(input_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Transforms ERP catalog input to upload-ready catalog format with defaults & image placeholders."""
    df, err = validate_catalog_input(input_df.copy())

    # Base structure
    out = pd.DataFrame(columns=CATALOG_HEADERS)
    meta = pd.DataFrame(CATALOG_TEMPLATE_ROWS)
    out = pd.concat([meta, out], ignore_index=True)

    mapped = pd.DataFrame(columns=CATALOG_HEADERS)
    for col in CATALOG_HEADERS:
        if col in ERP_TO_CATALOG_MAP:
            src = ERP_TO_CATALOG_MAP[col]
            mapped[col] = df[src] if src in df.columns else ""
        else:
            mapped[col] = ""

    # Generate SKU Code with prefix
    if "SKU Code" in mapped.columns and "Bar Code" in df.columns:
        mapped["SKU Code"] = df["Bar Code"].apply(barcode_to_ecomm_sku)

    # Derive SKU short code (without CKC prefix) for image filenames
    mapped["_sku_short"] = mapped["SKU Code"].astype(str).str.replace("CKC_00", "", regex=False)

    # -----------------------------------------------------------------
    #  Default static field values
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
        "Is Price on Request": "No",
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
        "Is Cancellable": "Yes",
    }
    for k, v in defaults.items():
        if k in mapped.columns:
            mapped[k] = v

    # -----------------------------------------------------------------
    #  Image Placeholders (SKU_1.jpg … SKU_15.jpg, PLP images)
    # -----------------------------------------------------------------
    for i in range(1, 16):
        col = f"PDP Image {i}"
        if col in mapped.columns:
            mapped[col] = mapped["_sku_short"] + f"_{i}.jpg"

    for i in range(1, 4):
        col = f"PLP Preview Image {i} "
        if col in mapped.columns:
            mapped[col] = mapped["_sku_short"] + f"_plp{i}.jpg"

    # Drop helper column
    mapped = mapped.drop(columns=["_sku_short"], errors="ignore")

    # Combine metadata + mapped data
    final = pd.concat([out, mapped], ignore_index=True)
    return final, err
