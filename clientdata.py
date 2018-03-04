import psycopg2


def _get_db_connection_string():
    dbname = '#####'
    user = '###'
    host = '#####'
    password = '####'
    port = '###'
    connection_string = "host={} port={} dbname={} user={} password={}".format(host, port, dbname, user, password)
    return connection_string

def _get_db_data(psql_string):
    connection_string = _get_db_connection_string()
    connection = psycopg2.connect(connection_string)
    cursor = connection.cursor()
    cursor.execute(psql_string)
    rows = cursor.fetchall()
    return rows




def get_dexibit_cust_info():  # Getting client id's and names from the venue table in test for now
    real_client_list_and_integrations = {'Antarctica Museum':['google_analytics', 'twitter', 'facebook','instagram'],
                        'Auckland Museum':['facebook','instagram','twitter','google_analytics','weather','presence'],
                        'Arizona Science Center':['facebook','instagram','twitter','google_analytics'],
                        'Kauri Museum':['facebook','twitter'],
                        'Rock and Roll Hall of Fame':['facebook','instagram','twitter','google_analytics'],
                        'The National Gallery of London':['facebook','instagram','twitter','google_analytics','weather','presence'],
                        'Te Papa':['facebook','twitter','google_analytics','weather'],
                        'Canadian Museum of Human Rights':['facebook','twitter','google_analytics'],
                        'Museum of the American Revolution':['facebook','twitter','google_analytics','weather','presence']
                        }
    dexibit_customers_info = {}

    sql_string = """SELECT id, name FROM venue"""
    dexibit_customers = _get_db_data(sql_string)

    for client in dexibit_customers:
        if client[1] in real_client_list_and_integrations:
            dexibit_customers_info[client[0]] = real_client_list_and_integrations[client[1]]

    #cur.mogrify("SELECT %s, %s, %s;", (dt, dt.date(), dt.time())) -> correct way to .format psql

    return dexibit_customers_info
