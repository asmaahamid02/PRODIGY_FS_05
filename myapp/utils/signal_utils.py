import os, shutil
from django.core.files.storage import default_storage
from django.db.models import FileField


def file_cleanup(instance, fieldname):
    image = getattr(instance, fieldname)

    if image:
        if hasattr(image, 'path') and os.path.exists(image.path):
            dir =image.path.rsplit('/', 1)[0]

            if os.path.exists(dir) and os.path.isdir(dir):
                shutil.rmtree(dir)         
