import pyarrow.parquet as pq
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the .parquet file
data = pq.read_table('yellow_tripdata_2024-01.parquet').to_pandas()

# Convert the pickup datetime column and filter for dates in January 2024 only
data['tpep_pickup_datetime'] = pd.to_datetime(data['tpep_pickup_datetime'])
data = data[(data['tpep_pickup_datetime'].dt.year == 2024) & (data['tpep_pickup_datetime'].dt.month == 1)]

# Set the Seaborn style for better visuals
sns.set_theme(style="whitegrid")

# Prepare data for the visualization
# Group by date and calculate total revenue in millions
data['date'] = data['tpep_pickup_datetime'].dt.date
revenue_per_day = data.groupby('date')['fare_amount'].sum() / 1_000_000  # Convert to millions

# Create a single large plot for Total Revenue Per Day
plt.figure(figsize=(15, 8))  # Increased figure size for better visibility
sns.lineplot(x=revenue_per_day.index, y=revenue_per_day.values, marker='o', color="royalblue")
plt.title('Total Revenue Per Day (January 2024)', fontsize=20)
plt.xlabel('Date', fontsize=16)
plt.ylabel('Total Revenue (Millions $)', fontsize=16)  # Updated label
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.ylim(0, revenue_per_day.max() * 1.1)  # Adjust y-axis limit for padding

# Save and show the figure
plt.tight_layout()
plt.savefig('data_visualization.png')
plt.show()
