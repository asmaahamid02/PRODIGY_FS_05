from django.http import HttpRequest, HttpResponse
from PIL import Image
from io import BytesIO
from urllib.parse import unquote
from django.conf import settings
from django.core.cache import cache

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

    filename = "_".join(path.split('/')[-4:])
    # generate a cache key for the thumbnail
    cache_key = f"thumbnail_{filename}_{width}x{height}"

    # check if the thumbnail is already in the cache
    cache_thumbnail = cache.get(cache_key)
    if cache_thumbnail:
        print(f"Cache hit for {cache_key}")
        return HttpResponse(cache_thumbnail, content_type=f"image/webp")

    image.thumbnail((width, height))

    thumbnail_io = BytesIO()
    image.save(thumbnail_io, format='webp', quality=90)
    thumbnail_io.seek(0)

    # save the thumbnail in the cache
    cache.set(cache_key, thumbnail_io.getvalue(), timeout=60*60*24) # cache for 24 hours

    return HttpResponse(thumbnail_io, content_type=f"image/webp")
    
