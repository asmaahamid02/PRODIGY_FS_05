from PIL import Image
import os
from io import BytesIO
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files import File

allowed_formats = ('png', 'jpg', 'webp')

def create_thumbnails(path: str, sizes: list[tuple[int, ...]], format: str = 'webp') -> dict[str, str]:
    if not path or len(sizes) == 0:
        return {"status": "fail", "message": "The path of the images and the needed sized are required"}
    
    format = format.lower()

    if format not in allowed_formats:
        return {"status": "fail", "message": f"'{format}' format is not allowed"}
    
    original_image = Image.open(path)
    image_name, image_extension = os.path.splitext(os.path.basename(path))
    image_path = os.path.dirname(path)

    counter = 0

    for size in sizes:
        if len(size) < 1:
            continue

        width, height = _get_dimensions(size, original_image)

        thumbnail_name = f"{image_name}_{width}x{height}.{format}"
        thumbnail_path = os.path.join(image_path, thumbnail_name)

        thumbnail_image = original_image.copy()
        thumbnail_image.thumbnail((width, height), Image.Resampling.LANCZOS)
        thumbnail_image.save(thumbnail_path, format, quality=90, optimize=True)

        counter += 1       

    if counter > 0:        
        return {"status": "success", "message": f"{counter} thumbnails were created for '{image_name}{image_extension}' image"}        
    
    return {"status": "fail", "message": f"An error occurred while creating thumbnails for '{image_name}{image_extension}' image!"}        
    
def resize_image(image, size: tuple[int, int] = (800,), format:str = 'webp') -> File | dict[str, str]:  
    format = format.lower()

    if format not in allowed_formats:
        return {"status": "fail", "message": f"'{format}' format is not allowed"}
    
    original_image = Image.open(image)
    width, height = _get_dimensions(size, original_image)

    original_image.thumbnail((width, height))

    image_io = BytesIO()
    original_image.save(image_io, format, quality=90)
    new_image = File(image_io, name=image.name)

    return new_image
    
def validate_image_size(image, max_size:int = 5) -> None | ValidationError: # in MB
    limit = max_size * 1024 * 1024

    if image.size > limit:
        return ValidationError(f"Image size should not exceed {max_size}MB")
        
def _get_dimensions(size: tuple[int, int], original_image: Image) -> tuple[int, int]:
    width = size[0]
    height = size[1] if len(size) > 1 else None

    # if no heigh is provided, calculate it based on the width (maintain the aspect ratio) 
    if height is None:
        height = int(original_image.height * (width / original_image.width))

    return (width, height)
        