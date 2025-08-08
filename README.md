# 🌍 Healthcare ETL & Analysis CLI

A Python-based command-line ETL pipeline to extract, transform, and load real-time COVID-19 data from public APIs.  
It stores data in a MySQL database and provides an interactive CLI to run analytical queries like daily trends and top vaccinated countries.

---

##  Features

-  Fetch COVID-19 case and vaccination data for any country
-  Filter by custom start and end date ranges
-  Store clean data into MySQL (`daily_cases` and `vaccination_data` tables)
-  Run built-in queries like:
  - Total cases
  - Daily trends
  - Top N countries by vaccinations

---

##  Tech Stack

| Component      | Purpose                                         |
|----------------|-------------------------------------------------|
| **Python**     | Core language used for building the pipeline    |
| **MySQL**      | Relational DB for storing transformed data      |
| **argparse**   | CLI interface to run ETL and query commands     |
| **requests**   | API calls to fetch live healthcare data         |
| **pandas**     | Clean, filter, and prepare tabular data         |
| **logging**    | Monitor pipeline execution and handle errors    |

---

## Project Structure

healthcare_etl_cli/
│
├── main.py # CLI entry point
├── api_client.py # API fetch logic
├── data_transformer.py # Data cleaning and transformation
├── mysql_handler.py # MySQL insert, query, and connect
├── config.ini # DB/API config
├── requirements.txt # Python dependencies
├── README.md # Project doc (this file)
│
├── sql/
│ └── create_tables.sql # DB table schema
├── docs/
│ └── architecture.png 


---

##  Setup Instructions

1. **Clone and enter the project**
    ```bash
    git clone https://github.com/your-username/healthcare-etl-cli.git
    cd healthcare-etl-cli

    python -m venv venv
    # Windows:
    venv\Scripts\activate


2. **Install dependencies**


    pip install -r requirements.txt


### 3. Configure your config.ini

[mysql]
host = localhost
user = root
password = yourpassword

database = healthcare_db

### 4. Run CLI

python main.py list_tables

### 5. CLI Usage

# Fetch and load data
python main.py fetch_data India 2023-01-01 2023-01-31
![alt text](<Screenshot 2025-08-03 165932.png>)

# Query total cases 
python main.py query_data total_cases India
![alt text](<Screenshot 2025-08-03 170125.png>)

# Query daily_trends
python main.py query_data daily_trends USA new_cases
![alt text](<Screenshot 2025-08-03 170334-1.png>)

# View all tables
python main.py list_tables
![alt text](<Screenshot 2025-08-03 165541.png>)

# Top 3 countries vaccinations report 
python main.py query_data top_n_countries_by_metric 3 total_vaccinations
![alt text](<Screenshot 2025-08-03 171228.png>)

# Drop tables (use with caution)
python main.py drop_tables

## ## Database Schema

### `daily_cases`

| Column         | Type        | Description               |
|----------------|-------------|---------------------------|
| id             | INT (PK)    | Primary key               |
| report_date    | DATE        | Date of the report        |
| country_name   | VARCHAR(255)| Name of the country       |
| total_cases    | BIGINT      | Total COVID-19 cases      |
| new_cases      | INT         | New COVID-19 cases        |
| total_deaths   | BIGINT      | Total deaths              |
| new_deaths     | INT         | New deaths                |
| etl_timestamp  | TIMESTAMP   | ETL process timestamp     |

---

### `vaccination_data`

| Column             | Type        | Description                   |
|--------------------|-------------|-------------------------------|
| id                 | INT (PK)    | Primary key                   |
| report_date        | DATE        | Date of the report            |
| country_name       | VARCHAR(255)| Name of the country           |
| total_vaccinations | BIGINT      | Total vaccination count       |
| etl_timestamp      | TIMESTAMP   | ETL process timestamp         |


## Sample query
    Fetching data for India from 2023-01-01 to 2023-01-31...
    Loaded 31 daily_cases & 31 vaccination records.

    Total COVID-19 Cases in India: 44,997,000

    Date        | New Cases
    -------------------------
    2023-01-01  | 12,300
    2023-01-02  | 14,250

    
### Future Enhancements
    Export data to CSV or Excel

    Add charts/plots for trend analysis

    Support regional/provincial data

    REST API wrapper or dashboard frontend

    Schedule daily fetch via cron job

