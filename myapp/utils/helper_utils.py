from uuid import uuid4
from datetime import datetime
import os, shutil

def generate_unique_folder_name() -> str:
    return f"{uuid4().hex[:6].upper()}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
def remove_image_file(image):
    if hasattr(image, 'path') and os.path.exists(image.path):
        dir = image.path.rsplit('/', 1)[0]

    if os.path.exists(dir) and os.path.isdir(dir):
        shutil.rmtree(dir)