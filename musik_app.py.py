import streamlit as st
import pandas as pd
import plotly.express as px

# =============================
# 🧠 1. Setup Awal
# =============================
st.set_page_config(page_title="Visualisasi Data Musik Spotify", layout="wide")

st.title("Visualisasi Data Musik Spotify")
st.write("Website ini menampilkan eksplorasi data musik berdasarkan genre, tahun, dan karakteristik lagu.")


@st.cache_data
def load_data():
    # Pastikan Anda menggunakan nama file yang benar (dataset_bersih.csv)
    # Jika dataset_bersih.csv ada di folder yang sama, ini sudah benar.
    df = pd.read_csv("dataset_bersih.csv")
    return df

df = load_data()

st.success("Dataset berhasil dimuat!")

# =============================
# 3. Sidebar untuk filter
# =============================
st.sidebar.header("🔍 Filter Data")
genre_filter = st.sidebar.multiselect("Pilih Genre:", df['genre'].unique())
# Menangani filter tahun, pastikan kolom 'year' sudah bersih
try:
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())
    year_filter = st.sidebar.slider("Pilih Rentang Tahun:", min_year, max_year, (min_year, max_year))
except ValueError:
    st.sidebar.error("Kolom 'year' mungkin mengandung nilai yang tidak valid.")
    # Fallback yang akan memfilter tahun secara minimal
    year_filter = (df['year'].min(), df['year'].max()) 

# Terapkan filter
filtered_df = df.copy()
if genre_filter:
    filtered_df = filtered_df[filtered_df['genre'].isin(genre_filter)]
# Pastikan perbandingan tahun menggunakan filter numerik yang sudah dikonversi
filtered_df = filtered_df[(filtered_df['year'].astype(int) >= year_filter[0]) & (filtered_df['year'].astype(int) <= year_filter[1])]

# =============================
# 4. Visualisasi
# =============================

st.header("1. Jumlah Lagu per Genre")

st.write("""
Grafik batang digunakan untuk membandingkan nilai antar kategori.  
Visualisasi ini membantu kita melihat kategori mana yang memiliki nilai tertinggi atau terendah dengan cepat.
""")

# --- KODE PERMANEN UNTUK PERBAIKAN PLOTLY ---
# BARIS KRITIS: Mengubah DataFrame agar kolomnya bernama 'Genre' dan 'Count'
genre_count = filtered_df['genre'].value_counts().reset_index()
genre_count.columns = ['Genre', 'Count'] 

# BARIS KRITIS: Menggunakan nama kolom yang benar di Plotly
fig_bar = px.bar(genre_count, x='Genre', y='Count',
                 labels={'Genre':'Genre', 'Count':'Jumlah Lagu'},
                 color='Genre', 
                 color_discrete_sequence=px.colors.qualitative.Plotly,
                 title="Distribusi Lagu Berdasarkan Genre")
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("**Insight:**  Genre dengan jumlah lagu terbanyak menggambarkan preferensi musik yang paling populer "
            "di kalangan pendengar Spotify dalam periode data yang dianalisis.")

# =============================
# 5. Line Chart: Tren Popularitas
# =============================
if 'year' in df.columns:
    st.header("2. Tren Rata-Rata Popularitas Lagu per Tahun")
    st.write("""
    Grafik garis digunakan untuk melihat perubahan rata-rata popularitas lagu dari tahun ke tahun.
    Visualisasi ini membantu mengidentifikasi tren peningkatan atau penurunan popularitas dalam industri musik.
    """)

    trend = filtered_df.groupby('year')['popularity'].mean().reset_index()
    fig_line = px.line(trend, x='year', y='popularity',
                        markers=True, color_discrete_sequence=['red'])
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown("**Insight:** Terlihat adanya fluktuasi tingkat popularitas lagu dari tahun ke tahun. "
            "Periode dengan rata-rata popularitas tinggi dapat mencerminkan munculnya genre atau artis yang sedang naik daun")

# =============================
# 6. Scatter Plot: Energy vs Danceability
# =============================
st.header("3. Hubungan Energy vs Danceability")
st.write("""
    Diagram sebar digunakan untuk melihat hubungan antara dua variabel numerik, yaitu *energy* dan *danceability*.
    Visualisasi ini membantu memahami bagaimana karakteristik lagu saling berhubungan.
    """)

fig_scatter = px.scatter(filtered_df, x='energy', y='danceability', color='popularity',
                          hover_data=['genre'], color_continuous_scale='Plasma',
                          title="Hubungan antara Energy dan Danceability Lagu")
st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("**Insight:** Lagu dengan tingkat *energy* tinggi umumnya juga memiliki *danceability* tinggi, "
            "menunjukkan korelasi positif antara kedua aspek ini dalam menciptakan lagu yang menarik untuk didengarkan dan ditarikan.")

# =============================
# 7. Footer
# =============================
st.write("---")
st.caption("Vanya Alifia Azzahra_220660121076_Untuk Tugas Visualisasi Data")