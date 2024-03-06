import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib.gridspec as gridspec

sns.set(style='dark')

# Load the data
product_review_revenue_order_df = pd.read_csv("product_review_revenue_order_df.csv")

def create_monthly_orders_df(df, year):
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])  # Konversi ke tipe data datetime
    df_year = df[df['order_purchase_timestamp'].dt.year == year]

    monthly_orders_df = df_year.resample(rule='ME', on='order_purchase_timestamp').agg({
        "payment_value": "sum"
    })
    monthly_orders_df.index = monthly_orders_df.index.strftime('%B')

    monthly_orders_df = monthly_orders_df.reset_index()
    monthly_orders_df.rename(columns={
        "payment_value": "revenue"
    }, inplace=True)

    return monthly_orders_df




# Create subplots with specified grid layout
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(15, 5),
                       gridspec_kw={'width_ratios': [4, 4, 4]})

# Call the function to get DataFrames for each year and plot
for i, year in enumerate([2016, 2017, 2018]):
    monthly_orders_df = create_monthly_orders_df(product_review_revenue_order_df, year)

    ax[i].plot(monthly_orders_df["order_purchase_timestamp"], monthly_orders_df["revenue"], marker='o', linewidth=2, color="#72BCD4")
    ax[i].set_title(f"Revenue per Month ({year})", fontsize=10)
    ax[i].tick_params(axis='x', rotation=45, labelrotation=45, labelsize=10)
    ax[i].tick_params(axis='y', labelsize=10)

# Adjust the layout to add space between subplots
plt.subplots_adjust(wspace=0.4)

# Display the subplots using st.pyplot(fig)
st.pyplot(fig)


# Fungsi untuk membuat plot kategori produk terbaik dan terburuk
def plot_best_worst_categories(data):
    # Proses pengolahan data
    produk_daya_jual_tinggi = data.groupby(by="product_category_name_english").agg({
        'product_id' : 'nunique',
        'review_score' :'mean',
    }).sort_values(by='product_id', ascending = False)

    produk_daya_jual_tinggi.rename(columns={
        "product_id": "Total Barang",
        "review_score" : "Rating"
    }, inplace=True)

    # Membuat plot menggunakan Seaborn dan Matplotlib
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    # Plot terbaik
    sns.barplot(x="Total Barang", y="product_category_name_english", data=produk_daya_jual_tinggi.head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Best Penjualan Kategori Produk", loc="center", fontsize=15)
    ax[0].tick_params(axis='y', labelsize=12)

    # Plot terburuk
    sns.barplot(x="Total Barang", y="product_category_name_english", data=produk_daya_jual_tinggi.sort_values(by="Total Barang", ascending=True).head(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Worst Penjualan Kategori Produk", loc="center", fontsize=15)
    ax[1].tick_params(axis='y', labelsize=12)

    # Menampilkan judul keseluruhan
    plt.suptitle("Best and Worst Penjualan Kategori Produk", fontsize=20)

    # Menampilkan plot di Streamlit
    st.pyplot(fig)


# Fungsi untuk membuat plot kategori produk berdasarkan rating
def plot_best_worst_rating(data):
    # Proses pengolahan data
    Rating_Produk = data.groupby(by="product_category_name_english").agg({
        'review_score': 'mean',
    }).sort_values(by='review_score', ascending=False)

    Rating_Produk.rename(columns={
        "review_score": "Rating"
    }, inplace=True)

    # Membuat plot menggunakan Seaborn dan Matplotlib
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    # Plot rating terbaik
    sns.barplot(x="Rating", y="product_category_name_english", data=Rating_Produk.head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Best Rating Kategori Produk", loc="center", fontsize=15)
    ax[0].tick_params(axis='y', labelsize=12)

    # Plot rating terburuk
    sns.barplot(x="Rating", y="product_category_name_english", data=Rating_Produk.sort_values(by="Rating", ascending=True).head(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Worst Rating Kategori Produk", loc="center", fontsize=15)
    ax[1].tick_params(axis='y', labelsize=12)

    # Menampilkan judul keseluruhan
    plt.suptitle("Best and Worst Rating Kategori Produk", fontsize=20)

    # Menampilkan plot di Streamlit
    st.pyplot(fig)

if __name__ == '__main__':

    # Menampilkan plot di aplikasi Streamlit
    plot_best_worst_categories(product_review_revenue_order_df)
    plot_best_worst_rating(product_review_revenue_order_df)