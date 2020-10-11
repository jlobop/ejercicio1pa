from flask import Flask, jsonify, make_response, request
from csv import reader
import json

app= Flask(__name__)

global archivo="/home/jlobo/python/curso_avanzado/caso1/listaAlumnos.csv"


class Alumnos:
    def __init__(self,id="",nombre="",apellido="",ci="",estado="pendiente", db=archivo):
        self.id=id
        self.nombre=nombre
        self.apellido=apellido
        self.ci=ci
        self.estado=estado
        self.db=db

    def toarray(self):
        return [self.id,self.nombre,self.apellido,self.ci,self.estado]
    def todict(self):
        return {'id':self.id,'nombre':self.nombre,'apellido':self.apellido,'ci':self.ci,'estado':self.estado}
    def getfile(self):
        return self.db
    def inscribo(self):
        file=open(self.db,'a')
        alumno=','.join(map(str,self.toarray()))
        file.write(alumno+"\n")
        file.close()

# A partir del archivo csv, obtengo una lista de objetos donde cada objeto es un alumno
def leo_archivo(file=archivo):
    listaAlumnos=[]
    with open(file,'r') as fp:
      alumnos=reader(fp)
      for i in alumnos:
         alumno=Alumnos(i[0],i[1],i[2],i[3])
         listaAlumnos.append(alumno)
    return listaAlumnos
#funcnion que carga la lista de alumnos en mmemoria y devuelve una lista si alguno machea con
#algun criterio, de lo contrario devuelve una lista vacia
def alumnos_check(key,valor,file=archivo):
    listaAlumnos=leo_archivo(file)
    out=[]
    for elemento in listaAlumnos:
       print(elemento.apellido)
       print(valor)
       if key=='estado':
           if elemento.estado == valor:
              out.append(elemento)
       elif key=='id':
           if elemento.id == valor:
               out.append(elemento)
               print(elemento.nombre)
       else:
           print("no termine")
    return out

def respuesta(status=201):
    respuesta_dic={'status':'ok'}
    response =jsonify(respuesta_dic)
    response.status_code=status
    response.headers["Content-Type"]= "application/json"
    return response
# maneja los id
def controlador():
    return null


@app.route('/alumno', methods=['POST','GET'])
def alumno():
    if request.method == 'POST':
       content=request.json
       if isinstance(content,list): #recibo mas de un nombre, lista de diccionarios
         for i in content:
             #print(i['id'],i["nombre"])
             a=Alumnos(i["id"],i["nombre"],i["apellido"],i["ci"],i["estado"])
             a.inscribo()
       else: #recibo solo un nombre
         #print(content['id'],content['nombre']
         if not (alumnos_check('id',int(content['id']),archivo)):
             #print("archivo: "+archivo)
             a=Alumnos(content["id"],content["nombre"],content["apellido"],content["ci"],content["estado"])
             a.inscribo()
             response=respuesta(201)
             return response
         else:
             response=respuesta(400)
             return response
    else:
       lista=leo_archivo()
       listaDic=[]
       for i in lista:
          listaDic.append(i.todict())
       response=make_response(jsonify(listaDic))
       response.headers["Content-Type"]=  "application/json"
       return response

def main():
    app.run(port=8080, debug=True)



"""
alumno1=Alumnos(2,'jorge','lobo',2022233)
alumno1.inscribo()
lista=leo_archivo(archivo)
for i in lista:
    print(i.array())
"""
if  __name__== '__main__':
   main()
