import psycopg2

#!/usr/bin/python
from configparser import ConfigParser

def config(filename='./db/database.ini', section='postgresql'):
    """ Config the PostgreSQL conn to db """
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def connect():
    """ Connect to the PostgreSQL database server """

    try:

        conn = None

        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        return conn
		
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insertProduct(conn, product):
    """ Insert product in db """

    if conn is not None and product is not None:
        print('Database connection ok, let\'s insert a product!')

        try:
            # create a cursor
            cur = conn.cursor()
            
            #query upsert
            upsertQuery = """
                INSERT INTO product (product_id, title, ean, category_name, brand, page, images, fk_id_category) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) 
                ON CONFLICT (product_id) DO UPDATE SET 
                (title, ean, category_name, brand, page, images, fk_id_category) = (EXCLUDED.title, EXCLUDED.ean, EXCLUDED.category_name, EXCLUDED.brand, EXCLUDED.page, EXCLUDED.images, EXCLUDED.fk_id_category);
                """

            # execute an insert
            cur.execute(upsertQuery, 
            (product.product_id, product.title, product.ean, product.category_name, product.brand, product.page, product.images, product.marketplace_category_id))
        
            conn.commit()

            # close the communication with the PostgreSQL
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        

def disconnect(conn):
    """ Disconnect to the PostgreSQL db """

    if conn is not None:
        conn.close()
        print('Database connection closed.')
