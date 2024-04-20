from pydrive.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

#Crea un servidor web local y maneja automáticamente la autenticación.