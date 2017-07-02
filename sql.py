import os
import psycopg2
import urllib


def query(sql, parameters, fetch):
    """Establish connection and run SQL statement."""
    connection = None
    try:
        urllib.parse.uses_netloc.append('postgres')
        url = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))
        connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

    except psycopg2.OperationalError as oe:
        print("Could NOT connect to database.")
        print(oe)

    else:
        connection.autocommit = True
        with connection.cursor() as cursor:
            result = run_statement(sql, parameters, fetch, cursor)
        if result:
            return result

    finally:
        if connection:
            connection.close()


def run_statement(sql, parameters, fetch, cursor):
    """Run an SQL statement."""
    if parameters:
        cursor.execute(sql, parameters)
    else:
        cursor.execute(sql)

    result = None
    if fetch == "all":
        result = cursor.fetchall()
    elif fetch == "one":
        result = cursor.fetchone()
    elif fetch == "col":
        result = tuple(row[0] for row in cursor)
    elif fetch == "cell":
        result = cursor.fetchone()[0]

    if result:
        return result
