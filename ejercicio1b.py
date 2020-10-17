from flask import Flask, jsonify, make_response, request
from csv import reader
import json
import csv

ARCHIVOCSV='/Users/jlobo/python/python_avanzado/ejercicio1/listaAlumnos.csv'
PATH='/Users/jlobo/ejemplos/'
nombrearchivo='listaAlumnos.csv'
listaEstados=('aprobado','reprobado','pendiente')


app= Flask(__name__)

class Alumnos:
    def __init__(self,id="",nombre="",apellido="",ci="",estado="", db=ARCHIVOCSV):
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



class listaAlumnos:
  def __init__(self,alumno=None,id=None,archivo=ARCHIVOCSV):
    
    self.archivo=archivo
    self.alumno=alumno
    self.id=id
    self.lista=[]

  def cargolista(self):
    self.lista=leo_archivo(self.archivo)
    
  def addAlumno(self,alumno):
    if type(alumno) == Alumnos:
       self.lista.append(alumno)
    else:
      print("bad object")
  
  def delAlumno(self,id):
    lista=list(filter(lambda alumnos: alumnos.id != id,self.lista))
    self.lista=lista
       #return self.lista
  def graboLista(self):
    with open(self.archivo,'w') as fp:
       wr = csv.writer(fp, quoting=csv.QUOTE_ALL)
       for x in self.lista:
         wr.writerow(x.toarray())
    fp.close() 
#metodo que chquea que carga la lista de alumnos en mmemoria y devuelve una lista si alguno machea con
#algun criterio, de lo contrario devuelve una lista vacia
  def check(self,key,valor):
    #listaAlumnos=leo_archivo(file)
    if key=='estado':
        return list(filter(lambda alumnos: alumnos.estado == valor,self.lista))
    elif key=='id':
        return list(filter(lambda alumnos: alumnos.id == valor,self.lista))
    else:
        print("no termine")
        out=[]
        return out

def respuesta(status=201,respuesta_dic={'status':'ok'}):
    response =make_response(jsonify(respuesta_dic))
    response.status_code=status
    response.headers["Content-Type"]= "application/json"
    return response

# A partir del archivo csv, obtengo una lista de objetos donde cada objeto es un alumno
def leo_archivo(file=ARCHIVOCSV):
    listaAlumnos=[]
    with open(file,'r') as fp:
      alumnos=reader(fp)
      for i in alumnos:
         alumno=Alumnos(int(i[0]),i[1],i[2],i[3],i[4])
         listaAlumnos.append(alumno)
    return listaAlumnos


listado=listaAlumnos()
listado.cargolista()

@app.route('/alumno/<int:idAlumno>',methods=['GET'])
@app.route('/alumno/',methods=['GET'])
def alumno(idAlumno=[]):
  if 'estado' in request.args:  ## chequeo que haya parametro
      estado=request.args.get('estado')
      if estado in listaEstados:
          out=listado.check('estado',estado)
          if out:
              response=make_response(jsonify(list(map(lambda x: x.todict(),out))))
              response.headers["Content-Type"]=  "application/json"
              return response
          else:
             #return "<h3>No hay alumnos {}</h3>".format(estado)
             return respuesta(204)
      else: 
          return respuesta(400)
      
  elif  idAlumno: #Si idalumno no vaciovacio 
       # out=listaAlu(idAlumno)
        out=listado.check('id',idAlumno)
        if not out:
            return respuesta(400)
        else:
            return respuesta(200,out[0].todict())
  else: #devuelvo todo
    response=make_response(jsonify(list(map(lambda x: x.todict(),listado.lista))))
    response.headers["Content-Type"]=  "application/json"
    return response  

@app.route('/alumno/<int:idAlumno>', methods=['DELETE'])
@app.route('/alumno', methods=['POST'])
def PostDelete(idAlumno=[]):
    if request.method == 'POST':
       content=request.json
       if isinstance(content,list): #recibo mas de un nombre, lista de diccionarios
         for i in content:
             a=Alumnos(int(i["id"]),i["nombre"],i["apellido"],i["ci"],i["estado"])
             a.inscribo()
             listado.addAlumno(a)    
       else: #recibo solo un nombre
         if not (listado.check('id',content['id'])):
             a=Alumnos(int(content["id"]),content["nombre"],content["apellido"],content["ci"],content["estado"])
             a.inscribo()
             listado.addAlumno(a)
             return respuesta(201)
         else:
             response=respuesta(400)
             return response
    elif request.method == 'DELETE':
       if idAlumno:
          response=listado.delAlumno(idAlumno)
          listado.graboLista()
          return "Se borra el alumno {}".format(idAlumno), 200
       else:
           return respuesta(400)         

@app.route('/alumno/<int:id>', methods=['PUT'])
def modifico(id):
  alumnotoModif=request.json
  alumno=listado.check('id',id)
  if not alumno:
    return "No encontrado: Alumno cuyo id es {}".format(id),404
  else:
    listado.delAlumno(id)
    a=Alumnos(int(alumnotoModif["id"]),alumnotoModif["nombre"],alumnotoModif["apellido"],alumnotoModif["ci"],alumnotoModif["estado"])
    listado.addAlumno(a)
    listado.graboLista()
    return "Usuario modificado con exito"




def main():  
  app.config['JSON_AS_AjsonSCII'] = False
  app.run(port=8080, debug=True)
if  __name__== '__main__':
   main()
