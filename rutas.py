from flask import Flask
from flask import request #para recibir parametros en la ruta tipo /params?a=b&c=6

app= Flask(__name__) # nuevo objeto (instancia), recibe como parametro name

@app.route('/') # necesitamos un wrap, decorador indica la ruta

def index(): # funcion que se ejecuta
 return 'hola  mundo!!'


@app.route('/params') 

def params():
  param= request.args.get('params1','no contiene este parametro') #http://127.0.0.1:8080/params?params1=jorge_lobo
  param_dos= request.args.get('params2','no contiene este parametro') #http://127.0.0.1:8080/params?params1=jorge&params2=lobo 
  return 'El parametro es: {} , {}'.format(param, param_dos)


if  __name__== '__main__':

  app.run(port=8080, debug=True) #debug x default es falso
