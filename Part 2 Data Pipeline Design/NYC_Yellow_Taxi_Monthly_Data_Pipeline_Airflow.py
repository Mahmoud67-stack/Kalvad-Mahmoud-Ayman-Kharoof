from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta
import pandas as pd
import pyarrow.parquet as pq
import requests
from sqlalchemy import create_engine
import logging

# PostgreSQL connection details
POSTGRES_URI = 'postgresql+psycopg2://username:password@localhost/dbname'

# Retrieve user-defined variables from Airflow's Variables feature
YEAR = Variable.get("taxi_data_year", default_var="2024")
MONTH = Variable.get("taxi_data_month", default_var="01")
MIN_FARE_AMOUNT = float(Variable.get("min_fare_amount", default_var=10))  # Default filter for fares > $10
NOTIFICATION_EMAIL = Variable.get("notification_email", default_var="mkharoof@gmail.com")

# Data file URL and name based on user inputs
DATA_URL = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{YEAR}-{MONTH}.parquet"
FILE_NAME = f"yellow_tripdata_{YEAR}-{MONTH}.parquet"

# Define helper functions

def download_data():
    """Download data file from the specified URL and save locally."""
    try:
        response = requests.get(DATA_URL, stream=True)
        if response.status_code == 200:
            with open(FILE_NAME, 'wb') as f:
                f.write(response.content)
            logging.info("File downloaded successfully.")
        else:
            raise Exception(f"Failed to download data, status code: {response.status_code}")
    except Exception as e:
        logging.error("Error during download:", exc_info=e)
        raise

def transform_data():
    """Transform data: filter trips with user-defined minimum fare, rename columns, and apply data quality checks."""
    try:
        # Load the .parquet file
        trips = pq.read_table(FILE_NAME).to_pandas()
        
        # Filter for trips with fare amounts over the user-defined minimum fare amount
        trips = trips[trips['fare_amount'] > MIN_FARE_AMOUNT]
        
        # Rename columns to align with target schema
        trips.rename(columns={
            'tpep_pickup_datetime': 'pickup_time',
            'tpep_dropoff_datetime': 'dropoff_time',
            'PULocationID': 'pickup_location',
            'DOLocationID': 'dropoff_location',
            'fare_amount': 'fare_amount'
        }, inplace=True)

        # Data Quality Checks
        trips.dropna(subset=['pickup_time', 'dropoff_time', 'fare_amount'], inplace=True)
        trips = trips[trips['pickup_time'] < trips['dropoff_time']]
        trips = trips[trips['fare_amount'] > 0]

        # Additional quality check - log the count of rows that pass and fail checks
        logging.info(f"Rows after filtering: {len(trips)}")

        # Save transformed data locally for loading
        trips.to_csv('transformed_trips.csv', index=False)
        logging.info("Transformation complete and saved to CSV.")
    except Exception as e:
        logging.error("Error during transformation:", exc_info=e)
        raise

def load_data():
    """Load the transformed data into PostgreSQL in batches."""
    try:
        engine = create_engine(POSTGRES_URI)
        chunksize = 10000  # Adjust this based on system's memory capacity

        # Read and load data in chunks
        for chunk in pd.read_csv('transformed_trips.csv', chunksize=chunksize):
            chunk.to_sql('taxi_trips', engine, if_exists='append', index=False)
            logging.info(f"Loaded chunk of {len(chunk)} rows to the database.")
        
        engine.dispose()
        logging.info("Data loading complete.")
    except Exception as e:
        logging.error("Error during data loading:", exc_info=e)
        raise

# Airflow DAG definition
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email': NOTIFICATION_EMAIL  # Email notification based on user input
}

with DAG(
    'nyc_taxi_pipeline',
    default_args=default_args,
    description='A pipeline for NYC Taxi data ETL process with user-defined inputs',
    schedule='@monthly',
    catchup=False,
) as dag:
    
    download_task = PythonOperator(
        task_id='download_data',
        python_callable=download_data
    )
    
    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data
    )
    
    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data
    )
    
    download_task >> transform_task >> load_task
