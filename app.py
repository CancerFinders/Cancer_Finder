from flask import Flask, jsonify, request
from os import listdir
from os import replace
from random import randint
from ImageWork.dicom import get_img_dicom
from DataBase.dbMongo import insert_file_info
import cv2


app = Flask(__name__)


#POST запрос
#В него отправлятся
# 1.Имя файла
# 2.Тип изображение ( chest(грудь), hands, legs и тд) пока папочки есть только под chest
# 3. Из формы: есть ли рак - True or False
# 4. Из формы: тип рака любая - строка
# 5. Из формы: комментрий - строка
@app.route('/setimg', methods=['POST'])
def set_image_info():
    print(request.json)
#    insert_file_info(request.json['filename'], request.json['imgType'], request.json['isCancer'], request.json['cancerType'], request.json['comment'])

    fullname_old = 'static/unmarked_img' + '/' + request.json['imgType'] + '/' + request.json['filename']
    fullname_new = 'static/marked_img' + '/' + request.json['imgType'] + '/' + request.json['filename']
    replace(fullname_old, fullname_new)

    return 201


#GET запрос
#в запросе указываешь тип изображение (пока есть только chest)
#в ответ получаешь имя присланного файла и двумерный массив пикселей изображения
@app.route('/img/<string:type>', methods=['GET'])
def get_image(type):
    dirname = 'static/unmarked_img' + '/' + type
    images = listdir(dirname)
    filename = images[randint(0, len(images) - 1)]
    fullname = dirname + '/' + filename
    if (filename.split(sep = '.')[1]):
        img = get_img_dicom(fullname)
    else:
        img = cv2.imread(fullname).tolist()

    json = jsonify({
        'name': filename,
        'img': img
    })
    return json

@app.route('/')
def hello_world():
    return 'Hello Cancer!'

if __name__ == '__main__':
    app.run()
