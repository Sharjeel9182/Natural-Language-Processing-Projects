ai-enabled-databased

Overview

The ai-enabled-databased project is a web-based application that leverages the Google Gemini Pro large language model (LLM) to interact with a BigQuery database of long-term care patients. This project enables users to query the database using natural language prompts, which are then converted into SQL queries by the AI model. The results of these queries are retrieved directly from the BigQuery table and presented to the user in a streamlined and user-friendly interface.

Key Features

Natural Language Querying: Users can input questions or prompts related to long-term care patient data stored in a BigQuery table, and the application will automatically generate the corresponding SQL query.
Seamless Integration with BigQuery: The application connects to Google BigQuery and retrieves data based on the generated SQL queries.
Web Interface: A user-friendly web application allows for easy interaction with the AI-powered query generation system.
How It Works

Data Storage in BigQuery: The long-term care patient data is stored in a Google BigQuery table. This dataset includes important patient information for analysis.
Prompt Input: Users input natural language prompts (e.g., "What is the average age of patients in long-term care?").
AI Processing: Google Gemini Pro LLM processes the prompt, translates it into a structured SQL query, and sends this query to the connected BigQuery database.
Query Execution: The SQL query is executed on the BigQuery table, and the results are returned.
Displaying Results: The application processes the returned data and displays the results in an easy-to-read format on the web interface.
Technology Stack

Google Gemini Pro: Utilized for natural language processing and SQL query generation.
Google BigQuery: Used to store and retrieve long-term care patient data.
Web Application: Built to provide a simple interface for users to interact with the AI system.
Setup & Installation

To set up and run the ai-enabled-databased project, follow these steps:

Clone the repository:
git clone https://github.com/yourusername/ai-enabled-databased.git
Install dependencies:
cd ai-enabled-databased
pip install -r requirements.txt
Configure your Google Cloud credentials to access BigQuery:
Set up your Google Cloud account and create a service account with appropriate permissions.
Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to point to your service account key file.
Run the web application:
python app.py
Open your browser and navigate to http://localhost:5000 to access the application.
Usage

Once the application is running, you can input your questions or prompts into the provided text field. The system will respond with the results generated from the BigQuery table.

For example:

Prompt: "What is the average age of patients?"
AI Generated SQL Query: SELECT AVG(age) FROM ai-enabled-database.tables.long_term_care_patients
Result: Displays the calculated average age of all patients in the database.