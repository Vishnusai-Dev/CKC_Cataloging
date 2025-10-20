
# Garnet Template Transformer — v3 (Catalog Included)

Streamlit app to convert ERP Excel inputs into upload-ready CSVs for:
- Seller Price (embedded template)
- Product Stone (embedded template)
- Catalog Creation (embedded template)

## Highlights
- All three templates embedded; preserves first 4 metadata rows.
- Logical ERP → Catalog mapping included.
- Row-level validations with an issue viewer.
- Sample ERP inputs included.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Cloud
- Push the repo to GitHub
- Set **Main file** to `app.py`

## Notes
- SKU Code = CKC_00 + 8-digit Bar Code
- Stone Type = Article Type
- Defaults: Is Active/Publish/Returnable/Cancellable = 'Y'
