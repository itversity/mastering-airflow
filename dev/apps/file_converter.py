import os
import json
import pandas as pd


def get_column_names(json_schemas_file_path, data_set_dir):
    schemas = json.load(open(json_schemas_file_path))
    return [column_details['column_name'] for column_details in schemas[data_set_dir]]


def convert(json_schemas_file_path, source_base_dir, data_set_dir, target_base_dir):
    # Get column names from schemas file
    data_set_dir_path = f'{source_base_dir}/{data_set_dir}'
    print(data_set_dir_path)
    file_names = os.listdir(data_set_dir_path)
    columns = get_column_names(json_schemas_file_path, data_set_dir)
    for file_name in file_names:
        # Read data from CSV
        file_path = f'{data_set_dir_path}/{file_name}'
        df = pd.read_csv(file_path, header=None, names=columns)
        # Write to target in json format
        target_file_name = f'{target_base_dir}/{data_set_dir}/{file_name}.json'
        os.makedirs(f'{target_base_dir}/{data_set_dir}', exist_ok=True)
        df.to_json(target_file_name, orient='records', lines=True)
        print(f'Successfully converted file located at {file_path} with {df.shape[0]} records into JSON!!!')


if __name__ == '__main__':
    json_schemas_file_path = '/dev/apps/file_converter_schemas.json'
    source_base_dir = '/data/retail_db'
    data_set_dir = 'orders'
    target_base_dir = '/data/retail_db_json'
    convert(json_schemas_file_path, source_base_dir, data_set_dir, target_base_dir)