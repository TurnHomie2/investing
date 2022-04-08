from PIL import Image, ImageTk


def load_image(name, pic_type, width, height):
    path = f'assets/images/{name}.{pic_type}'
    img_og = Image.open(path)
    img_res = img_og.resize((width, height))
    image_tk = ImageTk.PhotoImage(img_res)
    return image_tk
