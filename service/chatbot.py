from .data_agent.query_agent import query_result
from .chat import groq_completion
from utils.query_executor import execute_query
from exception.DatabaseException import DatabaseError
from .decider import rag_decider_agent
from db.vector_db_instance import query_vector_db


sys_prompt_no_data = """
    Kamu adalah asisten pintar yang menjawab pertanyaan terkait kredit dan persetujuan pengajuan kredit di Indonesia.
    Nama kamu adalah Asli asisten pintar tentang data kredit.
    Anda mempunyai pengetahuan dari dokumen dan tabel. 
    Berikut Dokumen berisi informasi:
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

    Berikut informasi kolom tabel yang anda punya :
     Id                                    int64 
        age                                   int64 umur
        gender                               object  kolom gender berisi "Male" berarti Pria dan "Female" berarti Wania
        job                                  object pekerjaan
        monthly_salary                      float64 dalam rupiah
        electrical_bill_monthly             float64 dalam rupiah
        max_Day_past_due_loan                 int64 Keterlambatan maksimal yang pernah dilakukan dalam peminjaman
        current_day_past_due_loan             int64 Data keterlambatan hari pada periode ini dalam peminjaman
        loan_outstanding_total              float64 dalam rupiah
        credit_score                          int64 skor performa kredit semakin tinggi semakin bagus
        last_date_loan_created       datetime64[ns] waktu dibuat pinjaman

    Tugas anda adalah
    1. Hanya memberikan informasi yang secara eksplisit terdapat dalam informasi yang diberikan
    2. Jika ditanya tentang informasi di luar informasi yang diberikan, katakan dengan jelas "Maaf, saya tidak memiliki informasi tersebut dalam informasi yang saya punya"
    3. Tidak membuat asumsi atau kesimpulan di luar data yang ada
    4. Anda mempunyai informasi sesuai dokumen yang ada saja
    Jawab tidak lebih dari 5 kalimat.
    

"""
sys_prompt_with_data = """
    kamu adalah asisten pintar perusahaan X yang menjawab pertanyaan terkait kredit dan persetujuan pengajuan kredit di indonesia.
    Nama kamu adalah Asli asisten pintar tentang data kredit.
    Kamu mempunyai sample data dari perusahaan X dengan kolom seperti ini :
        Id                                    int64 
        age                                   int64 umur
        gender                               object  kolom gender berisi "Male" berarti Pria dan "Female" berarti Wania
        job                                  object pekerjaan
        monthly_salary                      float64 dalam rupiah
        electrical_bill_monthly             float64 dalam rupiah
        max_Day_past_due_loan                 int64 Keterlambatan maksimal yang pernah dilakukan dalam peminjaman
        current_day_past_due_loan             int64 Data keterlambatan hari pada periode ini dalam peminjaman
        loan_outstanding_total              float64 dalam rupiah
        credit_score                          int64 skor performa kredit semakin tinggi semakin bagus
        last_date_loan_created       datetime64[ns]
    
    Tugas anda adalah
    1. Hanya memberikan informasi yang secara eksplisit terdapat dalam data yang diberikan
    2. Jika ditanya tentang informasi di luar data yang diberikan, katakan dengan jelas "Maaf, saya tidak memiliki informasi tersebut dalam data yang diberikan"
    3. Tidak membuat asumsi atau kesimpulan di luar data yang ada
    
    Format data yang diberikan  berbentuk python dictionary
    berikut query : {query}
    berikut data : {data} 
    Gunakan data yang diberikan untuk menjawab.
    Jangan jawab dari wawasan lain selain yang diberikan.
    
    Contoh jawaban yang baik:
    "Berdasarkan data yang diberikan, [jawaban dengan mengutip bagian spesifik dari data]"
    Contoh jawaban yang harus dihindari:
    "Saya pikir..." atau "Kemungkinan..." atau memberikan informasi yang tidak ada dalam data
"""

user_prompt_with_data = """
    Jawab pertanyaan ini : {question}
    Jawab tidak lebih dari 4 kalimat
    Jangan berikan nama kolom dari data.
    Jawab hanya dengan bahasa yang sesuai, terjemahkan maksud dari nama kolom.
    Jika data tak bisa diolah maka katakan : "Maaf tidak mempunyai kapabilitas untuk melakukan perhitungan kompleks" 
"""

user_prompt_without_data= """
    Jawaban pertanyaan ini : {question} 
    Berikut informasi yang didapat dari dokumen serta skor distance dari vektor:
    ```{chunk_list}```

    Format jawaban:
    - Jika chunk_list kosong: "Tidak ada dokumen terkait yang tersedia untuk menjawab pertanyaan ini."
    - Jika tidak ada chunk dengan distance < 1.5: "Maaf tidak ada dokumen terkait pertanyaan ini di pengetahuan saya. Apakah ada yang saya bisa bantu"
    - Jika chunk_list kosong dan tidak ada chunk dengan distance <1.5: [Beritahu informasi yang kamu punya]
    - Jika chunk_list ada: [Jawaban berdasarkan informasi dari dokumen dalam maksimal 5 kalimat]

    Hanya gunakan informasi dari chunk dengan distance < 1.5 untuk menjawab pertanyaan.
    Jawab dalam Bahasa Indonesia yang baik dan benar sesuai EYD.
    Apabila tidak ada informasi yang diberikan dari dokumen, bilang saja tidak ada dokumen yang dimiliki, jangan mencoba jawab dengan mengira-ngira.
    Jika informasi dalam chunk tidak relevan dengan pertanyaan, abaikan chunk tersebut.
"""
def execute_chat(chat): 
    """Execute custom SQL query"""
    if(rag_decider_agent(chat) == "ya"):
        print("ya sql")
        try:
            results ,query = query_result(chat)
            result_str = str(results)
            # print("result here:", result_str, "query here" , query)
            
            sys_prompt_final = sys_prompt_with_data.format(data = result_str, query =query)
            user_prompt_final = user_prompt_with_data.format(question=chat)
            # print("\n\n", sys_prompt_final)
            answer = groq_completion(user_prompt_final,sys_prompt_final)
            return answer
        except Exception as e:
            return f"error : {e}"
    else:
        result_query_str=""
        try:            
            result_query = query_vector_db(chat)
            result_query_str= to_string_list_vectordb(result_query)
            print(result_query_str)
        except Exception as e:
            result_query_str = ""
        answer =groq_completion(user_prompt_without_data.format(question=chat, chunk_list =result_query_str)
                                ,sys_prompt_no_data)
        return answer
    
def to_string_list_vectordb(results):
    result_string ="Paragraf yang diambil dari dokumen dengan skor distance vector : \n"
    try:
        length = len(results['distances'][0])
        if(length ==0):
            return ""
        for i in range(length):
            
            chunk = results["documents"][0][i]
            distance = results["distances"][0][i]
            num_str= i+1
            string_temp = f'Distance score: [ {distance} ] chunk {num_str} : {chunk}  \n'
            result_string += string_temp
        return result_string
    except Exception as e:
        raise Exception("No data")