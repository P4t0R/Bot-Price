from functions import *

#################### Menu ####################
#0.- /start      
#1.- Lista de productos --> #lista
#2.- Agregar producto   --> pegar link directamente
#3.- Editar lista --> #editar
#4.- Borrar lista -->   #borrar
#5.- Ayuda --> #ayuda
#6.- Comparar precios --> #bot
#7.- Cantidad de usuarios --> #user
#

aux_id = 0
cnt = 0
while True:

    mensaje = msj_user().lower()
    user_id = id_user()
    id = id_msj()

    if id != aux_id:
        #OP.0
        if mensaje == '/start':
            hola(user_id)

        #OP.1
        if mensaje == '#lista':
            my_list(user_id)
        if mensaje == '#lista2':
            my_list2(user_id)

        #OP.2
        if mensaje == '#agregar':
            add_url(user_id)
        if 'https://www.falabella' in mensaje:
            add_url0(user_id)
            
        #OP.3
        if mensaje == '#editar':
            add_url(user_id)

        #OP.4
        if mensaje == '#borrar':
            borrar_links(user_id)
            
        #OP.5
        if mensaje == '#ayuda':
            ayuda(user_id)

        #OP.6
        if mensaje == '#bot':
            compare()

        #OP.7
        if mensaje == '#user':
            msj = 'Cantidad de usuarios ' + str(len(lee_folder_id()))
            msj_telegram(msj, user_id)

        #print(mensaje, id_user())
        #Almacenamos Id_msj    
        aux_id = id

    #comparamos precio
    if cnt == 600:
        compare()
        cnt=0
        
    cnt+=1
    sleep(1)
