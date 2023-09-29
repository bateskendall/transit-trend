import psycopg2
import pandas as pd
import os
import time
from config import db_params, gtfs_path

def load_data_to_db(db_params, gtfs_path):
    try:
        # Connect to the PostgreSQL database using psycopg2
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Loop through each text file in the GTFS dataset
        for file_name in os.listdir(gtfs_path):
            if file_name.endswith(".txt"):
                # Record start time for performance monitoring
                start_time = time.time()

                # Define the table name based on the file name (remove .txt extension)
                table_name = file_name.replace(".txt", "")
                
                # Load the text file into a pandas DataFrame
                file_path = os.path.join(gtfs_path, file_name)
                df = pd.read_csv(file_path)

                # Define the SQL table schema based on the DataFrame dtypes
                schema = ", ".join([f"{col} TEXT" for col in df.columns])
                create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema});"

                # Execute the CREATE TABLE query
                cursor.execute(create_table_query)

                # Prepare COPY statement
                copy_stmt = f"COPY {table_name} FROM STDIN WITH CSV HEADER DELIMITER as ','"
                
                # Use the 'copy_expert' function to load data
                with open(file_path, 'r') as f:
                    cursor.copy_expert(copy_stmt, f)

                # Commit the transaction
                connection.commit()

                # Record end time and calculate elapsed time
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Finished processing {file_name} and loaded data to {table_name} in {elapsed_time:.2f} seconds.")

    except Exception as error:
        print(f"Error: {error}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

# Call the function to load data to DB
load_data_to_db(db_params, gtfs_path)