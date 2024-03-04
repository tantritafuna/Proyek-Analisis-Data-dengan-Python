import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Membaca data CSV
customers_df = pd.read_csv("https://raw.githubusercontent.com/tantritafuna/e-commerce-dataset/main/customers_dataset.csv")
order_payments_df = pd.read_csv("https://raw.githubusercontent.com/tantritafuna/e-commerce-dataset/main/order_payments_dataset.csv")
order_reviews_df = pd.read_csv("https://raw.githubusercontent.com/tantritafuna/e-commerce-dataset/main/order_reviews_df.csv")

# Pengolahan data
datetime_columns = ["review_creation_date"]
order_reviews_df.sort_values(by="review_creation_date", inplace=True)
order_reviews_df.reset_index(inplace=True)
for column in datetime_columns:
    order_reviews_df[column] = pd.to_datetime(order_reviews_df[column])

min_date = order_reviews_df["review_creation_date"].min()
max_date = order_reviews_df["review_creation_date"].max()

# Menampilkan data menggunakan Streamlit
st.sidebar.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", use_column_width=True)

# Menambahkan date_input di sidebar
start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu', min_value=min_date, max_value=max_date, value=[min_date, max_date]
)

# Memfilter data berdasarkan rentang waktu
main_df = order_reviews_df[(order_reviews_df["review_creation_date"] >= str(start_date)) & 
                            (order_reviews_df["review_creation_date"] <= str(end_date))]

# Menambahkan header pada dashboard
st.header('E-Commerce Public Dashboard :sparkles:')

# Menampilkan barchart jumlah pelanggan berdasarkan negara bagian
bystate_df = customers_df.groupby(by="customer_state").customer_id.nunique().reset_index()
bystate_df.rename(columns={"customer_id": "customer_count"}, inplace=True)
st.subheader("Number of Customer by States")
fig, ax = plt.subplots(figsize=(10, 5))
colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="customer_count", 
    y="customer_state",
    data=bystate_df.sort_values(by="customer_count", ascending=False),
    palette=colors_,
    ax=ax
)
st.pyplot(fig)

# Menampilkan barchart jumlah transaksi berdasarkan metode pembayaran
sum_payment_type_df = order_payments_df.groupby("payment_type")['order_id'].count().sort_values(ascending=False).reset_index()
sum_payment_type_df.columns = ['payment_type', 'transaction_count']
st.subheader('Number of Transactions by Payment Type')
fig, ax = plt.subplots(figsize=(10, 5))
colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
ax.barh(sum_payment_type_df['payment_type'], sum_payment_type_df['transaction_count'], color=colors_)
st.pyplot(fig)