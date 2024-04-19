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
def subir_archivo(ruta_archivo,id_folder):
    credenciales = login()
    archivo = credenciales.CreateFile({'parents': [{"kind": "drive#fileLink",\
                                                    "id": id_folder}]})
    archivo['title'] = ruta_archivo.split("/")[-1]
    archivo.SetContentFile(ruta_archivo)
    archivo.Upload()
    
    
    def main():
        #Leer los links del excel
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        column_data = df[column_name]
        