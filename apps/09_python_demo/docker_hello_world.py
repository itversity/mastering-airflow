import os


app_env = os.environ.get('APP_ENV')
print(f'Hello World from {app_env}')