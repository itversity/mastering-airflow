import subprocess
import os
import sys

airflow_home = sys.argv[1]
os.environ.setdefault('AIRFLOW_HOME', airflow_home)


processes = subprocess. \
  check_output('ps -ef|grep airflow|grep -v grep|grep -v restart', shell=True). \
  decode('utf-8'). \
  splitlines()

process_ids = map(lambda process: process.split()[1], processes)
process_ids_str = ' '.join(process_ids)


subprocess.check_call(f'kill -9 {process_ids_str}', shell=True)
subprocess.check_call(f'rm -rf {airflow_home}/*.pid', shell=True)
subprocess.check_call(f'airflow webserver -p 8080 -D', shell=True)
subprocess.check_call(f'airflow scheduler -D', shell=True)
