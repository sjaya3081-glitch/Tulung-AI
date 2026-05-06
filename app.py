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
            
            prompt = f"""Kamu adalah Pakar Perancang Pembelajaran Mendalam tingkat nasional. 
Tugasmu menyusun Modul Ajar untuk jenjang {jenjang} kelas {kelas} dengan mata pelajaran {mapel}.
Tujuan pembelajaran: {tujuan}.

ATURAN KHUSUS MEDIA:
1. DILARANG KERAS memunculkan atau merender gambar secara langsung.
2. Kamu HANYA BOLEH memberikan URL/Link mentahnya saja untuk referensi video dan gambar.
3. Taruh link tersebut di dalam tanda kutip tunggal terbalik (backticks) agar sistem menguncinya sebagai teks murni yang bisa di-copy paste.
4. Untuk gambar, berikan link pencarian cerdas ke Google Images dan Pinterest sesuai materi pembelajaran.

ATURAN MUTLAK FORMAT:
Kamu WAJIB mengeluarkan output menggunakan format persis seperti template di bawah ini. Jangan mengubah struktur. Pada bagian PENGALAMAN BELAJAR, WAJIB gunakan format nomor (1, 2, 3) langkah demi langkah, DILARANG menulis paragraf panjang.

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
  - Link Referensi Video: `https://www.youtube.com/results?search_query=[ganti_dengan_kata_kunci_materi_spesifik]`
  - Link Referensi Gambar (Google): `https://www.google.com/search?tbm=isch&q=[ganti_dengan_kata_kunci_materi_spesifik]`
  - Link Ide Visual (Pinterest): `https://id.pinterest.com/search/pins/?q=[ganti_dengan_kata_kunci_materi_spesifik]`

## PENGALAMAN BELAJAR
**AWAL (Bermakna, Menggembirakan)**
1. **Orientasi:** [Tuliskan langkah-langkah guru membuka pelajaran]
2. **Apersepsi:** [Tuliskan langkah guru mengaitkan materi dengan pengalaman siswa]
3. **Motivasi:** [Tuliskan langkah guru memberikan semangat dan tujuan belajar]

**INTI Memahami (Bermakna, Berkesadaran)**
1. **Penjelasan Terbimbing:** [Tuliskan langkah guru menjelaskan konsep awal]
2. **Aktivitas Siswa Langkah 1:** [Tuliskan apa yang dilakukan siswa secara spesifik]
3. **Aktivitas Siswa Langkah 2:** [Tuliskan langkah lanjutan diskusi atau pengerjaan tugas]

**Merefleksi (Bermakna dan berkesadaran)**
1. **Presentasi:** [Tuliskan langkah siswa menyampaikan hasil kerjanya]
2. **Tanggapan:** [Tuliskan langkah siswa lain/guru memberikan umpan balik]

**PENUTUP (Bermakna, Berkesadaran)**
1. **Kesimpulan:** [Tuliskan langkah menyimpulkan pembelajaran bersama]
2. **Refleksi:** [Tuliskan langkah evaluasi perasaan/pemahaman siswa hari ini]
3. **Tindak Lanjut:** [Tuliskan instruksi tugas atau persiapan materi berikutnya]

## ASESMEN PEMBELAJARAN
* **Asesmen pada Awal Pembelajaran:** [Teknik dan Instrumen]
* **Asesmen pada Proses Pembelajaran:** [Teknik dan Instrumen]
* **Asesmen pada Akhir Pembelajaran:** [Teknik dan Instrumen]

## RUBRIK PENILAIAN
[Buat tabel Rubrik Penilaian dengan kolom: Indikator, Baru Memulai, Berkembang, Cakap, Mahir]
"""
            
            isi_pesan.append(prompt)
            
            with st.spinner('Tulung AI sedang merakit modul dan menyusun langkah demi langkah...'):
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
