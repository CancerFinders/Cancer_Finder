import numpy as np


def DCMtoRGB(img):
    new_img = np.ndarray((len(img), len(img[0]), 3))

    for row_num in range(0,len(img)):


        for pixel_num in range(0, len(img[row_num])):
            color = img[row_num][pixel_num] * 255
            pixel = (color, color, color)
            new_img[row_num][pixel_num][0] = color
            new_img[row_num][pixel_num][1] = color
            new_img[row_num][pixel_num][2] = color

    return new_img

def RGBtoRGBA(img , a = 255):

    for row_num in range(0,len(img)):
        for pixel_num in range(0, len(img[row_num])):
            img[row_num][pixel_num].append(a)

    return img


def PlaneToLine(img):
    line = []

    for row in img:
        for pixel in row:
            line.extend(pixel)

    return line