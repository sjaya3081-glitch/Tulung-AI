import streamlit as st
import google.generativeai as genai
import tempfile
import os
import markdown

# 1. Mengatur Wajah Website
st.set_page_config(page_title="Tulung AI", page_icon="🤖")
st.title("🤖 TULUNG AI: Asisten Modul Pembelajaran Mendalam")
st.markdown("──────────────────────────────")
st.markdown("**Pilih kelas, ketik tujuan, upload KOSP (opsional), dan biarkan Tulung AI bekerja!**")

# 2. Pengaturan & Upload KOSP (Menu Samping)
st.sidebar.header("🔑 Pengaturan")
api_key = st.sidebar.text_input("Masukkan Kunci API Google Anda di sini:", type="password")

st.sidebar.markdown("──────────────────────────────")
st.sidebar.markdown("🏫 **Konteks Sekolah (Opsional)**")
kosp_file = st.sidebar.file_uploader("Upload KOSP Sekolah (Format PDF)", type=["pdf"])
st.sidebar.caption("Jika KOSP diunggah, Tulung AI akan membaca visi misi sekolah Anda untuk membuat modul yang jauh lebih kontekstual.")

# 3. Formulir Pesanan Guru
col1, col2 = st.columns(2)
with col1:
    jenjang = st.selectbox("🎓 Jenjang:", ["SD", "SMP", "SMA"])
with col2:
    kelas = st.selectbox("🏫 Kelas:", [str(i) for i in range(1, 13)])

mapel = st.text_input("📚 Mata Pelajaran:", placeholder="Contoh: IPAS")
tujuan = st.text_area("🎯 Tujuan Pembelajaran:", placeholder="Contoh: Peserta didik dapat menganalisis struktur dan fungsi organ tubuh manusia.")

# 4. Tombol Utama & Logika Berpikir AI
st.markdown("──────────────────────────────")
if st.button("🚀 MINTA TULUNG AI BUATKAN SEKARANG"):
    if not api_key:
        st.warning("⚠️ Masukkan Kunci API di menu sebelah kiri terlebih dahulu!")
    elif not mapel or not tujuan:
        st.warning("⚠️ Mata Pelajaran dan Tujuan Pembelajaran harus diisi!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            isi_pesan = []
            
            if kosp_file is not None:
                with st.spinner('Tulung AI sedang mempelajari Visi Misi dari KOSP sekolah Anda...'):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(kosp_file.getvalue())
                        tmp_path = tmp.name
                    
                    try:
                        file_ai = genai.upload_file(tmp_path)
                        isi_pesan.append(file_ai)
                    finally:
                        os.remove(tmp_path)
            
            prompt = f"""
            Kamu adalah Pakar Perancang Pembelajaran Mendalam tingkat nasional. 
            Tugasmu menyusun Modul Ajar untuk jenjang {jenjang} kelas {kelas} dengan mata pelajaran {mapel}.
            Tujuan pembelajaran: {tujuan}.
            
            ATURAN KHUSUS MEDIA (SANGAT PENTING - BACA DENGAN TELITI):
            1. DILARANG KERAS menggunakan format link markdown yang disembunyikan di balik teks seperti [Tonton Video](URL).
            2. Kamu WAJIB menaruh link/URL secara utuh dan mentah di dalam tanda kutip tunggal terbalik (backticks) agar sistem menguncinya sebagai teks murni yang bisa di-copy paste.
            
            ATURAN MUTLAK FORMAT:
            Kamu WAJIB mengeluarkan output menggunakan format persis seperti template di bawah ini. Jangan mengubah struktur.

            DAFTAR 8 DIMENSI PROFIL LULUSAN:
            1. Keimanan dan Ketakwaan Terhadap Tuhan Yang Maha Esa
            2. Kewargaan
            3. Penalaran Kritis
            4. Kreativitas
            5. Kolaborasi
            6. Kemandirian
            7. Kesehatan
            8. Komunikasi

            --- FORMAT YANG WAJIB DITIRU ---

            # PERENCANAAN PEMBELAJARAN MENDALAM
            **SEKOLAH** : [Isi dari KOSP atau kosongkan]
            **NAMA GURU** : [Kosongkan]
            **MATA PELAJARAN** : {mapel}
            **KELAS / SEMESTER** : {kelas} / [Isi Semester]
            **ALOKASI WAKTU** : [Isi waktu]

            ## IDENTIFIKASI
            * **Peserta Didik:** [Analisis ringkas]
            * **Materi Pelajaran:** [Fokus materi]
            * **Dimensi Profil Lulusan (DPL):** [Tuliskan dan tebalkan 2-4 DPL yang dipilih]

            ## DESAIN PEMBELAJARAN
            * **Capaian Pembelajaran:** [Capaian]
            * **Lintas Disiplin Ilmu:** [1 atau 2 mapel lain]
            * **Tujuan Pembelajaran:** {tujuan}
            * **Topik Pembelajaran:** [Topik utama]
            * **Praktik Pedagogis:** [Model dan Metode]
            * **Kemitraan Pembelajaran:** [Internal dan Eksternal]
            * **Lingkungan Pembelajaran:** [Budaya dan Ruang]
            * **Pemanfaatan Digital:** 
              - Alat bantu: [Sebutkan teknologi]
              - Video Referensi: `https://www.youtube.com/results?search_query=[ganti_dengan_kata_kunci_materi_spesifik]`
              - Gambar Referensi (Otomatis):
                ![Ilustrasi Pembelajaran](https://image.pollinations.ai/prompt/[ganti_dengan_kata_kunci_spesifik_berbahasa_inggris_tanpa_teks_tambahan]?width=800&height=600&nologo=true)
              - Link Gambar Mentah: `https://image.pollinations.ai/prompt/[ganti_dengan_kata_kunci_spesifik_berbahasa_inggris_tanpa_teks_tambahan]?width=800&height=600&nologo=true`

            ## PENGALAMAN BELAJAR
            **AWAL (Bermakna, Menggembirakan)**
            * [Tuliskan aktivitas Orientasi, Apersepsi, dan Motivasi]

            **INTI Memahami (Bermakna, Berkesadaran)**
            * [Tuliskan Penjelasan Terbimbing dan Aktivitas utama siswa]

            **Merefleksi (Bermakna dan berkesadaran)**
            * [Tuliskan aktivitas Presentasi/Tanggapan hasil belajar]

            **PENUTUP (Bermakna, Berkesadaran)**
            * [Tuliskan Kesimpulan, Refleksi, dan Tindak Lanjut]

            ## ASESMEN PEMBELAJARAN
            * **Asesmen pada Awal Pembelajaran:** [Teknik dan Instrumen]
            * **Asesmen pada Proses Pembelajaran:** [Teknik dan Instrumen]
            * **Asesmen pada Akhir Pembelajaran:** [Teknik dan Instrumen]

            ## RUBRIK PENILAIAN
            [Buat tabel Rubrik Penilaian dengan kolom: Indikator, Baru Memulai, Berkembang, Cakap, Mahir]
            """
            
            isi_pesan.append(prompt)
            
            with st.spinner('Tulung AI sedang merakit modul, memaksa link mentah, dan melukis ilustrasi untuk Anda...'):
                response = model.generate_content(isi_pesan)
                st.success("✅ Modul Ajar Profesional Berhasil Diciptakan!")
                
                st.markdown(response.text)
                
                html_text = markdown.markdown(response.text, extensions=['tables'])
                word_file = f"<html><head><meta charset='utf-8'></head><body>{html_text}</body></html>"
                
                st.markdown("──────────────────────────────")
                st.download_button(
                    label="📥 DOWNLOAD MODUL KE WORD (Pasti Rapi!)",
                    data=word_file,
                    file_name=f"Modul_Ajar_{mapel}_Kelas_{kelas}.doc",
                    mime="application/msword"
                )
                
        except Exception as e:
            st.error(f"Wah, ada sedikit kendala sistem: {e}")

# 5. Etalase Kasir
st.markdown("──────────────────────────────")
st.markdown("🔒 **MODUL TERKUNCI**")
st.markdown("Berlangganan Rp 50.000/Bulan untuk membuka hasil modul tanpa batas.")
st.markdown("💳 **Bayar Cepat via:** [ 🔵 **DANA** ]  [ 🔳 **QRIS** ]")
