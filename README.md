# End-to-End ETL Pipeline with Apache Airflow and Astro

## Project Overview

This project demonstrates how to build an **End-to-End ETL (Extract, Transform, Load) Pipeline** using **Apache Airflow** and **Astronomer Astro**. The pipeline automates data extraction, transformation, and loading processes, making data workflows efficient and scalable.

## Features

- **Automated Workflow Orchestration** with Apache Airflow
- **Integration with Astronomer Astro** for deployment and execution
- **Modular ETL Process** (Extract, Transform, Load)
- **Error Handling and Logging** for robust execution
- **Scalability** to accommodate growing data pipelines

## Technologies Used

- **Apache Airflow** (Orchestration)
- **Astronomer Astro** (Airflow deployment & management)
- **Python** (ETL scripting)
- **PostgreSQL / Any Database** (Data Storage)
- **Docker** (Containerization)
- **Cloud Storage (Optional)** (For scalability)

## Installation and Setup

### Prerequisites

Ensure you have the following installed on your system:

- Python (>=3.8)
- Docker
- Astronomer CLI
- PostgreSQL (or any supported database)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd apache-airflow-etl
```

### Step 2: Install Dependencies

Create a virtual environment and install required packages:

```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows
pip install -r requirements.txt
```

### Step 3: Start Airflow with Astro

Initialize and start an Astro project(https://www.astronomer.io/docs/astro/cli/overview):

```bash
astro dev init  # Initialize Astro project
astro dev start  # Start Airflow locally
```

### Step 4: Set Up Database Connection

Modify the `airflow.cfg` file or set environment variables to configure your database connection:

```bash
export AIRFLOW_CONN_DATABASE_URL='postgresql://user:password@localhost:5432/mydatabase'
```

### Step 5: Deploy the DAGs

Place your DAG files inside the `dags/` directory. Restart Airflow to recognize new DAGs:

```bash
astro dev restart
```

## Usage

1. **Access Airflow UI**: Open [http://localhost:8080](http://localhost:8080) and log in with default credentials (`airflow` / `airflow`).
2. **Enable DAG**: Navigate to the DAGs section and enable the ETL pipeline.
3. **Trigger DAG**: Click "Trigger DAG" to start the ETL process.
4. **Monitor Execution**: Check logs and execution status from the UI.

## Project Structure

```
├── dags/
│   ├── etl_pipeline.py  # Main DAG script
│   ├── extract.py  # Data extraction logic
│   ├── transform.py  # Data transformation logic
│   ├── load.py  # Data loading logic
├── plugins/
├── Dockerfile
├── requirements.txt
├── airflow.cfg
└── README.md
```

## DAG Workflow

1. **Extract**: Fetch data from an external source (API, database, etc.).
2. **Transform**: Clean, filter, and process data.
3. **Load**: Store the transformed data into a database or cloud storage.

