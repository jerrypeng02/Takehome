from flask import request, jsonify, make_response
import csv

from init import create_app
from models import db, Total_Experiments, Average_Experiments, Most_Commonly_Experimented_Compound

app = create_app()

def get_most_commonly_experimented_compound(user_experiments_table):
    compounds_file = 'data/compounds.csv'
    compounds_table = []

    with open(compounds_file) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            if row:
                compounds_table.append(row)
    csvfile.close()

    experimented_compound = {}
    compound_id_name_map = {}

    for row in compounds_table[1:]:
        compound_id = int(row[0].rstrip(','))
        compound_name = row[1].rstrip(',')
        experimented_compound[compound_id] = 0
        compound_id_name_map[compound_id] = compound_name

    for row in user_experiments_table[1:]:
        compounds_ids = row[2].rstrip(',').split(';')
        for id in compounds_ids:
            experimented_compound[int(id)] = experimented_compound[int(id)] + int(row[3])

    max_experiment_runtime = 0
    result_compound = ''

    for compound in experimented_compound:
        if experimented_compound[compound] > max_experiment_runtime:
            max_experiment_runtime = experimented_compound[compound]
            result_compound = compound_id_name_map[compound]

    return result_compound

def get_total_experiments_per_user():
    user_experiements_file = 'data/user_experiments.csv'
    users_file = 'data/users.csv'
    user_experiements_table = []
    users_table = []

    with open(users_file) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            if row:
                users_table.append(row)
    csvfile.close()

    with open(user_experiements_file) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            if row:
                user_experiements_table.append(row)
    csvfile.close()

    total_experiements = {}
    for row in users_table[1:]:
        user_id = int(row[0].rstrip(','))
        total_experiements[user_id] = 0

    for row in user_experiements_table[1:]:
        user_id = int(row[1].rstrip(','))
        total_experiements[user_id] = total_experiements[user_id] + int(row[3])

    return total_experiements, user_experiements_table

def get_average_experiments(total_experiements):
    sum = 0
    user_count = 0
    for user in total_experiements:
        user_count = user_count + 1
        sum = sum + total_experiements[user]
    average_experiments = sum / user_count

    return average_experiments
    

def etl():
    # Load CSV files
    # Process files to derive features
    # Upload processed data into a database
    total_experiements, user_experiements_table = get_total_experiments_per_user()
    result_compound = get_most_commonly_experimented_compound(user_experiements_table)
    average_experiments = get_average_experiments(total_experiements)

    total_experiements_tup = []

    for user in total_experiements:
        total_experiements_tup.append((user, total_experiements[user]))
    
    return total_experiements_tup, average_experiments, result_compound

# Your API that can be called to trigger your ETL process
@app.route('/empty', methods=['GET'])
def empty_page():
    return make_response(jsonify({'message': 'empty page'}), 200)

@app.route('/etl', methods=['POST'])
def trigger_etl():
    # Trigger your ETL process here
    body = request.get_json()
    print('Start ETL process')
    total_experiements, average_experiments, result_compound = etl()
    for experiment in total_experiements:
        db.session.add(Total_Experiments(user_id=experiment[0], number_of_experiments=experiment[1]))
        db.session.commit()
    
    db.session.add(Average_Experiments(average_experiments))
    db.session.commit()

    db.session.add(Most_Commonly_Experimented_Compound(result_compound))
    db.session.commit()

    print('End of ETL process')
    return make_response(jsonify({'message': 'successfully processed etl', 'input_json': body}), 201)