from .chat import groq_completion

def rag_decider_agent(chat):
    system_prompt = """
        Kamu adalah asisten pintar. Kamu mempunyai 2 sumber informasi yaitu dokumen dan tabel data.
        Dokumen berisi informasi:
        Berikut ringkasan dokumen:

Struktur Analisis:
- Analisis kondisi kredit di Indonesia
- Fokus pada populasi peminjam dan strategi persetujuan kredit
- Studi kasus 3 perusahaan (A, B, C)

Temuan Utama:
1. Demografi Peminjam:
- Mayoritas usia 25-45 tahun
- Dominasi di daerah perkotaan 
- Tingkat pendidikan mempengaruhi akses
- 55'%' laki-laki, 45% perempuan

2. Pola Kredit:
- Segmen UKM mendominasi (40%)
- Preferensi bunga tetap dan tenor panjang
- Platform digital berkembang pesat
- Kesenjangan akses kredit desa-kota

3. Pendekatan Perusahaan:
- Perusahaan A: Fokus teknologi
- Perusahaan B: Fokus keberlanjutan
- Perusahaan C: Konservatif

4. Manajemen Risiko:
- Kombinasi skor kredit tradisional dan data alternatif
- Penggunaan machine learning dan AI
- Riwayat kredit dan kemampuan bayar
- Tingkat risiko 20-30%

5. Rekomendasi:
- Pengembangan infrastruktur digital
- Peningkatan edukasi keuangan 
- Penyempurnaan model penilaian risiko
- Pengembangan produk kredit sesuai segmen
- Kolaborasi antar lembaga keuangan

Dokumen memberikan data komprehensif tentang pasar kredit Indonesia dan strategi detail untuk meningkatkan proses persetujuan kredit.
        dokumen tersebut menyimpan terkait informasi tentang penggunaan untuk persetujuan kredit.
        tabel tersebut terdapat kolom terkait 

        Id                                    int64
        age                                   int64
        gender                               object 
        job                                  object
        monthly_salary                      float64
        electrical_bill_monthly             float64
        max_Day_past_due_loan                 int64
        current_day_past_due_loan             int64
        loan_outstanding_total              float64
        credit_score                          int64
        last_date_loan_created       datetime64[ns]

        tidak perlu pakai ID untuk membalas. 
        """
    user_prompt = f"""
           Tentukan apakah pertanyaan ini membutuhkan data dari tabel atau tidak?
           pertanyaan: {chat}   

            hanya jawab dengan "ya" atau "tidak", jangan memberikan jawaban lain akan merusak format.
        """
    result = groq_completion(user_prompt,system_prompt).lower()

    return result