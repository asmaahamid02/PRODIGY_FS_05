from django.http import HttpRequest, HttpResponse
from PIL import Image
from io import BytesIO
from .utils import image_utils
from urllib.parse import unquote
import os
from django.conf import settings

def generate_thumbnail(request:HttpRequest, size: str, path:str) -> HttpResponse:
    if not size or not path:
        return HttpResponse(f"Both the image path and the size are required", status=400)
    
    path = unquote(path)
    path = settings.PROJECT_DIR + path

    try:
        image = Image.open(path)
    except Exception as e:
        return HttpResponse(f"An error occurred while opening the image: {e}", status=500)

    sizes = size.split('x')

    try:
        width = int(sizes[0])
        height = int(sizes[1]) if len(sizes) > 1 else None
    except Exception as e:
        return HttpResponse(f"An error occurred while parsing the size: {e}", status=500)
    
    if height is None:
        height = int(image.height * width / image.width)

    image.thumbnail((width, height))

    thumbnail_io = BytesIO()
    image.save(thumbnail_io, format='webp', quality=90)
    thumbnail_io.seek(0)

    return HttpResponse(thumbnail_io, content_type=f"image/webp")
    
