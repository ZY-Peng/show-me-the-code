#/usr/bin/env python
#-*- coding:utf-8 -*-

from PIL import Image,ImageDraw,ImageFont
import random

Num=str(random.randint(1,99))

im=Image.open('github.jpg')
w,h=im.size
wDraw = 0.8 * w
hDraw = 0.2 * h

font = ImageFont.truetype('Ubuntu-MI.ttf', 50)
draw = ImageDraw.Draw(im)
draw.text((wDraw,hDraw), Num, font=font, fill=(255,33,33))

im.save('github_1.jpg', 'jpeg')
