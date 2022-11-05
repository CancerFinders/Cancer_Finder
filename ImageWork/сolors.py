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

def RGBAtoDCM(img, height , weidth):
    new_img = np.ndarray((height, weidth, 4))
    pixel_num = 0
    for height_num in range(0, height):
        # print('w', weidth_num)
        for weidth_num in range(0, weidth):

            color = ((img[pixel_num + 2] + img[pixel_num + 1] + img[pixel_num])/3) + 1
            new_img[height_num][weidth_num] = color
            pixel_num = pixel_num + 4

    return new_img

def RGBAtoRGB(img, height , weidth):
    # print(img)
    # for i in img:
    #     if (i != 0 and i != 255):
    #         print(' NON BLACK OR WHITE',i)
    new_img = np.ndarray((height, weidth, 4))
    pixel_num = 0
    for height_num in range(0, height):
        # print('w', weidth_num)
        for weidth_num in range(0, weidth):


            new_img[height_num][weidth_num] = [img[pixel_num + 2], img[pixel_num + 1] , img[pixel_num],  img[pixel_num + 3]]
            pixel_num = pixel_num + 4
    # print(new_img)
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