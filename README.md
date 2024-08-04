# reddit_api_etl
Reddit data pull using API and then schedule based on airflow and docker

![Alt text](<Architecture Diagram.png>)

# 1. Reddit API:

- Source of the data.
- Data is pulled using HTTP requests.

# 2. Python ETL Script:

- Handles Extraction, Transformation, and Loading (ETL) processes.
- Extracts data from the Reddit API.
- Transforms the data (e.g., cleaning, filtering, aggregation).
- Loads the transformed data into an AWS S3 bucket.

# 3. Docker Container:

- Encapsulates the Python ETL script.
- Ensures consistency and reproducibility across different environments.
- Facilitates easy deployment and management.

# 4. Airflow Scheduler:

- Orchestrates the ETL process.
- Schedules and manages the execution of the Docker container running the ETL script.
- Monitors the ETL workflow and handles retries and failures.

# 5. AWS S3 Bucket:

- Stores the processed data.
- Provides scalable and durable storage.
