from .chat import groq_completion

def rag_decider_agent(chat):
    system_prompt = """
        Kamu adalah asisten pintar. Kamu mempunyai 2 sumber informasi yaitu dokumen dan tabel data.
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