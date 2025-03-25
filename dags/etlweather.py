from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from airflow.utils.dates import days_ago
import requests
import json

# Latitude and longitude for the desired location (London in this case)
Latitude = '27.700769'
Longitude = '85.300140'
POSTGRES_CONN_ID='postgres_default'
API_CONN_ID='api_open_meteo'

#DAG
default_args={
    'owner':'sauhar',
    'start_date':days_ago(2)
}

## DAG another style
# dag = DAG(
#     'weather_etl_pipeline',
#     default_args=default_args,
#     description='A simple Airflow tutorial DAG',  # Description of the DAG
#     schedule_interval=timedelta(days=1),  # Run once every day or '@daily' 
#     catchup=False,  # If False, Airflow won't backfill DAG runs for past dates
# )

with DAG(dag_id='weather_etl_pipeline',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dags:
    
    #define task
    @task()
    def extract_weather_data():
        """Extract weather data from Open-Meteo API using Airflow Connection."""

        # Use HTTP Hook to get connection details from Airflow connection

        http_hook=HttpHook(http_conn_id=API_CONN_ID,method='GET')

        # build the api endpoint(api site used https://open-meteo.com/)
        # https://api.open-meteo.com/v1/forecast?latitude=27.700769&longitude=-85.300140&current_weather=true
        endpoint=f'/v1/forecast?latitude={Latitude}&longitude={Longitude}&current_weather=true'

        ## Make the request via the HTTP Hook
        response=http_hook.run(endpoint)

        if response.status_code == 200:  #code is accepted
            return response.json()
        else:
            raise Exception(f"Failed to fetch weather data: {response.status_code}")
        
    @task()
    def transform_weather_data(weather_data):
        """Transform the extracted weather data."""
        current_weather = weather_data['current_weather']
        transformed_data = {
            'latitude': Latitude,
            'longitude': Longitude,
            'temperature': current_weather['temperature'],
            'windspeed': current_weather['windspeed'],
            'winddirection': current_weather['winddirection'],
            'weathercode': current_weather['weathercode']
        }
        return transformed_data
    
    @task()
    def load_weather_data(transformed_data):
        """Load transformed data into PostgreSQL."""
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            latitude FLOAT,
            longitude FLOAT,
            temperature FLOAT,
            windspeed FLOAT,
            winddirection FLOAT,
            weathercode INT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Insert transformed data into the table
        # %s represents the part of an INSERT SQL query where you are inserting values into a table. Each %s corresponds to a column in the table that will receive the provided value.
        cursor.execute("""
        INSERT INTO weather_data (latitude, longitude, temperature, windspeed, winddirection, weathercode)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            transformed_data['latitude'],
            transformed_data['longitude'],
            transformed_data['temperature'],
            transformed_data['windspeed'],
            transformed_data['winddirection'],
            transformed_data['weathercode']
        ))

        conn.commit()
        cursor.close()

    ## DAG Worflow- ETL Pipeline
    weather_data= extract_weather_data()
    transformed_data=transform_weather_data(weather_data)
    load_weather_data(transformed_data)