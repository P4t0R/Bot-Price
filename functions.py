#Importamos librerías
import os
import csv
import json
import requests

import os.path as path
from time import sleep

import telegram
from telegram import Bot

from bs4 import BeautifulSoup
from api import API_telegram



####################  FUNCIONES  ####################


#################### Telegram ####################

##### ID usuario
def id_user():
    url = 'https://api.telegram.org/bot' + API_telegram +'/getUpdates?offset=-1'
    response = requests.get(url).text       #Respuesta a texto
    respuesta_dict = json.loads(response)   #Respuesta a diccionario
    id_chat = respuesta_dict['result'][0]['message']['chat']['id']  #ID Chat
    return id_chat

##### ID usuario
def id_msj():
    url = 'https://api.telegram.org/bot' + API_telegram +'/getUpdates?offset=-1'
    response = requests.get(url).text       #Respuesta a texto
    respuesta_dict = json.loads(response)   #Respuesta a diccionario
    id_msj = respuesta_dict['result'][0]['message']['message_id']  #ID MSJ
    return id_msj

##### Enviar mensaje        -----
def msj_telegram(msj, user_id):
    bot = Bot(API_telegram)
    bot.send_message(text=msj, chat_id=user_id,parse_mode=telegram.ParseMode.HTML)

##### Leer Msj
def msj_user():
    url = 'https://api.telegram.org/bot' + API_telegram +'/getUpdates?offset=-1'
    response = requests.get(url).text           #Respuesta a texto
    respuesta_dict = json.loads(response)       #Respuesta a diccionario
    try:
        msj = respuesta_dict['result'][0]['message']['text']    #ID Chat
    except:
        msj = respuesta_dict['result'][0]['message']['caption'].split('\n')
        msj= msj[1] 
    #Comprobamos si msj contiene link
    if 'https://www.falabella' in msj:
        msj = msj.split('\n')
        for i in msj:
            if 'https://www.falabella' in i:
                msj=i
    return msj



#################### Menu ####################

#Saluda     -----
def hola(user_id):
    msj='Hola soy P4bot y te voy ayudar a encontrar los mejores precios, solo ten paciencia!...\nEscribe #ayuda'
    msj_telegram(msj, user_id)

#Ayuda      -----
def ayuda(user_id):
    msj='Yo te ayudo!\nSolo dime que quieres, escribiendo un comando:\n\n#lista  -> Para ver tú lista de Productos\n#borrar  -> Para eliminar todo de la lista\n# Para seguir un producto solo enviame el link.\n\n\nCuando termines de agregar todos los productos, solo espera que yo te aviso si bajan de precio.'
    msj_telegram(msj, user_id)

#Agregar link directo       -----
def add_url0(user_id):
    productos=[]
    crea_directorios(user_id)
    msj = 'Link dañado intenta nuevamente.'
    if 'https://www.falabella' in msj_user():
        msj = 'Producto Agregado!'
        productos.append(msj_user())
    #Manejo DB
    escribir_links(productos, user_id)
    #Msj Telegram
    msj_telegram(msj, user_id)

#Agregar link a lista
def add_url(user_id):
    productos=[]
    aux= 'agrega'
    cnt=0
    #Agregar link
    if msj_user().lower() == 'agrega':
        aux = msj_user().lower()
        msj_telegram('Ingresa el link del producto:', user_id)
        while True:
            #Agregamos link a lista
            if 'https://www.falabella' in msj_user():
                msj = 'Producto Agregado!'
                productos.append(msj_user())
                break
            #Cancela Operación
            if msj_user().lower() == 'no':
                msj = 'Operación Cancelada!'
                break  
            #Cancela por tiempo
            if cnt == 30:
                msj = 'Tiempo agotado / Operación cancelada'
                break
            #Advertencia 
            if msj_user().lower() != aux :
                msj='Si desea cancelar escriba <b>No</b>'
                aux = msj_user().lower()
                msj_telegram(msj, user_id)
            cnt+=1
            sleep(2)
        #Mensaje informe     
        msj_telegram(msj, user_id)
        #Manejo DB
        escribir_links(productos, user_id)



#################### Archivos ####################

##### Crea Directorios      -----
def crea_directorios(user_id):
    try:
        os.mkdir('data')
    except:
        pass
    file = 'productos_' + str(user_id) + '.txt'
    file_csv = 'data_' + str(user_id) + '.csv'
    if  not path.exists('data/' + file):
        f= open('data/' + file,'w')
    if  not path.exists('data/' + file_csv):
        f= open('data/' + file_csv,'w')

#Leer id folders
def lee_folder_id():
    ids_users=[]
    contenido = os.listdir('data')
    contenido
    for file in contenido:
        if '.txt' in file:
            id= file.split('_')[1].replace('.txt', '')
            ids_users.append(id)
    return ids_users

##### Leer BD       -----
def leer_BD(user_id):
    file = 'productos_' + str(user_id) + '.txt'
    f = open('data/' + file , 'r')
    productos = []
    for line in f:
        productos.append(line.replace('\n',''))
    f.close()
    return productos

##### Escribir BD       -----
def escribir_links(links, user_id):
    file = 'productos_' + str(user_id) + '.txt'
    f = open('data/' + file , 'a')
    for element in links:
        f.write(element + "\n")
    f.close()
    compare()

##### Leer BD       -----
def leer_links(user_id):
    file = 'productos_' + str(user_id) + '.txt'
    f = open('data/' + file, 'r')
    productos = []
    for line in f:
        productos.append(line.replace('\n',''))
    f.close()
    return productos

##### Leer CSV      -----
def leer_csv(user_id):
    file_csv = 'data_' + str(user_id) + '.csv'
    with open('data/' + file_csv, newline='') as File:  
        reader = csv.reader(File)
        for row in reader:
            print(row)

##### Borrar BD     -----
def borrar_links(user_id):
    #Borra txt
    file = 'productos_' + str(user_id) + '.txt'
    f = open('data/' + file, 'w')
    f.close()
    #Borra CSV
    file_csv = 'data_' + str(user_id) + '.csv'
    with open('data/' + file_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Producto', 'Precio', 'Nuevo Precio', 'Link'])
    msj = 'Lista Borrada!'
    msj_telegram(msj, user_id)

##### Mi lista      -----
def my_list(user_id):
    dict2={}
    lista=[]
    crea_directorios(user_id)
    file_csv = 'data_' + str(user_id) + '.csv'
    with open('data/' + file_csv) as R:
        lee = csv.reader(R.readlines()[1:])
        for line in lee:
            #Nombre,Precio,Precio Nuevo, Link
            dict2.update({line[0]:[line[1], line[2], line[3]]})
            lista.append([line[0], line[1], line[3]])
        cant_productos = len(dict2)
        msj_telegram('*'*32 + '\n<b>Tú lista contiene {} productos:</b>\n'.format(cant_productos) + '*'*32, user_id)
        for i in lista:
            producto = i[0][:30]
            precio = format(int(i[1]), ',d').replace(',', '.')
            link = i[2]
            msj = '{} <b> -->   ${}</b> \n<a href="{}">Link Producto</a>'.format(producto, precio, link)
            msj_telegram(msj, user_id)
    
##### Mi lista2      -----
def my_list2(user_id):
    dict2={}
    lista=[]
    crea_directorios(user_id)
    file_csv = 'data_' + str(user_id) + '.csv'
    with open('data/' + file_csv) as R:
        lee = csv.reader(R.readlines()[1:])
        for line in lee:
            #Nombre,Precio,Precio Nuevo, Link
            dict2.update({line[0]:[line[1], line[2], line[3]]})
            lista.append([line[0], line[1], line[2]])
        cant_productos = len(dict2)
        msj_telegram('*'*32 + '\n<b>Tú lista contiene {} productos:</b>\n'.format(cant_productos) + '*'*32, user_id)
        for i in lista:
            producto = i[0][:30]
            precio = format(int(i[1]), ',d').replace(',', '.')
            if i[2] != '':
                precio2 = format(int(i[2]), ',d').replace(',', '.')
            else:
                precio2 = precio
            link = i[2]
            msj = '{} <b> -->   ${}</b> \nPrecio anterior ${}'.format(producto, precio, precio2)
            msj_telegram(msj, user_id)



#################### WEB ####################

##### Comparacion de precios        -----
def compare():
    lista_usuarios = lee_folder_id()
    for user_id in lista_usuarios:
        dict1 = {}
        dict2 = {}
        crea_directorios(user_id)
        #Contenido HTML
        for url in leer_BD(user_id):
            html = requests.get(url)
            soup = BeautifulSoup( html.text, 'html.parser')
            try:
                producto = soup.h1.get_text()
                precio = soup.find( class_ = 'copy12' ).get_text().replace('$','').replace(' ','').replace('.','')     #class="copy12 primary high jsx-2612542277 normal
            except:
                continue
            dict1.update({producto:[precio, None, url]})
        #Leer datos de CSV
        file_csv = 'data_' + str(user_id) + '.csv'
        with open('data/' + file_csv) as R:
            lee = csv.reader(R.readlines()[1:])
            for line in lee:
                dict2.update({line[0]:[line[1], line[2], line[3]]})
        #Comparación de dict1/dict2
        if dict1 != dict2:
            for key, value in dict1.items():
                if key in dict2:
                    #Comparamos precio
                    if value[0] != dict2[key][0]:
                        precio_antiguo = dict2[key][0]
                        dict1.update({key:[value[0], precio_antiguo, value[2]]})
                        msj = f'''Alerta de Precio
                        {key} ${value[0]} {value[2]}'''
                        #Cambio el precio envia msj
                        msj_telegram(msj, user_id)
                        #dict1[key] = [value[0], precio_antiguo, value[2]]              
        #Combina todo dict2 en dict1
        dict1.update(dict2)
        #Guardar datos
        file_csv = 'data_' + str(user_id) + '.csv'
        with open('data/' + file_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Producto', 'Precio', 'Nuevo Precio', 'Link'])
            for key, value in dict1.items():
                writer.writerow([key, value[0], value[1], value[2]])
