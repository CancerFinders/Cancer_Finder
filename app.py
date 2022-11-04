import os
import numpy as np
from flask import Flask, jsonify, request
from os import listdir
from os import replace
from os import curdir
from os import getcwd
from random import randint
from ImageWork import сolors
from ImageWork.dicom import get_img_dicom
from DataBase.dbMongo import insert_file_info
from json import load
import cv2



from flask_cors import CORS
UPLOAD_FOLDER = 'upload'
# расширения файлов, которые разрешено загружать
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'json'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


@app.route('/sendimg', methods=['POST'])
def send_img():
    print('GET FILE')
    if request.method == 'POST':
        # проверим, передается ли в запросе файл
        # if 'file' not in request.files:
        #     # После перенаправления на страницу загрузки
        #     # покажем сообщение пользователю
        #     flash('Не могу прочитать файл')
        #     return redirect(request.url)
        file = request.files['file']
        # Если файл не выбран, то браузер может
        # отправить пустой файл без имени.
        # if file.filename == '':
        #     flash('Нет выбранного файла')
        #     return redirect(request.url)
        if file and file.filename:
            # безопасно извлекаем оригинальное имя файла
            filename = file.filename
            # сохраняем файл
            print(filename)
            file.save(app.config['UPLOAD_FOLDER'] + '/' + filename)
            # если все прошло успешно, то перенаправляем
            # на функцию-представление `download_file`
            # для скачивания файла
            # return redirect(url_for('download_file', name=filename))

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
    gen = сolors.RGBAtoRGB(data['img'], data['h'], data['w'])
    cv2.imwrite('PNG.png', gen)
    #insert_file_info(request.json['filename'], request.json['imgType'], request.json['isCancer'], request.json['cancerType'], request.json['comment'])

    # fullname_old = 'static/unmarked_img' + '/' + request.json['imgType'] + '/' + request.json['filename']
    # fullname_new = 'static/marked_img' + '/' + request.json['imgType'] + '/' + request.json['filename']
    # replace(fullname_old, fullname_new)

    json = jsonify({
        201
    })
    json.headers.add("Access-Control-Allow-Origin", "*")
    return json

@app.route('/setimg', methods=['POST'])
def set_image_info():
    print(request.json)
#    insert_file_info(request.json['filename'], request.json['imgType'], request.json['isCancer'], request.json['cancerType'], request.json['comment'])

    fullname_old = 'static/unmarked_img' + '/' + request.json['imgType'] + '/' + request.json['filename']
    fullname_new = 'static/marked_img' + '/' + request.json['imgType'] + '/' + request.json['filename']
    replace(fullname_old, fullname_new)

    json = jsonify({
        201
    })
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
    app.run()
