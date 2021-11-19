import os
from urllib.parse import urlparse, unquote

def get_folder_n_child_from_uri(uri:str) -> tuple[str, str]:
    'Returns filename with extension from URI (parses to conventional path)'
    # print('Before split:', unquote(urlparse(uri).path))
    head, tail = os.path.split(parse_uri2path(uri))
    return head, tail

def is_file_or_folder_uri(uri:str) -> bool:
    path = parse_uri2path(uri)
    'Returns a boolean. True is a file, False is a folder'
    if os.path.isfile(path):
        return True
    elif os.path.isdir(path):
        return False

def parse_uri2path(uri:str) -> str:
    return unquote(urlparse(uri).path).strip('/')

def get_filepath_wo_ext(path:str)->str:
    "Extracts the path without the extension of the file"
    return os.path.splitext(path)[0]


if __name__ == '__main__':
    folder, child = get_folder_n_child_from_uri('file:///D:/coding/CuyTraductor/assets/logo.png')
    print('Parent folder path:', folder)
    print('Filename or child folder:', child)
    