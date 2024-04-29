import base64
from PIL import Image
from io import BytesIO
import os


def convert_to_base64(filename: str):
    img = Image.open(f'imageshit/{filename}.jpeg')
    img = img.resize((512, int(img.height * 512 / img.width)))
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode()
    os.remove(f'imageshit/{filename}.jpeg')
    return image_base64
