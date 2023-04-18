import layoutparser as lp

import string
from pprint import pprint

import cv2

import fileio
import ner

TEXT = "text"
ENTITIES = "entities"
OVERALL_SENTIMENT = "overall_sentiment"
ENTITY_SENTIMENT = "entity_sentiment"

GCV_PATH = "INSERT PATH TO GCV JSON HERE"


def process_many(
    images_path: str, save_json: str, overwrite: bool, show: bool, ner_actions: tuple
) -> None:
    # Get a list of all the images
    image_paths = fileio.get_image_paths(images_path)

    # Process each image
    for path in image_paths:
        print(f"Processing {path}...")
        process(path, save_json, overwrite, show, ner_actions)


def process(
    image_path: str, save_json: str, overwrite: bool, show: bool, ner_actions: tuple
) -> None:
    # Read the text in the image
    text = fileio.get(save_json, image_path, TEXT)
    if TEXT in ner_actions:
        # Avoid an API call if we can
        if overwrite or text is None:
            text = read_image(image_path, show)
        fileio.update(save_json, image_path, TEXT, text, overwrite)
    
    # Make sure there's text to process
    if text is None:
        return

    # Get the entities
    if ENTITIES in ner_actions:
        entities = ner.get_spacy_entities(text, show)
        fileio.update(save_json, image_path, ENTITIES, entities, overwrite)
    
    # Get the sentiment
    if OVERALL_SENTIMENT in ner_actions:
        sentiment = fileio.get(save_json, image_path, OVERALL_SENTIMENT)
        # Avoid an API call if we can
        if overwrite or sentiment is None:
            sentiment = ner.get_sentiment(text, show)
        fileio.update(save_json, image_path, OVERALL_SENTIMENT, sentiment, overwrite)
    
    # Get the entity sentiment
    if ENTITY_SENTIMENT in ner_actions:
        entity_sentiment = fileio.get(save_json, image_path, ENTITY_SENTIMENT)
        # Avoid an API call if we can
        if overwrite or entity_sentiment is None:
            entity_sentiment = ner.get_entity_sentiment(text, show)
        fileio.update(save_json, image_path, ENTITY_SENTIMENT, entity_sentiment, overwrite)


def read_image(image_path: str, show: bool) -> str:
    # Open the image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Set up OCR Agent and detect
    ocr_agent = lp.GCVAgent.with_credential(GCV_PATH, languages=["es"])
    res = ocr_agent.detect(image, return_response=True)
    text_boxes = ocr_agent.gather_text_annotations(res)
    text = clean_text(text_boxes)

    if show:
        print(text)

    return text


def clean_text(text_boxes) -> str:
    cleaned = ""
    for i in range(len(text_boxes)):
        situational_space = (
            " "
            if i != len(text_boxes) - 1
            and text_boxes[i + 1].text not in string.punctuation
            else ""
        )
        cleaned += text_boxes[i].text + situational_space
    return cleaned
