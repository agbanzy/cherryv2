# File: /cherryAI/image_processor.py

from PIL import Image

def open_image(image_path):
    return Image.open(image_path)

def save_image(image, output_path):
    image.save(output_path)

def resize_image(image, size):
    return image.resize(size)

def crop_image(image, box):
    return image.crop(box)

def rotate_image(image, angle):
    return image.rotate(angle)


 # File: /cherryAI/image_processor.py

from PIL import Image

def convert_to_grayscale(image_path):
    img = Image.open(image_path).convert('L')
    gray_image_path = image_path.rsplit('.', 1)[0] + '_gray.' + image_path.rsplit('.', 1)[1]
    img.save(gray_image_path)
    return gray_image_path


from PIL import Image

def convert_to_grayscale(image_path):
    img = Image.open(image_path).convert('L')
    gray_image_path = image_path.rsplit('.', 1)[0] + '_gray.' + image_path.rsplit('.', 1)[1]
    img.save(gray_image_path)
    return gray_image_path