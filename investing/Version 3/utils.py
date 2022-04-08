from PIL import Image, ImageTk
from random import choice


def load_image(name, pic_type, width, height):
    path = f'assets/images/{name}.{pic_type}'
    img_og = Image.open(path)
    img_res = img_og.resize((width, height))
    image_tk = ImageTk.PhotoImage(img_res)
    return image_tk

def bool_calc(num):
    list = []
    for i in range(num):
        list.append(i)
    number = choice(list)
    if number == 0:
        return True
    else:
        return False

