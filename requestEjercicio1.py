import json
import requests

if __name__== '__main__':

    payload=[{'id':'23','nombre':'Juana', 'apellido':'molina','ci':'344443','estado':'activo'},{'id':'11','nombre':'Alexis', 'apellido':'Suarez','ci':'54455','estado':'activo'}]

    url='http://127.0.0.1:8080/alumno'
    headers={'Content-Type':'application/json'}

    response = requests.post(url,data=json.dumps(payload), headers=headers)


    #if response.status_code == 200:
    print(response.headers)

        #print(response.headers['Server'])
