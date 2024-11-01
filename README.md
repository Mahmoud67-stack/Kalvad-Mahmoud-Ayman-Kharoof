# NYC Yellow Taxi Data Analysis and Pipeline Project 🚕

## Table of Contents
- [Overview](#overview)
- [Dataset](#dataset)
  - [Source Information](#source-information)
  - [Data Preparation](#data-preparation)
- [Project Structure](#project-structure)
  - [Part 1: SQL Challenge](#part-1-sql-challenge)
  - [Part 2: Data Pipeline Design](#part-2-data-pipeline-design)
  - [Part 3: Data Processing](#part-3-data-processing)
  - [Part 4: Data Visualization](#part-4-data-visualization)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup Instructions](#setup-instructions)
- [Pipeline Overview](#pipeline-overview)
  - [Pipeline Steps](#pipeline-steps)
  - [Airflow Configuration](#airflow-configuration)
- [Data Insights](#data-insights)
  - [SQL Analysis Results](#sql-analysis-results)
  - [Average Fare Analysis](#average-fare-analysis)
  - [Key Findings](#key-findings)
- [Contributors](#contributors)

## Overview
A comprehensive data pipeline and analysis project focusing on NYC Yellow Taxi data for January 2024. The project combines SQL analysis, automated data processing, and visualization to extract meaningful insights from taxi trip records.

## Dataset
### Source Information
- **Source**: NYC Yellow Taxi Trip Records (January 2024)
- **Format**: Parquet
- **Key Fields**:
  - Pickup/drop-off times
  - Trip distances
  - Fare amounts
  - Payment types

### Data Preparation
Initial data conversion from Parquet to CSV using Python:
```python
import pyarrow.parquet as pq
trips = pq.read_table('yellow_tripdata_2024-01.parquet')
trips = trips.to_pandas()
trips.to_csv('yellow_tripdata_2024-01.csv', index=False)
```

## Project Structure

### Part 1: SQL Challenge
#### Approach and Implementation

1. **Total Revenue Calculation**
   ```sql
   SELECT SUM(Total_amount) AS total_revenue
   FROM "yellow_tripdata_2024-01"
   ```
   **Result**: Total revenue for NYC Yellow taxi in January 2024 was **$79,456,384.28**

2. **Top 3 Pickup Locations**
   ```sql
   SELECT PULocationID, SUM(Total_amount) AS revenue
   FROM "yellow_tripdata_2024-01"
   GROUP BY PULocationID
   ORDER BY revenue DESC
   LIMIT 3;
   ```
   **Results**: 
   - Location 132 (likely Empire State Building)
   - Location 138 (likely Ellis Island)
   - Location 161 (likely Statue of Liberty)

3. **Frequent Riders Analysis**
   ```sql
   SELECT PULocationID, SUM(Passenger_count) AS total_passengers
   FROM "yellow_tripdata_2024-01"
   GROUP BY PULocationID
   HAVING total_passengers > 5;
   ```
   **Finding**: Analysis revealed that there were no locations with more than 5 passengers in January 2024 for NYC yellow taxis.

### Part 2: Data Pipeline Design
#### Pipeline Architecture

1. **Tools Used**:
   - Apache Airflow
   - Python Libraries:
     - Requests: For data downloads
     - Pandas & PyArrow: Data manipulation
     - SQLAlchemy: Database connectivity
     - Logging: Custom event tracking

2. **Pipeline Components**:
   #### a. Download Component
   - Checks for local file existence
   - Downloads from public URL if needed
   - Implements retry mechanism
   - Logs success/failure events

   #### b. Transform Component
   - Filters trips (fare > $10)
   - Renames columns to match schema
   - Performs quality checks:
     - Null value removal
     - Logical consistency validation
     - Date/time validation

   #### c. Load Component
   - Batch processing (10,000 rows per batch)
   - PostgreSQL integration
   - Error handling and logging
   - Resource management

3. **Error Handling**:
   - Retry mechanism: 3 attempts with 5-minute delays
   - Email notifications for failures
   - Comprehensive logging
   - Connection pool management

4. **Data Quality Measures**:
   - Input validation
   - Schema enforcement
   - Data type checking
   - Business rule validation

### Part 3: Data Processing
#### Implementation Steps

1. **Data Processing Flow**:
   - Download verification
   - PostgreSQL connection
   - Average fare calculations
   - CSV report generation

2. **Analysis Results**:
   - **Weekly Averages**:
     - Highest average fare: Monday ($19.36)
     - Lowest average fare: Saturday ($16.97)
     - Overall weekly average: $18.18
     - Standard deviation: $0.71
   
   - **Weekly Patterns**:
     - Higher fares on weekdays
     - Lower fares during weekends
     - Stable mid-week patterns

### Part 4: Data Visualization
#### Revenue Analysis
![Alt vmware](https://github.com/Mahmoud67-stack/Kalvad-Mahmoud-Ayman-Kharoof/blob/main/Part%204%20Data%20Visualization/data_visualization.png)

#### Key Observations:
1. **Daily Revenue Range**:
   - Minimum: ~$1.25 million
   - Maximum: ~$2.0 million

2. **Notable Patterns**:
   - **Peak Days**: January 3rd, 13th, 17th, 25th, 29th
   - **Low Points**: January 6th, 12th
   - **End-Month Stability**: More consistent patterns

3. **Analysis Points**:
   - Regular weekly patterns visible
   - Weekend vs. weekday variations
   - Consistent recovery after dips
   - No long-term trend identified

## Installation
### Prerequisites
- Python 3.8+
- PostgreSQL (TimescaleDB optional)
- Apache Airflow
- Python libraries (see `requirements.txt`)

### Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone https://github.com/Mahmoud67-stack/Kalvad.git
   cd <repository-folder>
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure PostgreSQL**
   - Start PostgreSQL server
   - Create database: `nyc_taxi_data`
   - Update connection details in Python script

4. **Set up Airflow**
   - Configure Airflow settings
   - Start web server

## Pipeline Overview
### Pipeline Steps
1. **Data Download**
   - Local file verification
   - Remote file retrieval
   - Error handling

2. **Data Transformation**
   - Fare filtering
   - Column standardization
   - Quality validation

3. **Database Loading**
   - Batch processing
   - Error handling
   - Performance optimization

4. **Analysis**
   - Daily calculations
   - Weekly aggregations

### Airflow Configuration
- **Retry Settings**: 3 attempts, 5-minute delays
- **Notifications**: Email alerts on failure
- **Resource Management**: Connection pooling
- **Monitoring**: Task-level logging

## Data Insights
### Key Findings
- Higher fares on weekdays
- Peak revenue: $1.25M - $2M daily
- Notable revenue spikes on specific dates
- Stable end-of-month trends
- Consistent weekly patterns

## Contributors
- Mahmoud Ayman Kharoof

---
*For more information or questions, please open an issue in the repository.*
