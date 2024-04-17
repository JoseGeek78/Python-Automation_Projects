from pytube import YouTube
import pandas as pd
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

#Variables excel
file_path = 'enlaces_videos/enlaces.xlsx'
sheet_name = 'Hoja1'
column_name = 'Videos'

#Credenciales google drive
directorio_credenciales = 'credentials_module.json'
id_folder = ''

#Iniciar sesión en Drive
def login():
    GoogleAuth().DEFAULT_SETTINGS['cliente_config_file'] = directorio_credenciales
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)
    
    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_numbers=[8092])
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
        
    gauth.SaveCredentialsFile(directorio_credenciales)
    credenciales = GoogleDrive(gauth)
    return credenciales


#Subir un archivo a Drive
def subir_archivo(ruta_archivo, id_folder):
    credenciales = login()