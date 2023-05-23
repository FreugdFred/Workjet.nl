from flask import request

import inspect
import json


def get_json_language():
    file_name = inspect.stack()[1].filename.split('/')[-1].split('.')[0]
    language_cookie = request.cookies.get('language') or 'NL'
    
    with open(f'website/languages/{file_name}/{language_cookie}.json', 'r') as f:
        language_dict = json.load(f)

    return language_dict | get_base_json(language_cookie)


def get_base_json(language_cookie):
    with open(f'website/languages/Base/{language_cookie}.json', 'r') as f:
        language_base_dict = json.load(f)
        
    return language_base_dict
    