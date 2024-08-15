from uuid import uuid4
from datetime import datetime

def generate_unique_folder_name() -> str:
    return f"{uuid4().hex[:6].upper()}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    