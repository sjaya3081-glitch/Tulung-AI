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
            
            ATURAN KHUSUS KOSP & MEDIA:
            1. KONTEKS KOSP: Jika ada dokumen KOSP yang dilampirkan, pelajari visi, misi, dan karakteristik sekolah tersebut. Jadikan informasi dari KOSP sebagai dasar penentuan 'Kemitraan Pembelajaran', 'Lingkungan Pembelajaran', dan rancang 'Pengalaman Belajar' agar modul ini sangat kontekstual dengan sekolah tersebut.
            2. MEDIA VIDEO: Pada bagian Pemanfaatan Digital, jika kamu merekomendasikan video, WAJIB sertakan link pencarian cerdas YouTube dengan format: [Tonton Referensi Video di YouTube](https://www.youtube.com/results?search_query=kata+kunci+materi+spesifik)
            3. MEDIA GAMBAR/POSTER: Pada bagian Pemanfaatan Digital, buatkan gambar otomatis menggunakan layanan Pollinations. Agar gambarnya pantas untuk buku pelajaran dan tidak abstrak/menyeramkan, kamu WAJIB menggunakan bahasa Inggris untuk URL-nya dan tambahkan kata kunci gaya desain edukasi. Gunakan format persis seperti ini:
               ![Deskripsi Gambar](https://image.pollinations.ai/prompt/high+quality+educational+illustration+of+[TOPIK+SPESIFIK]+clear+vector+flat+design+for+kids+textbook?width=800&height=600&nologo=true)
               Contoh: ![Sistem Pencernaan](https://image.pollinations.ai/prompt/high+quality+educational+illustration+of+human+digestive+system+anatomy+clear+vector+flat+design+for+kids+textbook?width=800&height=600&nologo=true)
            
            ATURAN MUTLAK FORMAT:
            Kamu WAJIB mengeluarkan output menggunakan format persis seperti template di bawah ini. Jangan mengubah judul bagian. Gunakan Markdown agar rapi (termasuk tabel untuk rubrik).
            Pilih dan tebalkan (bold) 8 Dimensi Profil Lulusan yang paling relevan pada bagian 'IDENTIFIKASI'.

            DAFTAR 8 DIMENSI PROFIL LULUSAN:
            1. Keimanan dan Ketakwaan Terhadap Tuhan Yang Maha Esa: Memiliki landasan iman yang kuat, akhlak mulia, dan nilai spiritual.
            2. Kewargaan: Menjadi warga yang baik, disiplin, bertanggung jawab, menghargai aturan, dan bangga pada keberagaman Indonesia.
            3. Penalaran Kritis: Mampu memproses informasi, menganalisis, mengevaluasi, dan menyimpulkan secara objektif.
            4. Kreativitas: Menghasilkan gagasan atau karya asli dan inovatif.
            5. Kolaborasi: Kemampuan bekerja sama dan berinteraksi secara positif dalam kelompok.
            6. Kemandirian: Bertanggung jawab atas proses dan hasil belajarnya sendiri.
            7. Kesehatan: Memiliki kesadaran dan sikap peduli dalam menjaga kesehatan fisik, mental diri, dan lingkungan.
            8. Komunikasi: Kemampuan menyampaikan ide secara jelas, efektif, dan sopan.

            --- FORMAT YANG WAJIB DITIRU ---

            # PERENCANAAN PEMBELAJARAN MENDALAM
            **SEKOLAH** : [Isi otomatis berdasarkan nama sekolah di KOSP jika ada, jika tidak kosongkan]
            **NAMA GURU** : [Kosongkan]
            **MATA PELAJARAN** : {mapel}
            **KELAS / SEMESTER** : {kelas} / [Isi Semester yang logis]
            **ALOKASI WAKTU** : [Isi waktu yang logis]

            ## IDENTIFIKASI
            * **Peserta Didik:** [Buat analisis ringkas tahap perkembangan siswa kelas {kelas}]
            * **Materi Pelajaran:** [Buat fokus materi pelajaran]
            * **Dimensi Profil Lulusan (DPL):** [Tuliskan dan tebalkan 2-4 DPL yang dipilih dari daftar di atas]

            ## DESAIN PEMBELAJARAN
            * **Capaian Pembelajaran:** [Buat capaian yang sesuai materi]
            * **Lintas Disiplin Ilmu:** [Sebutkan 1 atau 2 mapel lain yang terkait dan alasannya]
            * **Tujuan Pembelajaran:** {tujuan}
            * **Topik Pembelajaran:** [Topik utama]
            * **Praktik Pedagogis:** [Sebutkan Model dan Metode yang digunakan]
            * **Kemitraan Pembelajaran:** [Sebutkan kemitraan Internal dan Eksternal]
            * **Lingkungan Pembelajaran:** [Jelaskan Budaya Belajar dan Ruang Fisik]
            * **Pemanfaatan Digital:** [Sebutkan teknologi/alat bantu. WAJIB sertakan LINK YOUTUBE pencarian cerdas DAN buatkan GAMBAR/POSTER otomatis menggunakan link pollinations.ai sesuai aturan!]

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
            
            with st.spinner('Tulung AI sedang merakit modul, merekomendasikan video, dan melukis poster untuk Anda...'):
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
