import streamlit as st
import pandas as pd

st.set_page_config(page_title="Kimerizm Analiz Paneli", layout="centered")

st.title("Kimerizm Analiz Otomasyonu")
st.write("Formül tiplerini seçerek pik değerlerini girin. Elde edilen tüm sonuçlar (manuel eklenen sıfırlar dahil) genel ortalamaya katılacaktır.")

# Dinamik lokus sayısı belirleme
num_loci = st.number_input("Analiz Edilecek Toplam Lokus Sayısı", min_value=1, max_value=20, value=4, step=1)

results = []

formula_options = [
    "2-2-4 Type-I: 4 Allel (Ad1+Ad2 / Ad1+Ad2+Ar1+Ar2)",
    "1-2-3 Type-I: 3 Allel - 1 Verici, 2 Alıcı (Ad / Ad+Ar1+Ar2)",
    "2-1-3 Type-I: 3 Allel - 2 Verici, 1 Alıcı (Ad1+Ad2 / Ad1+Ad2+Ar)",
    "1-1-2 ve 2-2-3 Type-I: 2 Allel (Ad / Ad+Ar)",
    "1-2-2 Type-II: Alıcı Formülü (1 - 2*Ar / Ar+A*)",
    "2-1-2 Type-II: Verici Formülü (2*Ad / Ad+A*)",
    "Manuel Sıfır (Şüpheli / Uyumsuz Profil)"
]

for i in range(int(num_loci)):
    st.markdown(f"### Lokus {i+1}")
    col1, col2 = st.columns(2)
    
    with col1:
        locus_name = st.text_input(f"Lokus Adı {i+1}", value=f"STR-{i+1}", key=f"name_{i}")
        formula_type = st.selectbox(f"Formül Tipi {i+1}", formula_options, key=f"formula_{i}")
        
    with col2:
        val_val = 0.0
        
        if "Manuel Sıfır" in formula_type:
            st.warning("Bu lokus şüpheli/uyumsuz kabul edilerek ortalamaya direkt %0 olarak katılacaktır.")
            val_val = 0.0
            
        elif "4 Allel" in formula_type:
            ad1 = st.number_input("Ad1 Değeri", min_value=0.0, value=None, key=f"ad1_{i}") or 0.0
            ad2 = st.number_input("Ad2 Değeri", min_value=0.0, value=None, key=f"ad2_{i}") or 0.0
            ar1 = st.number_input("Ar1 Değeri", min_value=0.0, value=None, key=f"ar1_{i}") or 0.0
            ar2 = st.number_input("Ar2 Değeri", min_value=0.0, value=None, key=f"ar2_{i}") or 0.0
            denominator = ad1 + ad2 + ar1 + ar2
            if denominator > 0:
                val_val = 100.0 * (ad1 + ad2) / denominator
                
        elif "3 Allel - 1 Verici" in formula_type:
            ad = st.number_input("Ad Değeri", min_value=0.0, value=None, key=f"ad_3v1_{i}") or 0.0
            ar1 = st.number_input("Ar1 Değeri", min_value=0.0, value=None, key=f"ar1_3v1_{i}") or 0.0
            ar2 = st.number_input("Ar2 Değeri", min_value=0.0, value=None, key=f"ar2_3v1_{i}") or 0.0
            denominator = ad + ar1 + ar2
            if denominator > 0:
                val_val = 100.0 * ad / denominator
                
        elif "3 Allel - 2 Verici" in formula_type:
            ad1 = st.number_input("Ad1 Değeri", min_value=0.0, value=None, key=f"ad1_2v3_{i}") or 0.0
            ad2 = st.number_input("Ad2 Değeri", min_value=0.0, value=None, key=f"ad2_2v3_{i}") or 0.0
            ar = st.number_input("Ar Değeri", min_value=0.0, value=None, key=f"ar_2v3_{i}") or 0.0
            denominator = ad1 + ad2 + ar
            if denominator > 0:
                val_val = 100.0 * (ad1 + ad2) / denominator
                
        elif "2 Allel" in formula_type:
            ad = st.number_input("Ad Değeri", min_value=0.0, value=None, key=f"ad_2a_{i}") or 0.0
            ar = st.number_input("Ar Değeri", min_value=0.0, value=None, key=f"ar_2a_{i}") or 0.0
            denominator = ad + ar
            if denominator > 0:
                val_val = 100.0 * ad / denominator
                
        elif "Alıcı Formülü" in formula_type:
            ar = st.number_input("Ar Değeri", min_value=0.0, value=None, key=f"ar_t2r_{i}") or 0.0
            a_star = st.number_input("A* Değeri", min_value=0.0, value=None, key=f"astar_t2r_{i}") or 0.0
            denominator = ar + a_star
            if denominator > 0:
                val_val = 100.0 * (1.0 - (2.0 * ar) / denominator)
                
        elif "Verici Formülü" in formula_type:
            ad = st.number_input("Ad Değeri", min_value=0.0, value=None, key=f"ad_t2d_{i}") or 0.0
            a_star = st.number_input("A* Değeri", min_value=0.0, value=None, key=f"astar_t2d_{i}") or 0.0
            denominator = ad + a_star
            if denominator > 0:
                val_val = 100.0 * (2.0 * ad) / denominator

    st.info(f"**Bu Lokusun Kimerizm Sonucu:** %{val_val:.2f}")
    results.append({
        "Lokus": locus_name, 
        "Tip": formula_type.split(":")[0], 
        "Kimerizm_%": round(val_val, 2)
    })
    st.markdown("---")

st.header("📊 Genel Analiz Özeti")

df = pd.DataFrame(results)

st.table(df)

if not df.empty:
    mean_chimerism = df["Kimerizm_%"].mean()
    st.success(f"**Ortalama Kimerizm Sonucu:** %{mean_chimerism:.2f}")
