from google.cloud import storage, bigquery
from src.utils.config import GCPConfig
import pandas as pd
import csv
from io import StringIO

#Make sure your GOOGLE_APPLICATION_CREDENTIALS env var is set outside this script

def upload_dataframe_to_gcs(
        df:pd.DataFrame, 
        config:GCPConfig, 
        destination_blob_name:str ="stock_sentiment_csv") -> None:
    
    bucket_name = config.GCLOUD_BUCKET
   #convert df to CSV string in memory (no local file)
    csv_buffer = StringIO()
    df.to_csv(
        csv_buffer,
        index=False,
        quoting=csv.QUOTE_ALL,  # Force quotes around all fields      
        doublequote=True,       # Handle existing quotes
        escapechar=None
        )
    csv_buffer.seek(0)  #resets the pointer so it can be read from the beginning when uploading       

    
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    #upload the CSV string content
    blob.upload_from_string(csv_buffer.getvalue(), content_type="text/csv")
    
    print(f"Uploaded DataFrame to gs://{bucket_name}/{destination_blob_name}")

def load_csv_to_bigquery(config:GCPConfig, source_blob_name:str ="stock_sentiment_csv") -> int:
    dataset_id = config.BQ_DATASET
    table_id = config.BQ_TABLE
    bucket_name = config.GCLOUD_BUCKET

    client = bigquery.Client()
    table = client.dataset(dataset_id).table(table_id)

    load_file_config = bigquery.LoadJobConfig(
        source_format = bigquery.SourceFormat.CSV,
        skip_leading_rows = 1,  #skip header row
        autodetect = True,       #automatically detect schema
        allow_quoted_newlines = True,
        quote_character = '"'   #to match QUOTE ALL
    )

    uri = f"gs://{bucket_name}/{source_blob_name}"
    load_job = client.load_table_from_uri(
        source_uris=uri,
        destination=table,
        job_config=load_file_config
    )

    load_job.result()   #waits for the job to finish
    return load_job.output_rows
