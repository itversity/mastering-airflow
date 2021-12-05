import os
import glob
import pandas as pd


def get_file_paths(source_base_dir, data_set_dir):
    file_paths = glob.glob(f'{source_base_dir}/{data_set_dir}/*')
    return sorted(file_paths)[:3]


def convert(source_file_paths, target_base_dir, data_set_dir):
    processed_files = []
    for source_file_path in source_file_paths:
        df = pd.read_csv(
            source_file_path,
            names=['order_id', 'order_date', 'order_customer_id', 'order_status']
        )
        os.makedirs(f'{target_base_dir}/{data_set_dir}', exist_ok=True)
        target_file_path = f'{target_base_dir}/{data_set_dir}/{source_file_path.split("/")[-1]}'
        df.to_json(target_file_path, lines=True, orient='records')
        processed_files.append({'source_file_path': source_file_path, 'record_count': df.shape[0]})
        print(f'Successfully converted file at {source_file_path} with record count {df.shape[0]} to json')
    return processed_files


def archive(source_file_paths):
    for source_file_path in source_file_paths:
        os.remove(source_file_path)


if __name__ == '__main__':
    source_base_dir = '/Users/itversity/Projects/Internal/bootcamp/itversity-material/mastering-airflow/airflow-docker/data/retail_db'
    data_set_dir = 'orders_by_date'
    target_base_dir = '/Users/itversity/Projects/Internal/bootcamp/itversity-material/mastering-airflow/airflow-docker/data/retail_db_json'
    file_paths = get_file_paths(source_base_dir, data_set_dir)
    processed_files = convert(file_paths, target_base_dir, data_set_dir)
    archive(file_paths)
