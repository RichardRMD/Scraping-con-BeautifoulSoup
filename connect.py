import sqlite3
from sqlite3 import Error

def sql_connection():

    try:

        con = sqlite3.connect('upload_data.db',timeout=20)
        return con

    except Error:

        print(Error)

con = sql_connection()
cursorObj = con.cursor()
#cursorObj.execute("SELECT titulo FROM noticias ")
cursorObj.execute("CREATE TABLE if not exists Noticias(id integer PRIMARY KEY, titulo text, breve_descripcion text, fecha_hora text, seccion text, tipo text)")
#rows = cursorObj.fetchall()
con.commit()
