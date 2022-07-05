from zipfile import ZipFile
import os

def zip_repo_code():

    file_paths = []
    exclude = set({".git", "__pycache__", ".venv", "cdk.out", "zip_file_code"})
    for root, directories, files in os.walk(os.path.dirname('./')):
        directories[:] = [d for d in directories if d not in exclude]
        
        for filename in files:
            file_paths.append(os.path.join(root, filename))

    with ZipFile('tensor_generic_backend.zip', 'w') as zip:
        for file in file_paths:
            zip.write(file)
