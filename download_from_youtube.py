from pytube import YouTube
import pandas as pd
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

#variables excel
file_path = 'enlaces_videos/enlaces.xlsx'
sheet_name = 'Hoja1'
column_name = 'Videos'

#credenciales google drive
directorio_credenciales = 'credentials_module.json'
id_folder = ''

