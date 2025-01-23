from .data_agent.query_agent import query_result
from .chat import groq_completion
from utils.query_executor import execute_query
from exception.DatabaseException import DatabaseError
from .decider import rag_decider_agent
from db.vector_db_instance import query_vector_db


sys_prompt_no_data = """
    Kamu adalah asisten pintar yang menjawab pertanyaan terkait kredit dan persetujuan pengajuan kredit di Indonesia.
    Tugas anda adalah
    1. Hanya memberikan informasi yang secara eksplisit terdapat dalam informasi yang diberikan
    2. Jika ditanya tentang informasi di luar informasi yang diberikan, katakan dengan jelas "Maaf, saya tidak memiliki informasi tersebut dalam informasi yang saya punya"
    3. Tidak membuat asumsi atau kesimpulan di luar data yang ada
    Jawab tidak lebih dari 5 kalimat.

"""
sys_prompt_with_data = """
    kamu adalah asisten pintar perusahaan X yang menjawab pertanyaan terkait kredit dan persetujuan pengajuan kredit di indonesia.
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
    - Jika chunk_list ada: [Jawaban berdasarkan informasi dari dokumen dalam maksimal 5 kalimat]

    Hanya gunakan informasi dari chunk dengan distance < 0.8 untuk menjawab pertanyaan.
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