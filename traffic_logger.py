import os
import csv
import requests
from datetime import datetime, timedelta

# Natažení proměnných z prostředí GitHub Actions
token = os.environ.get('TRAFFIC_TOKEN')
repo = os.environ.get('GITHUB_REPOSITORY')
headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}

def get_yesterdays_data(endpoint):
    url = f'https://api.github.com/repos/{repo}/traffic/{endpoint}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data_list = response.json().get(endpoint, [])
    # Pokud jsou data dostupná, vezmeme předposlední záznam (včerejšek je už uzavřený)
    if len(data_list) > 1:
        return data_list[-2]
    elif len(data_list) == 1:
        return data_list[0]
    
    # Kdyby byla data prázdná
    return {'timestamp': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%dT00:00:00Z'), 'count': 0, 'uniques': 0}

# Stažení dat
views = get_yesterdays_data('views')
clones = get_yesterdays_data('clones')
date_str = views['timestamp'][:10]

file_path = 'traffic_data.csv'
is_new_file = not os.path.exists(file_path)

# Zápis do CSV
with open(file_path, 'a', newline='') as f:
    writer = csv.writer(f)
    if is_new_file:
        writer.writerow(['Date', 'Views', 'Unique_Views', 'Clones', 'Unique_Clones'])
    writer.writerow([date_str, views['count'], views['uniques'], clones['count'], clones['uniques']])
