import json

def main(**kwargs):
    with open('tmp_dict.json', 'w') as file:
        json.dump(kwargs, file)
    