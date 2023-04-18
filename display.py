import json

import pandas as pd
import matplotlib.pyplot as plt

from pprint import pprint

import sys


MODIFIER = 10.0
MIN_MAGNITUDE = 1.0
MAPPINGS = {
    "DV-20Apr": "Diario Vea",
    "EN-20Apr": "El Nacional",
    "TC-20Apr2017": "Tal Cual",
    "UN-20Apr": "Ultimas Noticias",
}

# TODO: Holy shit clean up your panic code please goddamn fuck


def sentiment_bar_graph(name: str, json_path: str, show: bool = False):
    sentiments = get_sentiments_by_name(name, json_path, show)
    df = entity_sentiments_to_dataframe(sentiments)
    # df = df.groupby(["entity", "sentiment"]).count()
    # df = df.groupby(["category", "sentiment"]).count()
    # print(df)
    # df = df.reset_index()
    # df = df.pivot(index="category", columns="sentiment", values="image_name")
    df = df.drop(columns=["image_name", "entity"])
    df = df.groupby("category", as_index=False).mean()
    # Normalize the magnitude between 0 and 1
    df["magnitude"] = df["magnitude"] / MODIFIER
    # print(df.columns)
    # sys.exit(0)
    # df.plot.bar(stacked=True)
    # color = [{s<0.0: "red", s>=0.0: "green"}[True] for s in df["sentiment"]]
    # print(df["sentiment"])
    df.plot(
        title=name,
        kind="bar",
        x="category",
        y=["sentiment", "magnitude"],
        rot=0,
        # color=color,
        # c="magnitude",
        # norm=norm,
        # colormap="viridis",
    )
    # df.groupby(["category", "sentiment"]).count().unstack().plot.bar(stacked=True)
    # df.groupby("category").nunique().plot.bar(stacked=True)
    plt.legend(["sentiment", f"magnitude / {MODIFIER}"], loc="upper left")
    plt.axhline(y=0, color="black", linestyle="-")
    plt.show()


def overall_sentiment_bar_graph(json_path: str, show: bool = False):
    # Get the overall sentiment of all images
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    sentiments = []
    for _, image_data in data.items():
        image_name = image_data["image_name"]
        image_category = MAPPINGS[image_data["category"]]
        sentiments.append(
            (
                image_name,
                image_category,
                image_data["overall_sentiment"]["sentiment"],
                image_data["overall_sentiment"]["magnitude"],
            )
        )
    pprint(sentiments)
    df = overall_sentiments_to_dataframe(sentiments)
    df = df.drop(columns=["image_name"])
    df = df.groupby("category", as_index=False).mean()
    # Normalize the magnitude between 0 and 1
    df["magnitude"] = df["magnitude"] / MODIFIER
    df.plot(
        title="Overall sentiment",
        kind="bar",
        x="category",
        y=["sentiment", "magnitude"],
        rot=0,
    )
    plt.legend(["sentiment", f"magnitude / {MODIFIER}"], loc="upper left")
    plt.axhline(y=0, color="black", linestyle="-")
    plt.show()


def get_sentiments_by_name(name: str, json_path: str, show: bool = False):
    # Browse the json file for the name
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    sentiments = []
    for _, image_data in data.items():
        for entity_type in image_data["entity_sentiment"]:
            # if entity_type != "PERSON":
            #     continue
            for entity in image_data["entity_sentiment"][entity_type]:
                if name.lower() in entity.lower():
                    image_name = image_data["image_name"]
                    # image_category = image_data["category"]
                    image_category = MAPPINGS[image_data["category"]]
                    entity_data = image_data["entity_sentiment"][entity_type][entity]
                    sentiments.append(
                        (
                            image_name,
                            image_category,
                            entity,
                            entity_data["sentiment"],
                            entity_data["magnitude"],
                        )
                    )
    if show:
        pprint(sentiments)
    return sentiments


def get_top_magnitudes(json_path: str, show: bool = False):
    # Get the top magnitudes from a given json file
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    magnitudes = []
    for _, image_data in data.items():
        for entity_type in image_data["entity_sentiment"]:
            for entity in image_data["entity_sentiment"][entity_type]:
                image_category = MAPPINGS[image_data["category"]]
                entity_data = image_data["entity_sentiment"][entity_type][entity]
                if entity_data["magnitude"] < MIN_MAGNITUDE:
                    continue
                magnitudes.append(
                    (
                        image_category,
                        entity,
                        entity_data["sentiment"],
                        entity_data["magnitude"],
                    )
                )
    magnitudes.sort(key=lambda x: x[-1], reverse=True)
    if show:
        pprint(magnitudes)
    return magnitudes


def entity_sentiments_to_dataframe(sentiments: list):
    df = pd.DataFrame(
        sentiments,
        columns=["image_name", "category", "entity", "sentiment", "magnitude"],
    )
    return df


def overall_sentiments_to_dataframe(sentiments: list):
    df = pd.DataFrame(
        sentiments,
        columns=["image_name", "category", "sentiment", "magnitude"],
    )
    return df
