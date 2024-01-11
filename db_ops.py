import asyncio
import asyncpg
dbname = ""
user = ""
password = ""
host = ""
port = 5432
async def create_conn():             # Connect to postgressql database
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
async def execute_query(query, values=None):                    # Execute the Query
    try:
        conn = await create_conn()
        if conn:
            if values:
                results = await conn.fetch(query, *values)
            else:
                results = await conn.fetch(query)
            await conn.close()
            return results
    except Exception as e:
        print("Error executing query:", e)
        return None

async def delete_data_by_id(table_name, id_to_delete):           # Delete the record based on ID 
    query = f"DELETE FROM {table_name} WHERE id = $1;"
    await execute_query(query, values=(id_to_delete,))

async def insert_data(table_name, i):         # inserting data function
    query = f""" INSERT INTO {table_name} (Question, Answer)
        VALUES ($1, $2) """
    await execute_query(query,i)
async def main():            # main function 
    try:
        #user_input = int(input("Enter the ID to delete: "))
        table_name = "tree_user"  
        user_data=[('what is the capital of india','delhi'),('what is the smallest 2 digit number','10')]
        for i in user_data:
            await insert_data(table_name, i)
        print("Data inserted successfully.")
        '''await delete_data_by_id(table_name, user_input)
        print(f"Record {id_to_delete} deleted successfully.")'''
    except ValueError:
        print("Invalid input")

if __name__ == "__main__":
    asyncio.run(main())
