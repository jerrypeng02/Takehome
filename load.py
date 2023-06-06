import psycopg2

def create_tables_load_data(data):
    commands = (
        """
        CREATE TABLE total_experiments (
            user_id INTEGER NOT NULL,
            number_of_experiements INTEGER NOT NULL
        )
        """,
        """ 
        CREATE TABLE average_experiments (
            average_experiments FLOAT4 NOT NULL
        )
        """,
        """
        CREATE TABLE most_commonly_compound (
            most_commonly_compound VARCHAR(255) NOT NULL
        )
        """
    )

    conn = None
    try:
        print('Connecting database.')
        conn = psycopg2.connect(host="localhost",
                                database="takehomedb",
                                user="user",
                                password="")
        cursor = conn.cursor()

        for command in commands:
            cursor.execute(command)

        total_experiments_sql = "INSERT INTO total_experiments VALUES(%s, %s)"
        average_experiments_sql = "INSERT INTO average_experiments VALUES(%s)"
        most_commonly_compound_sql = "INSERT INTO most_commonly_compound VALUES(%s)"
        total_experiment_list = data[0]
        average_experiments = data[1]
        most_commonly_compound = data[2]

        cursor.executemany(total_experiments_sql, total_experiment_list)
        cursor.execute(average_experiments_sql, (average_experiments, ))
        cursor.execute(most_commonly_compound_sql, (most_commonly_compound, ))

        conn.commit()

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
