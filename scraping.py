from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import sqlite3
from connect import sql_connection

con = sql_connection()
cursorObj = con.cursor()
def Create_Table():
    cursorObj.execute("CREATE TABLE if not exists Noticias(id integer PRIMARY KEY, titulo text, breve_descripcion text, fecha_hora text, seccion text, tipo text)")

Create_Table()

def Insert_values(data,con):
    cursorObj.execute("""INSERT INTO Noticias (id,titulo,breve_descripcion,fecha_hora,seccion,tipo) VALUES(?,?,?,?,?,?)""",data)
    con.commit()

def verificar_siExiste(titulo):
    cursorObj.execute("SELECT titulo FROM Noticias")
    rows = cursorObj.fetchall()
    for row in rows:
        if row[0] == titulo:
            return True
    return False


url="https://www.cnnchile.com/tag/emprendimiento/"
page=requests.get(url)
soup=BeautifulSoup(page.content,features="html.parser")

cursorObj.execute("SELECT max(id) FROM Noticias")
row = cursorObj.fetchone()[0]
if row == None:
    ide=0
else:
    ide = row + 1

cont=1
rep = 0
while cont <= 2:
    
    containers = soup.find_all('div',class_='inner-item__content')
    for contain in containers:  

            link = contain.find('h2', class_='inner-item__title').a.get('href')
            page_news = requests.get(link)
            soup_news = BeautifulSoup(page_news.content,features="html.parser")
            time.sleep(0.5)  
            titulo = soup_news.find('h1', class_='main-single-header__title').text
            if verificar_siExiste(titulo) == True:
                rep +=1
                
            else:
                descripcion = soup_news.find('div', class_='main-single-header__excerpt').find('p').text[19:]
                fecha_hora = soup_news.find('span',class_='main-single-about__item main-single__date').text
                seccion = soup_news.find('a',class_='main-single-about__item main-single__button u-uppercase main-single__button--primary js-single-button-cat').text
                tipo = soup_news.find('a',class_='main-single-about__item main-single__button u-uppercase main-single__button--secondary js-single-button-tag').text
                
                data = (ide,titulo,descripcion,fecha_hora,seccion,tipo)
                Insert_values(data,con)
                ide+=1
        
    tag = soup.find_all('a', class_='new-pagination__button new-pagination__button--secondary')[1].get('href')
    page=requests.get(tag)
    soup=BeautifulSoup(page.content,features="html.parser")
    time.sleep(0.5)
    cont+=1

if rep > 0:
    print("",rep,"Noticias analizadas por el scraping, ya existe en la base de datos!")
con.close()
#df = pd.DataFrame(data, columns=['Titulo','Descripcion','Fecha','Seccion','Tipo'])
#df.to_csv('drive/My Drive/Scraping/Noticias.csv')
