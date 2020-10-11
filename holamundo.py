from flask import Flask

app= Flask(__name__) # nuevo objeto (instancia), recibe como parametro name

@app.route('/') # necesitamos un wrap, decorador indica la ruta

def index(): # funcion que se ejecuta
 return 'hola  mundo'

app.run() #Se encarga de ejecuta r el servidor en el 5000 por default
