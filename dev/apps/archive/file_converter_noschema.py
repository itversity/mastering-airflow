import os
import pandas as pd


def convert(source_base_dir, data_set_dir, target_base_dir):
    # Get column names from schemas file
    data_set_dir_path = f'{source_base_dir}/{data_set_dir}'
    file_names = os.listdir(data_set_dir_path)
    for file_name in file_names:
        # Read data from CSV
        file_path = f'{data_set_dir_path}/{file_name}'
        df = pd.read_csv(file_path, header=None)
        # Write to target in json format
        target_file_name = f'{target_base_dir}/{data_set_dir}/{file_name}.json'
        os.makedirs(f'{target_base_dir}/{data_set_dir}', exist_ok=True)
        df.to_json(target_file_name, orient='records', lines=True)


if __name__ == '__main__':
    source_base_dir = '/data/retail_db'
    data_set_dir = 'orders'
    target_base_dir = '/data/retail_db_json'
    convert(source_base_dir, data_set_dir, target_base_dir)