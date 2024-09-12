import streamlit as st
import pandas as pd
from cojinautos_insert import insert_data_cojinautos

def _extract_data_from_excel(excel_file):
    """Extracts data from the provided Excel file."""
    try:
        df = pd.read_excel(excel_file)
        return df
    except Exception as e:
        st.write(f"Error reading the Excel file: {e}")
        return pd.DataFrame()

st.title("Upload Cojinautos Excel files")

uploaded_file_1 = st.file_uploader("Cojinautos Clientes Excel file", type=["xls", "xlsx"])

uploaded_file_2 = st.file_uploader("Cojinautos Servicios Excel file", type=["xls", "xlsx"])

df_clients = None
df_services = None
merged_df = None

if uploaded_file_1 is not None:
    st.write("Clientes file was uploaded successfully.")
    df_clients = _extract_data_from_excel(uploaded_file_1)
    st.write(df_clients)

if uploaded_file_2 is not None:
    st.write("Servicios file was uploaded successfully.")
    df_services = _extract_data_from_excel(uploaded_file_2)
    st.write(df_services)

if df_clients is not None and df_services is not None:
    if st.button("Merge Files"):
        try:
            merged_df = pd.merge(df_clients, df_services, on='IDCustomer', how='inner')
            st.write("Merged data:")
            st.write(merged_df)
            insert_data_cojinautos(merged_df)
        except KeyError:
            st.write("Error: The column 'IDCustomer' is not present in both files.")


