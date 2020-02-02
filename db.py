# -*- coding: utf-8 -*-
# EASY-GYM - Sistema de gestión de clientes para gimnasio
# version 1.0
# Desarrollador - Claudio Herrera
# Empresa - Procyon
# Septiembre 2019

import pymysql

DB_HOST = 'localhost' 
DB_USER = 'root' 
DB_PASS = '' 
DB_NAME = 'gym'

def Run_query(query=''): 
    datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME]

    conn = pymysql.connect(*datos) # Conectar a la base de datos 
    cursor = conn.cursor()         # Crear un cursor 
    cursor.execute(query)          # Ejecutar una consulta 

    if query.upper().startswith('SELECT'): 
        data = cursor.fetchall()   # Traer los resultados de un select si la query arranca con SELECT
    else: 
        conn.commit()              # Hacer efectiva la escritura de datos 
        data = None 
    
    cursor.close()                 # Cerrar el cursor 
    conn.close()                   # Cerrar la conexión 
    return data

