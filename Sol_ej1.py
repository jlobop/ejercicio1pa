

from flask import Flask,jsonify,request

app = Flask(__name__)
app.config['JSON_AS_AjsonSCII'] = False  # Para que tolere los acentos UTF-8

alumnos = [{'id':1,'nombre':'Rodrigo','apellido':'Pérez','estado':'aprobado'}]

@app.route('/alumnos')
def get_alumnos():
    """ Obtiene todos los alumnos. Acepta también: GET /alumnos?estado=[aprobado|reprobado|pendiente] """
    estado = request.args.get('estado')
    if estado:
        return jsonify([al for al in alumnos if al.get('estado') == estado])
    else:
        return jsonify(alumnos)

@app.route('/alumnos/<int:id>')
def get_alumnos_by_id(id):
    """ Obtiene el alumno identificado con el id especificado """

    return jsonify([a for a in alumnos if a.get('id') == id])

@app.route('/alumnos',methods=['POST'])
def post_alumnos():
    """ Servicio que da de alta un alumno (o varios).
    Los datos se envía vía Json con, al menos, nombre, ci, estado. """

    if request.headers.get('Content-Type') == 'application/json':
        _alumnos = request.json
        if isinstance(_alumnos,list):
            for al in _alumnos:
                alumnos.append(al)
        elif isinstance(_alumnos, dict):
            alumnos.append(_alumnos)
        else:
            return 'Bad Request', 400
        return 'OK', 201
    else:
        return 'Unsupported Media Type', 415


@app.route('/alumnos/<int:id>',methods=['PUT'])
def put_alumno(id):
    """ Servicio que modifica el alumno con el id específico. Se envía el mismo Json que se usa para dar de alta. """
    if request.headers.get('Content-Type') == 'application/json':
        update_alumno = request.json
        for al in alumnos:
            if al.get('id') == id:
                al.update(update_alumno)
                return jsonify(al), 201
        return 'Not Found:  No se encontro el alumno', 404
    else:
        return 'Unsupported Media Type', 415

@app.route('/alumnos/<int:id>',methods=['DELETE'])
def delete_alumno(id):
    """Borra el alumno con el id especificado """
    for al in alumnos:
        if al.get('id') == id:
            alumnos.remove(al)
            return 'OK', 201
    return 'Not Found:  No se encontro el alumno', 404



if __name__ == '__main__':  #este es el main si lo llamaron directamente
    app.run(debug=True)
