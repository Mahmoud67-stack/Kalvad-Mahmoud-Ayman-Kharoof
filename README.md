# NYC Yellow Taxi Data Analysis and Pipeline Project 🚕

## Table of Contents
- [Overview](#overview)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
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
- [Results](#results)
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

## Project Structure
### Components
1. **SQL Challenges**: Complex queries for data analysis
2. **Data Pipeline Design**: Automated ETL processes
3. **Data Processing**: Python-based transformations
4. **Data Visualization**: Insights presentation

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
   - Checks for local .parquet file
   - Downloads from public URL if needed

2. **Data Transformation**
   - Filters trips (fare > $10)
   - Column renaming
   - Quality checks
   - Null value handling

3. **Database Loading**
   - Batch processing for PostgreSQL
   - Efficient large file handling

4. **Analysis**
   - Daily average fare calculations
   - Weekly patterns analysis

5. **Visualization**
   - Time series revenue charts
   - Trend analysis

### Airflow Configuration
- **Retry Settings**: 3 attempts, 5-minute delays
- **Notifications**: Email alerts on failure

## Data Insights
### SQL Analysis Results
- **Revenue Metrics**: 30-day total revenue analysis
- **Top Locations**: Identified 3 highest-revenue pickup points
- **Customer Patterns**: Analysis of frequent riders (5+ trips/month)

### Average Fare Analysis
| Day      | Average Fare |
|----------|-------------|
| Monday   | $19.36      |
| Saturday | $16.97      |

### Key Findings
- Higher fares on weekdays
- Peak revenue: $1.25M - $2M daily
- Notable revenue spikes: Jan 3rd, 13th, 17th, 25th
- Stable end-of-month trends

## Results
The project successfully:
- Automated data pipeline with Airflow
- Delivered detailed SQL-based insights
- Created comprehensive revenue visualizations
- Established efficient large dataset management

## Contributors
- Mahmoud Ayman Kharoof

---
*For more information or questions, please open an issue in the repository.*
