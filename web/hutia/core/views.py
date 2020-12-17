from flask import render_template, Blueprint, request, redirect, url_for, make_response, flash, jsonify, send_file
from flask_login import current_user
from functools import wraps
from hutia.model import User, getPatients, getPatient, loadData, Evolution, loadAllEvolution, getEvaluation, getEvaluations, howManyData
import variables as v
import os
from werkzeug import secure_filename
from flask_cors import cross_origin
import time
import datetime
from sqlalchemy import and_
from subprocess import Popen, PIPE
import cv2
import base64

core = Blueprint('core', __name__)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("user.login"))
        else:
            return f(*args, **kwargs)
    return wrap



@core.route("/index")
@login_required
def index():    
    
    if current_user.utype == 2:
        return redirect(url_for("core.patient_menu"))
    elif current_user.utype == 1:
        return redirect(url_for("core.manager_menu"))
    else:
        return redirect(url_for("user.logout"))


@core.route('/menu')
def patient_menu():
    return render_template("patient_index.html.j2", title="Menu", token=current_user.token, jitsi=v.JITSI)


@core.route('/menu-responsable')
def manager_menu():
    return render_template("manager_menu.html.j2", title="Menú Responsable", user=current_user)


@core.route('/patient/help')
def patient_ayuda():
    return render_template("patient_help.html.j2", title="Ayuda")

@core.route('/patient/evaluation')
def patient_evaluacion():
    if howManyData(current_user.idu) >= 2:
        da = True
        ev = getEvaluation(current_user.idu)
        res = (ev[0].data/ev[1].data-1)*100
    else:
        da = False
    res=0
    #if len(ev) != 2:
    #    return render_template("patient_index.html.j2", title="Menu", token=current_user.token)
    
    return render_template("patient_evaluation.html.j2", title="Evaluación", ev = res, da=da)

@core.route('/patient/tele')
def patient_telerehabilitation():
    return render_template("patient_telerehabilitation.html.j2", title="", token=current_user.token, jitsi=v.JITSI)


@core.route('/comunicacion', methods=["GET", "POST"])
def manager_com():
    if request.method=="POST":
        idu = request.form.get("patient",None)
        if idu != None:                
            patient = getPatient(idu)
            if patient != None:
                resp = make_response(render_template("manager_telerehabilitation.html.j2", title="Llamada con " + patient.name,token=patient.token, jitsi=v.JITSI))
                resp.headers["Access-Control-Allow-Origin"] = v.JITSI
                return resp
            elif idu == "grupal":
                resp = make_response(render_template("manager_telerehabilitation.html.j2", title="Llamada grupal ", token="reunion-grupal", jitsi=v.JITSI))
                resp.headers["Access-Control-Allow-Origin"] = v.JITSI
                return resp
            else:
                return "Usuario no encontrado",404
        else:
            return "Petición incorrecta",400
    patients = getPatients()
    return render_template("select_com.html.j2", title="Selección de Paciente", patients=patients)


@cross_origin
@core.route('/save-vid', methods=["POST"])
def save_vid():
    identifier = request.form.get("video_identifier")
    folder = os.path.join(v.basedir, "uploaded_videos", identifier)
    file = request.files["video-blob"]
    if file.filename != "":
        filename = secure_filename(file.filename)
        file.save(os.path.join(folder, filename))
        return "", 200
    else:
        return "", 400


@cross_origin
@core.route("/video-save-start", methods=["POST"])
def start_video_upload():
    identifier = request.form.get("video_identifier")
    os.makedirs(os.path.join(v.basedir, "uploaded_videos", identifier))
    return "", 200



@core.route("/upload_file", methods=["POST"])
def upload_file():
    folder = os.path.join(v.basedir, "uploaded_videos")
    file = request.files["zip"]
    if request.form['name'] != "":
        filename = secure_filename(request.form['name'])
        file.save(os.path.join(folder, filename))
        ts = filename.split("-")[0]
        machine = filename.split("-")[-1].split(".")[0]

        p = Popen(["bash", os.path.dirname(os.path.abspath(__file__))+"/merge.sh", folder, filename, ts+"-"+machine+".webm"], stdout=PIPE)

        return "", 200
    else:
        return "", 400


@core.route("/send_ip", methods=["POST"])
def send_ip():
    ip = request.form["ip"]
    user = request.form["user"]
    with open(os.path.join(v.basedir, "ips/ip.csv"), 'a') as csv:
        csv.write(user+","+ip+","+str(time.time())+"\n")
    return "", 200

@core.route("/statics", methods=["GET", "POST"])
def base_statics():
    if request.method == "GET":
        patients = getPatients()
        return render_template("manager_statics.html.j2", title="Selección de Paciente", patients=patients)
    else:
        return redirect(url_for("core.statics_menu", patient=request.form.get("patient",None)))

@core.route("/statics_menu/<patient>", methods=["GET"])
def statics_menu(patient):
    paciente = getPatient(patient)
    if paciente.utype != 2:
        return redirect(url_for("core.base_statics"))
    medidas = True
    if howManyData(patient) == 0:
        medidas = False
    return render_template("manager_statics_menu.html.j2", title="Menú de las medidas", name=paciente.name, idu=paciente.idu, medidas=medidas)

@core.route("/statics_menu/<patient>/add", methods=["GET", "POST"])
def statics_add(patient):
    paciente = getPatient(patient)
    if paciente.utype != 2:
        return redirect(url_for("core.base_statics"))
    if request.method == "GET":
        return render_template("statics/manager_add.html.j2", title="Añadir dato", name=paciente.name, date=datetime.datetime.now().strftime("%Y-%m-%d"), data=0)
    else:
        idu = paciente.idu
        date_origin = request.form.get("date",None)
        data = request.form.get("data",None)
        if date_origin is not None:
            date = int("".join(date_origin.split("-")))
            evolution = loadData(idu,date)
        if date is None or data is None:
            flash("No se ha rellenado correctamente", category="danger")
            return render_template("statics/manager_add.html.j2", title="Añadir dato", name=paciente.name, date=date_origin, data=data)
        elif evolution is not None:
            flash("Ya existe una medida para esa fecha en este paciente ", category="danger")
            return render_template("statics/manager_add.html.j2", title="Añadir dato", name=paciente.name, date=date_origin, data=data)
        else:      
            data = int(data)
            flash("Se ha añadido correctamente el valor"+str(evolution), category="success")
            evolution = Evolution(idu, date, data)
            v.db.session.add(evolution)
            v.db.session.commit()
            return redirect(url_for("core.statics_menu", patient=idu))

@core.route("/statics_menu/<patient>/mod", methods=["GET","UPDATE","DELETE"])
def statics_modify(patient):
    paciente = getPatient(patient)
    if paciente.utype != 2:
        return redirect(url_for("core.base_statics"))
    if request.method == "GET":
        return render_template("statics/manager_modify.html.j2",\
            title="Actualizar las medidas", name=paciente.name, idu=paciente.idu, evolution=loadAllEvolution(paciente.idu))
    elif request.method == "DELETE":
        date = request.form.get("date", None)
        if date is not None:
            Evolution.query.filter(and_(Evolution.date == date, Evolution.idu == paciente.idu)).delete()
            v.db.session.commit()
            return "", 200
        else:
            return "", 400
    elif request.method == "UPDATE":
        date = request.form.get("date", None)
        data = request.form.get("data", None)
        if date is not None and data is not None and data != "":
            loadData(paciente.idu, date).data = data
            v.db.session.commit()
            return "", 200
        else:
            return "", 400
    else:
        return "", 405

@core.route("/statics_menu/<patient>/show")
def show_statics(patient):
    paciente = getPatient(patient)
    if paciente.utype != 2:
        return redirect(url_for("core.base_statics"))
    eva = getEvaluations(paciente.idu)
    f = []
    e=[]
    for i in eva:
        f.append(v.app.jinja_env.filters["date"](i.date))
        e.append(i.data)
    return render_template("manager_statics_show.html.j2", title="Medidas de " + paciente.name, name=paciente.name, fecha = f, eva = e, idu=paciente.idu )

@core.route("/givemethepower")
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def give_me_the_code():

    r = {"code":"$('.action-btn').first().click()"}
    return jsonify(r)


@core.route("/videos", methods=["GET", "POST"])
def videos():

    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))

    ruta = os.path.join(v.basedir,"static","videos","processed")
    ficheros = os.listdir(ruta)
    ficheros.sort()
    if request.method == "GET":
        ficheros = list(set(map(lambda x: int(x.split("-")[1].split(".")[0]), filter(lambda x: x[0]!=".", ficheros))))
        ficheros.sort()
        return render_template("list_videos.html.j2", ficheros=ficheros, title="Lista de videos")
    else:
        f = request.form["file"]
        ficheros = list(filter(lambda x: x[-6:-1]+x[-1] == str(f)+".webm", ficheros))
        names = list(map(lambda x: datetime.datetime.fromtimestamp(int(x.split("-")[0])).strftime("%d de %m del %Y"),ficheros))
        # Si existe FIS 10 no funcionaría, que piense el siguiente
        imagenes = []
        for f in ficheros:
            vidcap = cv2.VideoCapture(os.path.join(ruta,f))
            success,image = vidcap.read()
            imagenes.append(base64.b64encode(cv2.imencode('.png', image)[1].tostring()).decode('ascii'))
        imagenes.reverse()
        ficheros.reverse()
        names.reverse()

        return render_template("machine_videos.html.j2", ficheros=ficheros, imagenes=imagenes, names=names)
        

@core.route("/descargar/<name>", methods=["GET"])
def download(name):

    if not current_user.is_authenticated:
        return "Not Allowed", 403
    machine=name.split("-")[1].split(".")[0]
    ts=int(name.split("-")[0])
    dt=datetime.datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
    return send_file(os.path.join(v.basedir,"static","videos","processed",name), as_attachment=True,
                    attachment_filename="FIS-HUBU-"+machine+"_"+str(dt)+".webm")
