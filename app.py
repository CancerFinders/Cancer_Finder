from flask import Flask, jsonify, request
from os import listdir
from os import replace
from random import randint
from ImageWork import сolors
from ImageWork.dicom import get_img_dicom
from DataBase.dbMongo import insert_file_info
import cv2



from flask_cors import CORS

app = Flask(__name__)
CORS(app)


#POST запрос
#В него отправлятся
# 1.Имя файла
# 2.Тип изображение ( chest(грудь), hands, legs и тд) пока папочки есть только под chest
# 3. Из формы: есть ли рак - True or False
# 4. Из формы: тип рака любая - строка
# 5. Из формы: комментрий - строка

@app.route('/sendjson', methods=['POST'])
def send_json():
    print(request.json)
#    insert_file_info(request.json['filename'], request.json['imgType'], request.json['isCancer'], request.json['cancerType'], request.json['comment'])

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
    dirname = 'static/unmarked_img' + '/' + type
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
