import pyarrow.parquet as pq
trips = pq.read_table('yellow_tripdata_2024-01.parquet')
trips = trips.to_pandas()
# Export to CSV
trips.to_csv('yellow_tripdata_2024-01.csv', index=False)