from dotenv import load_dotenv
import os
from google.cloud import bigquery

# Load environment variables
load_dotenv()

# Get project ID and credentials from environment variables
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")  # Ensure this is set in .env file
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")  # Path to service account JSON

# Check if project ID and credentials are correctly set
if not project_id:
    raise ValueError("Project ID not found. Please set GOOGLE_CLOUD_PROJECT in your .env file.")
if not credentials_path:
    raise ValueError("Credentials path not found. Please set GOOGLE_APPLICATION_CREDENTIALS in your .env file.")

# Set up BigQuery client
client = bigquery.Client(project=project_id)

# Define dataset and table information
dataset_id = 'tables'  # Replace with your BigQuery dataset ID
table_id = 'long_term_care_patients'  # Table name in BigQuery

# Function to create table in BigQuery if it doesn't exist
def create_bq_table():
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    # Define schema
    schema = [
        bigquery.SchemaField("NAME", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("CLASS", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("SECTION", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("MARKS", "INTEGER", mode="REQUIRED")
    ]

    # Create the table if it doesn't exist
    try:
        client.get_table(table_ref)  # Check if table exists
        print(f"Table {table_id} already exists in dataset {dataset_id}.")
    except Exception:
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)
        print(f"Created table {table_id} in dataset {dataset_id}.")

# Function to insert data into BigQuery table
def insert_data_to_bq():
    rows_to_insert = [
        {"patient_id": "12345a", "patient_name": "Alice Thompson", "patient_age": 78, "diagnosis": "Hypertension",
         "care_level": "Medium", "admission_date": "2023-08-15"},
        {"patient_id": "12345b", "patient_name": "Bob Johnson", "patient_age": 85, "diagnosis": "Diabetes",
         "care_level": "High", "admission_date": "2023-02-10"},
        {"patient_id": "12345c", "patient_name": "Carol White", "patient_age": 90, "diagnosis": "Alzheimer's",
         "care_level": "High", "admission_date": "2022-12-01"},
        {"patient_id": "12345d", "patient_name": "David Smith", "patient_age": 82, "diagnosis": "Arthritis",
         "care_level": "Low", "admission_date": "2021-07-20"},
        {"patient_id": "12345e", "patient_name": "Eve Black", "patient_age": 87, "diagnosis": "Parkinson's",
         "care_level": "Medium", "admission_date": "2022-11-15"},
        {"patient_id": "12345f", "patient_name": "Frank Green", "patient_age": 79, "diagnosis": "Heart Disease",
         "care_level": "High", "admission_date":  "2023-04-18"},
        {"patient_id": "12345g", "patient_name": "Grace Lee", "patient_age": 83, "diagnosis": "COPD",
         "care_level": "High", "admission_date":  "2021-09-12"},
        {"patient_id": "12345h", "patient_name": "Hank Taylor", "patient_age": 80, "diagnosis": "Stroke",
         "care_level": "Medium", "admission_date":  "2022-03-05"},
        {"patient_id": "12345i", "patient_name": "Ivy Davis", "patient_age": 86, "diagnosis": "Osteoporosis",
         "care_level": "Low", "admission_date": "2023-05-30"},
        {"patient_id": "12345j", "patient_name": "Jack Wilson", "patient_age": 92,
         "diagnosis": "Chronic Kidney Disease", "care_level": "High", "admission_date": "2020-08-19"},
        {"patient_id": "12345k", "patient_name": "Kara Adams", "patient_age": 88, "diagnosis": "Dementia",
         "care_level": "High", "admission_date":  "2021-04-11"},
        {"patient_id": "12345l", "patient_name": "Leo Miller", "patient_age": 81, "diagnosis": "Lung Cancer",
         "care_level": "High", "admission_date": "2022-07-22"},
        {"patient_id": "12345m", "patient_name": "Mona Clark", "patient_age": 84, "diagnosis": "Hypertension",
         "care_level": "Medium", "admission_date": "2023-03-14"},
        {"patient_id": "12345n", "patient_name": "Ned Moore", "patient_age": 75, "diagnosis": "Diabetes",
         "care_level": "Low", "admission_date": "2023-06-25"},
        {"patient_id": "12345o", "patient_name": "Olive Martin", "patient_age": 89, "diagnosis": "Arthritis",
         "care_level": "Medium", "admission_date": "2022-02-17"}
    ]
    # Insert rows into the table
    table_full_id = f"{project_id}.{dataset_id}.{table_id}"
    errors = client.insert_rows_json(table_full_id, rows_to_insert)
    if not errors:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: ", errors)

# Run the functions
create_bq_table()
insert_data_to_bq()
