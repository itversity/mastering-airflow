import os
import pandas as pd


source_base_dir = '/data/retail_db'
data_set_dir = 'orders'
target_base_dir = '/data/retail_db'
target_data_set_dir = 'orders_by_date'

os.makedirs(f'{target_base_dir}/{target_data_set_dir}', exist_ok=True)

data_set_dir_path = f'{source_base_dir}/{data_set_dir}'
for file_name in os.listdir(data_set_dir_path):
    df = pd.read_csv(
        f'{data_set_dir_path}/{file_name}',
        names=['order_id', 'order_date', 'order_customer_id', 'order_status']
    )
    df_grouped = df.groupby('order_date')

    for file_name, data_to_be_saved in map(lambda dfg: (dfg[0], dfg[1]), df_grouped):
        data_to_be_saved.to_csv(
            f'{target_base_dir}/{target_data_set_dir}/part-{file_name[:10]}',
            header=None,
            index=False
        )
        print(f'Data for date {file_name} is successfully saved')
