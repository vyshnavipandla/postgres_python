import asyncio
import asyncpg
from fuzzywuzzy import fuzz
dbname = ""
user = ""
password = ""
host = ""
port = 5432
async def create_conn():
    try:
        connection = await asyncpg.connect(
            user=user,
            password=password,
            database=dbname,
            host=host,
            port=port
        )
        return connection
    except Exception as e:
        print("Unable to connect to the database:", e)
        return None
async def execute_query(query, values=None):
    try:
        conn = await create_conn()
        if conn:
            if values is None:
                results = await conn.fetch(query)
                #print(f"results are...{results}")
            else:
                results = await conn.fetch(query, *values)
            await conn.close()
            return results
    except Exception as e:
        print("Error executing query:", e)
        return None
async def main():
    user_question = input("Enter your question: ")
    query_all_questions = "SELECT Question FROM Tree_User;"
    all_questions = await execute_query(query_all_questions, values=None)
    if all_questions is not None:
        max_ratio = 0
        best_match = None
        for db_question in all_questions:
            ratio = fuzz.partial_ratio(user_question.lower(), db_question['question'].lower())
            #print(f"comparing ratio...{ratio}") 
            if ratio > max_ratio:
                max_ratio = ratio
                #print(f"maximum ratio is .....{max_ratio}")
                best_match = db_question['question']
                #print(best_match)
        if max_ratio > 80:  
            query_answer = "SELECT answer FROM Tree_User WHERE question = $1;"
            value_answer = (best_match,)
            results = await execute_query(query_answer, values=value_answer)
            for i in results:
                print("Answer:", i['answer'])
        else:
            print("No sufficiently similar question found in the database.")
    else:
        print("Error fetching questions from the database.")

if __name__ == "__main__":
    asyncio.run(main())
