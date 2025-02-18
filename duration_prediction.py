from prefect import flow, task
import requests
import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge, Lasso, LinearRegression
from sklearn.metrics import root_mean_squared_error

@task(name='data load', log_prints=True)
def load_data():
    files = [('green_tripdata_2024-10.parquet', './data'), 
         ('green_tripdata_2024-11.parquet', './data')]

    print("Downloading started:...")

    for file, path in files:
        url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{file}"
        save_path = f"{path}/{file}"
        response = requests.get(url, stream=True)

        with open(save_path, "wb") as handle:
            for data in response.iter_content(chunk_size=1024):
                handle.write(data)


@task(name='data transform', log_prints=True)
def transform_data():
    # print(f'transformed: {path}')
    train_data = pd.read_parquet("data/green_tripdata_2024-10.parquet")
    test_data = pd.read_parquet("data/green_tripdata_2024-11.parquet")
    return train_data, test_data

def load_transform_data(path):
   print(path)

def train_test_split(path):
   print(path)

def dataset_visualization(dataframe):
    pass

def train_model(dataframe):
    pass

@task(name='model load', log_prints=True)
def load_model(model):
    print(f'load model {model}')

@task(name='model validation', log_prints=True)
def validate_model(preds, actual):
    print(f'validation for {preds}, {actual}')

@task(name='predictions generation', log_prints=True)
def generate_predictions(model, dataframe):
    print(f'generate predictions {model}, {dataframe}')

@flow(name='taxi ride duration prediction')
def the_flow():
    load_data()
    # load_data('test_data')
    train_data, test_data = transform_data()
    # transform_data('test_data')
    load_model('best_model')
    generate_predictions('model', 'train_data')
    generate_predictions('model', 'test_data')
    validate_model('preds_train', 'y_train')
    validate_model('preds_test', 'y_test')

if __name__ == '__main__':
    the_flow()

    
    
    
    
    