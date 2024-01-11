 import asyncio
import asyncpg
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
    
        async with connection.transaction():
            user_question = 'what is the smallest 2 digit num'
            results = await connection.fetch('SELECT * FROM find_answer($1)', user_question)
            print("Results:", results)
            
    except Exception as e:
        print("Unable to connect to the database:", e)
    finally:
        await connection.close()
asyncio.run(create_conn())
