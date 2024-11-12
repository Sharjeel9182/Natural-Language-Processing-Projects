from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from google.cloud import bigquery

# Load environment variables
load_dotenv()

# Configure GenAI Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up BigQuery client
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")  # Ensure correct key in .env
client = bigquery.Client(project=project_id)

# Define the full table address
table_address = '`ai-enabled-database.tables.long_term_care_patients`'  # Note the backticks around the full table name


# Function to load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([prompt[0], question])

        # Clean the response by stripping any extraneous text
        sql_query = response.text.strip().split('\n')[0]  # Only return the first line, which should be the query

        # Remove any occurrences of the word "SQL" or any leading/following commentary
        if sql_query.lower().startswith("sql command:"):
            sql_query = sql_query[len("SQL Command:"):].strip()

        return sql_query
    except Exception as e:
        print(f"Error generating response: {e}")
        return None


# Function to retrieve query from BigQuery database
def read_bq_query(sql):
    try:
        print(f"Executing query: {sql}")  # Print the query for debugging
        query_job = client.query(sql)
        rows = query_job.result()
        return [row for row in rows]
    except Exception as e:
        print(f"Error executing query: {e}")
        return []


# Define your prompt
prompt = [
    """

      You are an expert in converting English questions to SQL queries!
    The Bigquery table is named ai-enabled-database.tables.long_term_care_patients and has the following columns: patient_id, patient_name, patient_age, diagnosis, care_level, and admission_date.

    For example:
    1. How many records are present? 
    SELECT COUNT(*) FROM ai-enabled-database.tables.long_term_care_patients;

    2. List all patients diagnosed with Alzheimer's.
    SELECT * FROM ai-enabled-database.tables.long_term_care_patients WHERE diagnosis='Alzheimer''s';

    3. Show names and ages of patients requiring high care.
    SELECT patient_name, patient_age FROM ai-enabled-database.tables.long_term_care_patients WHERE care_level='High';

    4. How many patients are older than 80?
    SELECT COUNT(*) FROM ai-enabled-database.tables.long_term_care_patients WHERE patient_age > 80;

    5. List patients admitted after January 1, 2023.
    SELECT * FROM ai-enabled-database.tables.long_term_care_patients WHERE admission_date > DATE '2023-01-01';

    6. How many patients have diabetes as a diagnosis?
    SELECT COUNT(*) FROM ai-enabled-database.tables.long_term_care_patients WHERE diagnosis='Diabetes';

    7. Show diagnosis and care level for patients named 'Alice Thompson'.
    SELECT diagnosis, care_level FROM ai-enabled-database.tables.long_term_care_patients WHERE patient_name='Alice Thompson';

    8. List all patients sorted by admission date.
    SELECT * FROM ai-enabled-database.tables.long_term_care_patients ORDER BY admission_date DESC;

    9. Count the number of patients in each care level.
    SELECT care_level, COUNT(*) FROM ai-enabled-database.tables.long_term_care_patients GROUP BY care_level;

    10. Who was admitted most recently?
    SELECT * FROM ai-enabled-database.tables.long_term_care_patients ORDER BY admission_date DESC LIMIT 1;

    11. List names of all patients younger than 85 years old.
    SELECT patient_name FROM ai-enabled-database.tables.long_term_care_patients WHERE patient_age < 85;

    12. Give all the patient names that dignosed with Hypertension.
    SELECT patient_name FROM ai-enabled-database.tables.long_term_care_patients WHERE diagnosis = "Hypertension";

    13. Give all the patient names that dignosed with Hypertension and Lung Cancer.
    SELECT patient_name FROM ai-enabled-database.tables.long_term_care_patients WHERE diagnosis = "Lung Cancer";

    Return only the SQL query, no additional text.
    """
]

# Streamlit App
st.set_page_config(page_title="Retrieve Any SQL Query")
st.header("Gemini App to Retrieve SQL Data")

# Streamlit UI
question = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

# If submit is clicked
if submit:
    response_sql = get_gemini_response(question, prompt)

    if response_sql:
        # Check if the response is not empty or malformed
        if not response_sql or len(response_sql.split()) < 2:
            st.error("The generated SQL query is empty or malformed. Please try asking the question differently.")
        else:
            st.subheader("Generated SQL Query:")
            st.code(response_sql, language='sql')

            # Handle possible issues with query syntax (ensure it ends with a semicolon)
            if not response_sql.strip().endswith(";"):
                response_sql += " ;"

            # Ensure the query doesn't return too many rows by addi

            # Ensure the query is valid before execution
            response_rows = read_bq_query(response_sql)

            if response_rows:
                st.subheader("The Response is:")
                for row in response_rows:
                    st.write(dict(row))  # Display results in a clean dictionary format
            else:
                st.error("No data returned or error in the query execution.")
    else:
        st.error("Error generating SQL query.")
