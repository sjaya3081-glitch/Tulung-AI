import streamlit as st
import google.generativeai as genai

# 1. Mengatur Wajah Website
st.set_page_config(page_title="Tulung AI", page_icon="🤖")
st.title("🤖 TULUNG AI: Asisten Modul Ajar Otomatis")
st.markdown("──────────────────────────────")
st.markdown("**Pilih kelasnya, ketik tujuannya, biarkan Tulung AI bekerja!**")

# 2. Kolom Rahasia untuk Kunci AI
st.sidebar.header("🔑 Pengaturan")
api_key = st.sidebar.text_input("Masukkan Kunci API Google Anda di sini:", type="password")

# 3. Formulir Pesanan Guru
col1, col2 = st.columns(2)
with col1:
    jenjang = st.selectbox("🎓 Jenjang:", ["SD", "SMP", "SMA"])
with col2:
    kelas = st.selectbox("🏫 Kelas:", [str(i) for i in range(1, 13)])

mapel = st.text_input("📚 Mata Pelajaran:", placeholder="Contoh: IPAS")
tujuan = st.text_area("🎯 Tujuan Pembelajaran:", placeholder="Contoh: Siswa mampu menganalisis rotasi bumi dan dampaknya terhadap siang dan malam.")

# 4. Tombol Utama & Logika Berpikir AI
st.markdown("──────────────────────────────")
if st.button("🚀 MINTA TULUNG AI BUATKAN SEKARANG"):
    if not api_key:
        st.warning("⚠️ Masukkan Kunci API di menu sebelah kiri terlebih dahulu!")
    elif not mapel or not tujuan:
        st.warning("⚠️ Mata Pelajaran dan Tujuan Pembelajaran harus diisi!")
    else:
        try:
            # Menyambungkan Kunci AI
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Buku Panduan (Prompt)
            prompt = f"""
            Kamu adalah Asisten Perancang Pembelajaran tingkat nasional. 
            Tugasmu merancang Modul Ajar untuk jenjang {jenjang} kelas {kelas} dengan mata pelajaran {mapel}.
            Tujuan pembelajaran hari ini adalah: {tujuan}.
            
            Aturan baku:
            1. Gunakan format 8 Dimensi Profil Lulusan.
            2. Sesuaikan gaya bahasa dan materi dengan siswa {jenjang} kelas {kelas}.
            3. Terapkan prinsip Pembelajaran Mendalam (Deep Learning).
            4. Berikan rekomendasi alat peraga visual yang menarik.
            """
            
            with st.spinner('Tulung AI sedang mengetik modul untuk Anda...'):
                response = model.generate_content(prompt)
                st.success("✅ Modul Berhasil Dibuat!")
                st.write(response.text)
        except Exception as e:
            st.error(f"Wah, ada sedikit kendala: {e}")

# 5. Etalase Kasir (Untuk Fase Selanjutnya)
st.markdown("──────────────────────────────")
st.markdown("🔒 **MODUL TERKUNCI**")
st.markdown("Berlangganan Rp 50.000/Bulan untuk membuka hasil modul tanpa batas.")
st.markdown("💳 **Bayar Cepat via:** [ 🔵 **DANA** ]  [ 🔳 **QRIS** ]")
