import os
import json

import sys


IMAGE_NAME = "image_name"
CATEGORY = "category"


def update(json_path, image_path, key, value, overwrite=True):
    # Open the json file
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # If it doesn't exist, create a new entry
    if data.get(image_path) is None:
        image_name = image_path.split("/")[-1].split(".")[0]
        category = image_path.split("/")[-2]
        data[image_path] = {IMAGE_NAME: image_name, CATEGORY: category, key: value}

    # Otherwise, update the key/value if it doesn't exist or overwrite is True
    elif data[image_path].get(key) is None or overwrite:
        data[image_path][key] = value

    # Write back to file
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get(json_path, image_path, key: str = None):
    # Open the json file
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Get the text
    if key is None:
        return data.get(image_path)
    elif data.get(image_path) is not None:
        return data[image_path].get(key)
    
    return None


def get_image_paths(images_path: str) -> list:
    # Get a list of all the images
    extensions = (".jpg", ".jpeg", ".png")
    images = []
    for subdir, _, files in os.walk(images_path):
        for file in files:
            if file.lower().endswith(extensions):
                path = os.path.join(subdir, file).replace("\\", "/")
                images.append(path)
    return images