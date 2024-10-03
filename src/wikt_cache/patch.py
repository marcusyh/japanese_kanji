import os
import json

def load_patch(patch_path='../data/wiktionary/patch.txt'):
    if not os.path.isfile(patch_path):
        return {}
    with open(patch_path) as file:
        patch = json.load(file)
        #print(patch)
    return patch


