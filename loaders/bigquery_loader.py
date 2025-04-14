from google.cloud import bigquery
import pandas as pd
import os
import logging

def load_df_to_bigquery(client: bigquery.Client, df: pd.DataFrame, table_id: str):
    project_name = os.getenv("BIGQUERY_PROJECT_NAME")
    dataset = os.getenv("BIGQUERY_DATASET")
    table_route = '.'.join((project_name, dataset, table_id))

    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
    job = client.load_table_from_dataframe(df, table_route, job_config=job_config)

    job.result()
    logging.info("Dataframe subido a {0} exitosamente.".format(table_route))
