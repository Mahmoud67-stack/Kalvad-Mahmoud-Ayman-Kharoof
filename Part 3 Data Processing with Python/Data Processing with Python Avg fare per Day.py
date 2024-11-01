import os
import requests
import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine
import datetime

# Configuration
YEAR = "2024"       # Set the year
MONTH = "01"        # Set the month
FILE_NAME = f"yellow_tripdata_{YEAR}-{MONTH}.parquet"
DATA_URL = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{FILE_NAME}"

# PostgreSQL connection details
DB_NAME = "postgres"          # Database name
DB_USER = "postgres"          # Username
DB_PASSWORD = "ROOT"          # Password
DB_HOST = "localhost"         # Server host
DB_PORT = "5432"              # Port
TABLE_NAME = "nyc_taxi_trips"

# 1. Download the specified month's dataset if it is not already available locally
def download_data():
    if not os.path.exists(FILE_NAME):
        print(f"Downloading {FILE_NAME}...")
        response = requests.get(DATA_URL, stream=True)
        if response.status_code == 200:
            with open(FILE_NAME, 'wb') as f:
                f.write(response.content)
            print("Download complete.")
        else:
            raise Exception(f"Failed to download data: {response.status_code}")
    else:
        print(f"{FILE_NAME} already exists locally.")

# 2. Connect to PostgreSQL database and load the data
def load_data_to_db():
    print("Loading data into PostgreSQL...")
    # Establish a database connection
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    # Read the data from the parquet file
    trips = pq.read_table(FILE_NAME).to_pandas()
    
    # Write the DataFrame to PostgreSQL
    trips.to_sql(TABLE_NAME, engine, if_exists='replace', index=False)
    print("Data loaded into PostgreSQL.")

# 3. Calculate the average fare per day of the week for the specified month
def calculate_average_fare():
    print("Calculating average fare per day of the week...")
    # Establish a database connection
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    # Query to calculate the average fare per day of the week
    query = f"""
        SELECT
            EXTRACT(DOW FROM tpep_pickup_datetime) AS day_of_week,
            AVG(fare_amount) AS avg_fare
        FROM {TABLE_NAME}
        WHERE EXTRACT(YEAR FROM tpep_pickup_datetime) = {YEAR}
          AND EXTRACT(MONTH FROM tpep_pickup_datetime) = {MONTH}
        GROUP BY day_of_week
        ORDER BY day_of_week;
    """
    avg_fare_per_day = pd.read_sql_query(query, engine)

    # Map day of the week to weekday names
    avg_fare_per_day['day_of_week'] = avg_fare_per_day['day_of_week'].map({
        0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
        4: 'Thursday', 5: 'Friday', 6: 'Saturday'
    })

    # Close the engine connection
    engine.dispose()
    print("Average fare calculation complete.")
    return avg_fare_per_day

# 4. Generate a summary report and save it as a CSV file
def save_to_csv(dataframe):
    output_file = "average_fare_per_day.csv"
    dataframe.to_csv(output_file, index=False)
    print(f"Report saved as {output_file}.")

# Run the entire workflow
if __name__ == "__main__":
    try:
        # Step 1: Download data if not already present
        download_data()

        # Step 2: Load data into PostgreSQL
        load_data_to_db()

        # Step 3: Calculate the average fare per day of the week
        avg_fare_per_day = calculate_average_fare()

        # Step 4: Save the results to a CSV file
        save_to_csv(avg_fare_per_day)

    except Exception as e:
        print(f"Error: {e}")
