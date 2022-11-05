import os
import numpy as np
from flask import Flask, jsonify, request
from os import listdir
from os import replace
from os import curdir
from os import getcwd
import json as json_lib
from random import randint
from ImageWork import сolors
from ImageWork.dicom import get_img_dicom
from DataBase.dbMongo import insert_file_info
from json import load
from matplotlib import pyplot as plt
import numpy
import tqdm
from pathlib import Path
#При деплое заменить на
from nn import api
# from Cancer_Finder.nn import api
import cv2



from flask_cors import CORS

api.reload_model(Path('weights'))

UPLOAD_FOLDER = 'upload'
# расширения файлов, которые разрешено загружать
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'json'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


@app.route('/generate', methods=['POST'])
def generate():
    data = request.json

    img = сolors.RGBAtoDCM(data['img'], data['h'], data['w'] )
    # print(img)
    cv2.imwrite('PNG.png', img)
    case = api.normalize(img)
    x = api.predict_ones(case)
    x[x < 0] = 0
    x[x > 1] = 1
    # print('###################################################################################################################')
    # print(x)
    r = numpy.zeros((x.shape[2], x.shape[3], 3))
    r[:, :, 0] = x[1, 0]

    try:
        os.mkdir('Generate')
    except:
        ...

    plt.imsave(f"Generate/{request.json['filename']}.png", r)
    # new_img = api.normalize()
    print('END')
    json = jsonify(201)
    json.headers.add("Access-Control-Allow-Origin", "*")
    return json

@app.route('/sendimg', methods=['POST'])
def send_img():
    print('GET FILE')
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename:
            # безопасно извлекаем оригинальное имя файла
            filename = file.filename
            # сохраняем файл
            print(filename)
            file.save(app.config['UPLOAD_FOLDER'] + '/' + filename)

    json = jsonify({
        201
    })
    json.headers.add("Access-Control-Allow-Origin", "*")
    return json

@app.route('/sendjson', methods=['POST'])
def send_json():
    print(type(request.json.keys()))
    data = request.json
    # for i in data['img']:
    #     if (i != 0 and i != 255):
    #         print(' NON BLACK OR WHITE',i)

    #insert_file_info(request.json['filename'], request.json['imgType'], request.json['isCancer'], request.json['cancerType'], request.json['comment'])

    # fullname_old = 'static/unmarked_img' + '/' + request.json['imgType'] + '/' + request.json['filename']
    # fullname_new = 'static/marked_img' + '/' + request.json['imgType'] + '/' + request.json['filename']
    # replace(fullname_old, fullname_new)

    json = jsonify(201)
    json.headers.add("Access-Control-Allow-Origin", "*")
    return json

@app.route('/setimg', methods=['POST'])
def set_image_info():
    # print(request.json)
    # insert_file_info(request.json['filename'], request.json['imgType'], request.json['isCancer'], request.json['cancerType'], request.json['comment'])

    data = request.json
    name = request.json['filename'].split('.')[0]
    try:
        os.mkdir('static/marked_img' + '/' + request.json['type'] + '/' + name)
    except:
        ...
    old_path = 'static/unmarked_img' + '/' + request.json['type'] + '/'
    new_path = 'static/marked_img' + '/' + request.json['type'] + '/' + name + '/'

    fullname_old = old_path + request.json['filename']
    fullname_new = new_path + request.json['filename']
    replace(fullname_old, fullname_new)

    gen = сolors.RGBAtoRGB(data['img'], data['h'], data['w'])
    # print(data['bitMask'])
    cv2.imwrite(new_path +  name + '_mark.png', gen)

    # buff_json = jsonify(request.json)
    with open(new_path + request.json['filename'] +'.json', "w") as file:
        file.write(request.json)


    json = jsonify(
        201
    )
    json.headers.add("Access-Control-Allow-Origin", "*")
    return json


        #GET запрос
#в запросе указываешь тип изображение (пока есть только chest)
#в ответ получаешь имя присланного файла и двумерный массив пикселей изображения


@app.route('/img3d/<string:type>/<int:weight>/<int:height>', methods=['GET'])
def get_3dimage(type, weight, height):
    print('DIR: ' + getcwd())
    dirname = 'static/3D_Cases' + '/' + type
    cases = listdir(dirname)
    case = cases[randint(0, len(cases) - 1)]
    dirname = dirname + '/' + case
    images = listdir(dirname)

    resultList = []
    for filename in images:

        fullname = dirname + '/' + filename
        if (filename.split(sep = '.')[1] == 'dcm'):
            img = get_img_dicom(fullname)
            img = сolors.DCMtoRGB(img)

        else:
            img = cv2.imread(fullname)
        img = cv2.resize(img, (weight, height))
        img = img.tolist()
        w = len(img)
        h = len(img[0])
        img = сolors.RGBtoRGBA(img)
        img = сolors.PlaneToLine(img)

        resultList.append({
        'name': filename,
        'type': type,
        'img': img,
        'w': w,
        'h': h,
    })
    json = jsonify(resultList)
    json.headers.add("Access-Control-Allow-Origin", "*")
    return json


@app.route('/img/<string:type>/<int:weight>/<int:height>', methods=['GET'])
def get_image(type, weight, height):
    dirname =  'static/unmarked_img' + '/' + type
    print('DIR: ' + getcwd())
    images = listdir(dirname)
    filename = images[randint(0, len(images) - 1)]
    fullname = dirname + '/' + filename
    if (filename.split(sep = '.')[1] == 'dcm'):
        img = get_img_dicom(fullname)
        img = сolors.DCMtoRGB(img)

    else:
        img = cv2.imread(fullname)
    img = cv2.resize(img, (weight, height))
    img = img.tolist()
    w = len(img)
    h = len(img[0])
    img = сolors.RGBtoRGBA(img)
    img = сolors.PlaneToLine(img)

    json = jsonify({
        'name': filename,
        'img': img,
        'w': w,
        'h': h,
    })
    json.headers.add("Access-Control-Allow-Origin", "*")
    return json

@app.route('/')
def hello_world():
    return 'Hello Cancer!'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run()
