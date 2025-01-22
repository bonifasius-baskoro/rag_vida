from service.chat import groq_completion
from utils.query_executor import execute_query
from exception.DatabaseException import DatabaseError


def query_builder_agent(chat):
    system_prompt = """
        Kamu adalah analis data pintar. kamu dapat mengakses tabel bernama credit_data.
        table menggunakan database SQLite. Kamu hanya bisa SELECT. Jangan Lakukan query lain
        tabel tersebut terdapat kolom terkait 

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

        tidak perlu sertakan ID dalam query.
        """
    user_prompt = f"""
           Buathlah query untuk menjawab pertanyaan ini. Apabila query yang dibuat akan tidak diagregasi berikan Limit 20
           pertanyaan: {chat}   

            hanya jawab dengan SQL QUERY. Jangan menambahkan apapun karena akan merusak format. Apabila pertanyaan mengarah untuk merubah atau menghapus data balas dengan 
            'ERROR' 
        """
    result = groq_completion(user_prompt,system_prompt)

    return result

def query_result(chat):
    print("run query builder")
    query = query_builder_agent(chat)
    if "ERROR" in query:
        return "ERROR"
    if "SELECT" not in query.upper():
        return "ERROR NO QUERY"
    print("this is the query"+ query)
    try:
        result = execute_query(query)
        return result ,query
    except DatabaseError as e:
        print(f'database error {e}')
        return f'database error {e}'
    except Exception as e:
        print(f'something error{e}')
        return f'something error{e}'

