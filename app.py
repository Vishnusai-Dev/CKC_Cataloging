
import streamlit as st
import pandas as pd
from io import BytesIO

from transformers.price import transform_price
from transformers.stone import transform_stone
from transformers.catalog import transform_catalog

st.set_page_config(page_title="Garnet Template Transformer", page_icon="💎", layout="wide")
st.title("💎 Garnet Template Transformer")
st.caption("Convert ERP inputs to upload-ready CSVs: Seller Price, Product Stone, and Catalog (flexible).")

option = st.selectbox("Select output workflow", ["Seller Price", "Product Stone", "Catalog Creation"], index=0)

if option in ["Seller Price", "Product Stone"]:
    uploaded = st.file_uploader("Upload ERP Excel (.xlsx)", type=["xlsx"], key="erp")
    if uploaded is not None:
        try:
            df = pd.read_excel(uploaded)
            st.subheader("Input preview")
            st.dataframe(df.head(20))

            if option == "Seller Price":
                out_df, err_df = transform_price(df)
                filename = "SellerPriceBulkUpload.csv"
            else:
                out_df, err_df = transform_stone(df)
                filename = "ProductStoneBulkUpload.csv"

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

else:
    st.info("For Catalog Creation, please upload both the ERP input and your Catalog output template CSV. Once you share the official template, we will embed it like the others.")
    col1, col2 = st.columns(2)
    with col1:
        erp = st.file_uploader("Upload ERP Catalog Excel (.xlsx)", type=["xlsx"], key="cat_erp")
    with col2:
        tpl = st.file_uploader("Upload Catalog Output Template (CSV)", type=["csv"], key="cat_tpl")

    if erp is not None and tpl is not None:
        try:
            df = pd.read_excel(erp)
            template_df = pd.read_csv(tpl)
            st.subheader("ERP input preview")
            st.dataframe(df.head(20))
            st.subheader("Template columns")
            st.write(list(template_df.columns))

            out_df = transform_catalog(df, template_df)

            st.subheader("Output preview (first 20 rows)")
            st.dataframe(out_df.head(20))

            buf = BytesIO()
            out_df.to_csv(buf, index=False)
            st.download_button("⬇️ Download CatalogUpload.csv", buf.getvalue(),
                               file_name="CatalogUpload.csv", mime="text/csv")
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
with st.expander("📘 Data Dictionary & Mappings"):
    st.markdown("""
**Seller Price (ERP → Output)**  
- CR_EcommSKUCode = CKC_00 + 8-digit Bar Code  
- CR_DiamondCost = Diamond Cost  
- CR_GemstoneCost = Stone Cost  
- CR_MakingCharges = Making  
- CR_WastageCharges = Wastage  
- CR_AccessoriesCost = Accessories Cost  
- CR_MetalCost = Metal Cost  
- CR_GSTCharges = GST  
- CR_Price_without_Promotion = Selling Price w/o Promotion  
- CR_Price_with_Promotion = Selling Price with Promotion  
- Price_Group_Code = (blank)

**Product Stone (ERP → Output)**  
- SKU_Code_Bar_Code = Main Batch Number  
- Stone Number = Stone Batch Number  
- Stone Type = Article Type  
- Stone Name = Article Description  
- Stone Description = Article Description  
- Stone(No. of Pieces) = Stone  No. of Pieces  
- Stone Origin/Appearance/Shape/Units/Cut/Clarity/Color = same  
- Stone Weight = Stone Weight  
- Stone Price = Stone Amount  
    """)

with st.expander("📎 Sample ERP files"):
    st.markdown("- samples/Sample_ERP_Price.xlsx")
    st.markdown("- samples/Sample_ERP_Stone.xlsx")
