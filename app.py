from flask import Flask, jsonify, request
from os import listdir
from os import replace
from random import randint
from DataBase.dbMongo import insert_file_info
import cv2


app = Flask(__name__)

@app.route('/setimg', methods=['POST'])
def set_image_info():
    print(request.json)
#    insert_file_info(request.json['filename'], request.json['imgType'], request.json['isCancer'], request.json['cancerType'], request.json['comment'])

    fullname_old = 'static/unmarked_img' + '/' + request.json['imgType'] + '/' + request.json['filename']
    fullname_new = 'static/marked_img' + '/' + request.json['imgType'] + '/' + request.json['filename']
    replace(fullname_old, fullname_new)

    return 201

@app.route('/img/<string:type>', methods=['GET'])
def get_image(type):
    dirname = 'static/unmarked_img' + '/' + type
    images = listdir(dirname)
    filename = images[randint(0, len(images) - 1)]
    fullname = dirname + '/' + filename

    img = cv2.imread(fullname).tolist()
    print(img)
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
