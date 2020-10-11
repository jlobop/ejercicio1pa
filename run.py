from flask import Flask

app= Flask(__name__) # nuevo objeto (instancia), recibe como parametro name

@app.route('/') # necesitamos un wrap, decorador indica la ruta

def index(): # funcion que se ejecuta
 return 'hola  mundo!!'

if  __name__== '__main__':

  app.run(port=8080, debug=True) #debug x default es falso
