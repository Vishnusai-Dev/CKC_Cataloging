
import streamlit as st
import pandas as pd
from io import BytesIO

from transformers.price import transform_price
from transformers.stone import transform_stone
from transformers.catalog import transform_catalog

st.set_page_config(page_title="Garnet Template Transformer", page_icon="💎", layout="wide")
st.title("💎 Garnet Template Transformer (v3)")
st.caption("Seller Price • Product Stone • Catalog Creation — all with embedded templates and validations.")

option = st.selectbox("Select output workflow", ["Seller Price", "Product Stone", "Catalog Creation"], index=2)

uploaded = st.file_uploader("Upload ERP Excel (.xlsx)", type=["xlsx"], key="erp_v3")
if uploaded is not None:
    try:
        df = pd.read_excel(uploaded)
        st.subheader("Input preview")
        st.dataframe(df.head(20))

        if option == "Seller Price":
            out_df, err_df = transform_price(df)
            filename = "SellerPriceBulkUpload.csv"
        elif option == "Product Stone":
            out_df, err_df = transform_stone(df)
            filename = "ProductStoneBulkUpload.csv"
        else:
            out_df, err_df = transform_catalog(df)
            filename = "CatalogUpload.csv"

        st.subheader("Output preview (first 20 rows)")
        st.dataframe(out_df.head(20))

        if not err_df.empty:
            st.warning("Validation issues found. Expand to review.")
            with st.expander("Row-level validation issues"):
                st.dataframe(err_df)

        buf = BytesIO()
        out_df.to_csv(buf, index=False)
        st.download_button("⬇️ Download " + filename, buf.getvalue(),
                           file_name=filename, mime="text/csv")

    except Exception as e:
        st.error(f"Error: {e}")

st.divider()
with st.expander("📘 Notes & Mappings"):
    st.markdown("""
**Seller Price**: CR_EcommSKUCode = CKC_00 + 8-digit Bar Code; Price_Group_Code blank.  
**Product Stone**: Stone Type = Article Type; Stone Name/Description = Article Description.  
**Catalog**: Logical ERP→Output mapping embedded; flags default to 'Y'.  
    """)

with st.expander("📎 Sample ERP files"):
    st.markdown("- samples/Sample_ERP_Price.xlsx")
    st.markdown("- samples/Sample_ERP_Stone.xlsx")
    st.markdown("- samples/Sample_ERP_Catalog.xlsx")
