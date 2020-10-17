from flask import Flask, jsonify, make_response, request
from csv import reader
from datetime import datetime
from shutil import move
import json

app= Flask(__name__)

#
#archivo= '/home/jlobo/python/curso_avanzado/caso1/listaAlumnos.csv'
archivo='/Users/jlobo/ejemplos/listaAlumnos.csv'
PATH='/Users/jlobo/ejemplos/'
nombrearchivo='listaAlumnos.csv'
listaEstados=('aprobado','reprobado','pendiente')

class Alumnos:
    def __init__(self,id="",nombre="",apellido="",ci="",estado="", db=archivo):
        self.id=int(id)
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
    def __str__(self):
        return "Alumno: {} {}, ID: {}".format(self.nombre,self.apellido,self.id)

# A partir del archivo csv, obtengo una lista de objetos donde cada objeto es un alumno
def leo_archivo(file=archivo):
    listaAlumnos=[]
    with open(file,'r') as fp:
      alumnos=reader(fp)
      for i in alumnos:
         alumno=Alumnos(int(i[0]),i[1],i[2],i[3],i[4])
         listaAlumnos.append(alumno)
    return listaAlumnos
#funcion que carga la lista de alumnos en mmemoria y devuelve una lista si alguno machea con
#algun criterio, de lo contrario devuelve una lista vacia
def alumnos_check(key,valor,lista):
    #listaAlumnos=leo_archivo(file)
    if key=='estado':
        return list(filter(lambda alumnos: alumnos.estado == valor,lista))
    elif key=='id':
        return list(filter(lambda alumnos: alumnos.id == valor,lista))
    else:
        print("no termine")
        out=[]
        return out

def respuesta(status=201,respuesta_dic={'status':'ok'}):
    response =make_response(jsonify(respuesta_dic))
    response.status_code=status
    response.headers["Content-Type"]= "application/json"
    return response
# maneja los id
def controlador():
    pass

def borraAlumno(key,value,lista):
    listaAlumnos=leo_archivo(file)
    if key =='id':
        listasid = list(filter(lambda alumnos:alumnos.id != value))

def dumpListtoFile(lista):
   now=datetime.now()
   date_str=now.strftime("%Y%m%d%H%M%S")
   move(archivo,PATH+nombrearchivo+'.'+datetime) # creo bkp
   lambda lista: expression

   


@app.route('/alumno/<int:idAlumno>',methods=['PUT','GET','DELETE'])
@app.route('/alumno', methods=['POST','GET'])
def alumno(idAlumno=[]):
    if 'estado' in request.args:  ## chequeo que haya parametro
        estado=request.args.get('estado')
    else: estado=[]
    if request.method == 'POST':
       content=request.json
       if isinstance(content,list): #recibo mas de un nombre, lista de diccionarios
         for i in content:
             a=Alumnos(int(i["id"]),i["nombre"],i["apellido"],i["ci"],i["estado"])
             a.inscribo()
       else: #recibo solo un nombre
         if not (alumnos_check('id',int(content['id']),archivo)):
             a=Alumnos(int(content["id"]),content["nombre"],content["apellido"],content["ci"],content["estado"])
             a.inscribo()
             response=respuesta(201)
             return response
         else:
             response=respuesta(400)
             return response
    elif request.method == 'DELETE':
       if idAlumno:
           response=borraAlumno('id',idAlumno)
           return response
        else:
            return respuesta(400)         
    elif estado:
        if estado in listaEstados:
           out=alumnos_check('estado',estado)
           if out:
              response=make_response(jsonify(list(map(lambda x: x.todict(),out))))
              response.headers["Content-Type"]=  "application/json"
              return response
           else:
             #return "<h3>No hay alumnos {}</h3>".format(estado)
             return respuesta(204)
        else: 
            return respuesta(400)
        if not out:
            return respuesta(400)
    elif  idAlumno: #Si idalumno no vaciovacio 
        out=alumnos_check('id',idAlumno)
        if not out:
            return respuesta(400)
        else:
            return respuesta(200,out[0].todict())
    else:
       lista=leo_archivo()
       response=make_response(jsonify(list(map(lambda x: x.todict(),lista))))
       response.headers["Content-Type"]=  "application/json"
       return response
        
        



#@app.route('/alumno/<int:idAlumno>')
#def alumnosByid(idAlumno):
 #   alumno=alumnos_check('id',idAlumno)
 #   if not alumno:



def main():
  listadoDealumnos=leo_archivo()
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
