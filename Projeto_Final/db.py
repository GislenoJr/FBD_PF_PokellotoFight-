import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="trabalhofinaltres",
        user="readonly_user",
        password="readonly123",
        host="localhost",
        port="5432"
    )

