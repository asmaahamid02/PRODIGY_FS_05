import os, shutil
from django.core.files.storage import default_storage
from django.db.models import FileField
from .helper_utils import remove_image_file


def file_cleanup(instance, fieldname):
    image = getattr(instance, fieldname)

    if image:
        remove_image_file(image)        
