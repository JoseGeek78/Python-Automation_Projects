import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import logging
import time  
from pytube import YouTube  
import pytube  

# Configure logging
logging.basicConfig(filename='video_processing.log', level=logging.INFO)

# Variables
file_path = 'enlaces_videos/enlaces.xlsx'
sheet_name = 'Hoja1'
column_name = 'Videos'
credentials_path = 'credentials.json'
folder_id = ''  # ID de la carpeta de destino en Google Drive

def login():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(credentials_path)

    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_numbers=[8092])
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile(credentials_path)
    return GoogleDrive(gauth)

def upload_file(file_path, folder_id, drive):
    try:
        file = drive.CreateFile({'parents': [{'id': folder_id}]})
        filename = os.path.basename(file_path)

        # Prepend a unique identifier (timestamp) to avoid overwriting
        timestamp = int(time.time())
        new_filename = f'{timestamp}_{filename}'
        file['title'] = new_filename

        file.SetContentFile(file_path)
        file.Upload()
        logging.info(f'Successfully uploaded: {new_filename}')
    except Exception as e:
        logging.error(f'Error uploading {file_path}: {str(e)}')
    finally:
        drive.Close()  # Cerrar la conexión

def download_and_upload(video_link, folder_id):
    try:
        yt = YouTube(video_link)
        video = yt.streams.get_highest_resolution()
        filename = f'YT/{video.title}.mp4'

        # Download video
        video.download(filename=filename)

        # Upload video to Google Drive
        drive = login()
        upload_file(filename, folder_id, drive)

        # Delete downloaded video after upload
        os.remove(filename)
    except pytube.exceptions.PyTubeError as e:
        logging.error(f'Error downloading {video_link}: {str(e)}')
    except Exception as e:
        logging.error(f'Unexpected error processing {video_link}: {str(e)}')

def main():
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    video_links = df[column_name].values

    for link in video_links:
        download_and_upload(link, folder_id)

if __name__ == "__main__":
    main()
