import streamlit as st
import pandas as pd

st.set_page_config(page_title="Kimerizm Analiz Paneli", layout="centered")

st.title("Kimerizm Analiz Otomasyonu")
st.write("Elde edilen tüm sonuçlar genel ortalamaya katılacaktır.")

results = []
auto_counter = 1  #Isimsiz lokuslar için otomatik isimlendirme sayacı

# --- 1. MANUEL HESAPLAMA ALANI ---
st.subheader("Manuel Hesaplanacak Lokuslar")
num_calc = st.number_input("Formül Girilecek Lokus Sayısı (Boş bırakmak için 0 yapabilirsiniz)", min_value=0, max_value=20, value=1, step=1)

formula_options = [
    "2-2-4 Type-I: 4 Allel (Ad1+Ad2 / Ad1+Ad2+Ar1+Ar2)",
    "1-2-3 Type-I: 3 Allel - 1 Verici, 2 Alıcı (Ad / Ad+Ar1+Ar2)",
    "2-1-3 Type-I: 3 Allel - 2 Verici, 1 Alıcı (Ad1+Ad2 / Ad1+Ad2+Ar)",
    "1-1-2 ve 2-2-3 Type-I: 2 Allel (Ad / Ad+Ar)",
    "1-2-2 Type-II: Alıcı Formülü (1 - 2*Ar / Ar+A*)",
    "2-1-2 Type-II: Verici Formülü (2*Ad / Ad+A*)"
]

for i in range(int(num_calc)):
    st.markdown(f"### Lokus {i+1}")
    col1, col2 = st.columns(2)
    
    with col1:
        locus_name = st.text_input(f"Lokus Adı {i+1}", value=f"Man-Lokus-{i+1}", key=f"name_{i}")
        formula_type = st.selectbox(f"Formül Tipi {i+1}", formula_options, key=f"formula_{i}")
        
    with col2:
        val_val = 0.0
            
        if "4 Allel" in formula_type:
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

    st.info(f"**Bu Lokusun Donör Kimerizm Oranı:** %{val_val:.2f}")
    results.append({
        "Lokus": locus_name, 
        "Tip": formula_type.split(":")[0] if ":" in formula_type else formula_type, 
        "Kimerizm Oranı (%)": round(val_val, 2)
    })

st.markdown("---")

# --- 2. HIZLI TOPLU EKLEME ALANI  ---
st.subheader("Hızlı Veri Girişi (Tam Uyumlu / Uyumsuz Lokuslar)")
st.info("Manuel hesabı bitirdikten sonra, kalan %100 ve %0 lokusları buradan hızlıca ekleyebilirsiniz.")

# %100 Alanı
st.markdown("**1. Tam Uyumlu (%100) Lokuslar**")
col_100_1, col_100_2 = st.columns(2)
with col_100_1:
    num_100 = st.number_input("Otomatik %100 Eklenecek Lokus Sayısı", min_value=0, max_value=20, value=0, step=1, key="num_100")
with col_100_2:
    auto_100_names = st.text_input("Bu lokusların adları (İsteğe bağlı, virgülle ayırın)", placeholder="Örn: vWA, FGA", key="names_100")

if num_100 > 0:
    names_list_100 = [name.strip() for name in auto_100_names.split(",")] if auto_100_names else []
    for i in range(int(num_100)):
        if i < len(names_list_100) and names_list_100[i]:
            l_name = names_list_100[i]
        else:
            l_name = f"Oto-Lokus-{auto_counter}"
            auto_counter += 1
            
        results.append({
            "Lokus": l_name, 
            "Tip": "Toplu %100", 
            "Kimerizm Oranı (%)": 100.0
        })

# %0 Alanı
st.markdown("**2. Şüpheli / Tamamen Uyumsuz (%0) Lokuslar**")
col_0_1, col_0_2 = st.columns(2)
with col_0_1:
    num_0 = st.number_input("Otomatik %0 Eklenecek Lokus Sayısı", min_value=0, max_value=20, value=0, step=1, key="num_0")
with col_0_2:
    auto_0_names = st.text_input("Bu lokusların adları (İsteğe bağlı, virgülle ayırın)", placeholder="Örn: CSF1PO, TPOX", key="names_0")

if num_0 > 0:
    names_list_0 = [name.strip() for name in auto_0_names.split(",")] if auto_0_names else []
    for i in range(int(num_0)):
        if i < len(names_list_0) and names_list_0[i]:
            l_name = names_list_0[i]
        else:
            l_name = f"Oto-Lokus-{auto_counter}"
            auto_counter += 1
            
        results.append({
            "Lokus": l_name, 
            "Tip": "Toplu %0", 
            "Kimerizm Oranı (%)": 0.0
        })

st.markdown("---")

st.header("Genel Analiz Özeti")

df = pd.DataFrame(results)

st.table(df)

if not df.empty:
    mean_chimerism = df["Kimerizm Oranı (%)"].mean()
    st.success(f"**Ortalama Donör Kimerizm Oranı:** %{mean_chimerism:.2f}")
