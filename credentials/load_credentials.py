import os
from .models import Credential

def load_from_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            print(f"Loading: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if ':' in line:
                        email, password = line.split(':', 1)
                        Credential.objects.update_or_create(email=email, defaults={'password': password})
