# from os import listdir
# from random import randint
# import cv2
# from skimage.io import imread
# from os.path import isfile, join
#
# image = 'unmarked/' + str(listdir('unmarked')[randint(0, len(listdir('unmarked')) - 1)])
# # print(listdir('unmarked')[randint(0, len(listdir('unmarked')) - 1)])
# # print(imread(image))
#
# dirname = 'unmarked'
# images = listdir(dirname)
# filename = images[randint(0, len(images) - 1)]
# fullname = dirname + '/' + filename
#
#
# print(cv2.imread(fullname))
import requests

answer = requests.post('http://127.0.0.1:5000/setimg', json={
                                                            "filename":"1.png",
                                                            "imgType": "chest",
                                                            "isCancer": "False",
                                                            "cancerType": "normal",
                                                            "comment": "Test Text" })

print(answer)