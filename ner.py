import numpy as np

import spacy
from spacy import displacy

from google.cloud import language_v1

from pprint import pprint


GCNL_PATH = "INSERT PATH TO GCNL JSON HERE"


def get_spacy_entities(text: str, show: bool):
    # Parse the doc
    doc = parse_doc(text)

    # Return the entities for a JSON
    entities = {}
    for entity in doc.ents:
        if entities.get(entity.label_) is None:
            entities[entity.label_] = [entity.text]
        elif entity.text not in entities[entity.label_]:
            entities[entity.label_].append(entity.text)

    if show:
        pprint(entities)
    return entities


def get_sentiment(text: str, show: bool):
    client, document = get_client_and_doc(text)

    response = client.analyze_sentiment(
        request={"document": document, "encoding_type": language_v1.EncodingType.UTF8}
    )
    sentiment = {
        "sentiment": np.around(response.document_sentiment.score, 2),
        "magnitude": np.around(response.document_sentiment.magnitude, 2),
    }

    if show:
        pprint(sentiment)
    return sentiment


def get_entity_sentiment(text: str, show: bool):
    client, document = get_client_and_doc(text)

    response = client.analyze_entity_sentiment(
        request={"document": document, "encoding_type": language_v1.EncodingType.UTF8}
    )

    entities = {}
    for entity in response.entities:
        entity_type = entity.type_.name
        if entity_type not in entities:
            entities[entity_type] = {}
        json_entity = {
            "salience": np.around(entity.salience, 4),
            "sentiment": np.around(entity.sentiment.score, 2),
            "magnitude": np.around(entity.sentiment.magnitude, 2),
        }
        entities[entity_type][entity.name] = json_entity

    if show:
        pprint(entities)
    return entities


def parse_doc(text: str):
    nlp = spacy.load("es_core_news_lg")
    doc = nlp(text)
    return doc


def get_client_and_doc(text: str):
    client = language_v1.LanguageServiceClient.from_service_account_json(GCNL_PATH)

    document = {
        "content": text,
        "type_": language_v1.Document.Type.PLAIN_TEXT,
        "language": "es",
    }

    return client, document


def display(doc: spacy.tokens.doc.Doc):
    return displacy.serve(doc, style="ent")
