import os

def ensure_dir(file_path):
    """Assicura che la directory per il file esista."""
    directory = os.path.dirname(file_path)
    if directory: # Solo se directory non è una stringa vuota (es. file nella root)
        os.makedirs(directory, exist_ok=True)
