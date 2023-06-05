import csv
import requests
from requests.structures import CaseInsensitiveDict

def etl():
    # Load CSV files
    # Process files to derive features
    # Upload processed data into a database
    compounds_file = 'data/compounds.csv'
    user_experiements_file = 'data/user_experiments.csv'
    users_file = 'data/users.csv'
    compounds_table = []
    user_experiements_table = []
    users_table = []
    with open(compounds_file) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            compounds_table.append(row)
    csvfile.close()
    with open(user_experiements_file) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            user_experiements_table.append(row)
    csvfile.close()
    with open(users_file) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            users_table.append(row)
    csvfile.close()
    
    total_experiements = {}
    experiemented_compound = {}

    for row in user_experiements_table[1:]:
        user_id = row[1].rstrip(',')
        if user_id not in total_experiements:
            total_experiements[user_id] = int(row[3])
        else:
            total_experiements[user_id] = total_experiements[user_id] + int(row[3])
    
    sum = 0
    user_count = 0
    for user in total_experiements:
        user_count = user_count + 1
        sum = sum + total_experiements[user]
    average_experiments = sum / user_count

    for row in user_experiements_table[1:]:
        compounds = row[2].rstrip(',').split(';')
        for compound in compounds:
            if int(compound) not in experiemented_compound:
                experiemented_compound[int(compound)] = int(row[3])
            else:
                experiemented_compound[int(compound)] = experiemented_compound[int(compound)] + int(row[3])
    max_experiment_runtime = 0
    result_compound = 0
    for compound in experiemented_compound:
        if experiemented_compound[compound] > max_experiment_runtime:
            max_experiment_runtime = experiemented_compound[compound]
            result_compound = compound
    
    return [total_experiements], average_experiments, result_compound

# Your API that can be called to trigger your ETL process
def trigger_etl():
    # Trigger your ETL process here
    [total_experiements], average_experiments, result_compound = etl()
    url = "https://reqbin.com/echo/post/json"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    data = {'total_experiements': [total_experiements], 'average_experiments': average_experiments, 'result_compound': result_compound}


    response = requests.post(url, headers=headers, data=data)
    return {"message": "ETL process started"}, response.status_code