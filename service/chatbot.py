from .data_agent.query_agent import query_result
from .chat import groq_completion
from utils.query_executor import execute_query
from exception.DatabaseException import DatabaseError
from .decider import rag_decider_agent


sys_prompt_no_data = """
    Kamu adalah asisten pintar yang menjawab pertanyaan terkait kredit dan persetujuan pengajuan kredit di Indonesia.
"""
sys_prompt_with_data = """
    kamu adalah asisten pintar perusahaan X yang menjawab pertanyaan terkait kredit dan persetujuan pengajuan kredit di indonesia.
    Kamu mempunyai sample data dari perusahaan X dengan kolom seperti ini :
        Id                                    int64
        age                                   int64
        gender                               object  kolom gender berisi "Male" dan "Female"
        job                                  object
        monthly_salary                      float64 dalam rupiah
        electrical_bill_monthly             float64 dalam rupiah
        max_Day_past_due_loan                 int64 
        current_day_past_due_loan             int64
        loan_outstanding_total              float64 dalam rupiah
        credit_score                          int64
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
        answer =groq_completion(user_prompt_with_data,sys_prompt_no_data)
        return answer