
# Garnet Template Transformer — v2 (Modular + Validations)

Streamlit app to convert ERP Excel inputs into upload-ready CSVs for:
- Seller Price Bulk Upload (embedded template)
- Product Stone Bulk Upload (embedded template)
- Catalog Creation (flexible; can embed once template is provided)

## What's new in v2
- Modular transformers (price, stone, catalog)
- Embedded templates for Price & Stone (first 4 metadata rows preserved)
- Row-level validations with an issue viewer
- Data Dictionary (input → output)
- Sample ERP input files included

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Catalog Creation
Until you provide the official **Catalog output template CSV**, the app supports a flexible mode:
- Upload ERP Catalog Excel
- Upload your Catalog output template CSV
- The app will align by column names and preserve the first 4 metadata rows if present.
Once you share the final template, we'll embed it just like Price & Stone.

## Templates (embedded)
- templates/SellerPriceBulkUpload.csv
- templates/ProductStoneBulkUpload.csv

## Samples
- samples/Sample_ERP_Price.xlsx
- samples/Sample_ERP_Stone.xlsx
