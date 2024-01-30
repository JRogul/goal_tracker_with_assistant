import psycopg2
import json

def connect_to_database():
    with open("src\database.json", 'r') as file:
        config = json.load(file)
    user = config['user']
    password = config['password']
    host = config['host']
    port = config['port']
    database = config['database']
    connection = psycopg2.connect(user=user, password=password,
                              host=host, port=port,
                              database=database)
    return connection

def select_task_from_database(ID_task):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM public."Tasks" WHERE id = %s''', (ID_task,))
    data = cursor.fetchall()
    connection.close()
    return data

def insert_task_to_database(ID_task, title, description, start_date, end_date, created_at):
    connection = connect_to_database()
    ID_task = get_number_of_tasks_from_database()
    cursor = connection.cursor()

    cursor.execute('''INSERT INTO public."Tasks" (id, task, description, start_date, end_date, created_at) 
                   VALUES (%s, %s, %s, %s, %s, %s)''', 
                    (ID_task, title, description, start_date, end_date, created_at))
    connection.commit()
    connection.close()

    return ID_task

def delete_task_from_database(id_TASK):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute('''DELETE FROM public."Tasks" WHERE id = %s''', (id_TASK,))
    connection.commit()
    connection.close()

def get_task_list_from_database():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM public."Tasks"''')
    data = cursor.fetchall()
    connection.close()
    return data


def get_number_of_tasks_from_database():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute('''SELECT COUNT(*) FROM public."Tasks"''')
    row = cursor.fetchall()
    connection.commit()
    connection.close()
    return row[0][0]