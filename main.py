from pprint import pprint

import reader
import display


IMAGES_PATH = "projects/image_reader/images/"
JSON_PATH = "projects/image_reader/config/data.json"


if __name__ == "__main__":
    # Get a list TextBlock objects
    reader.process_many(
        IMAGES_PATH,
        JSON_PATH,
        overwrite=False,
        show=False,
        ner_actions=(
            reader.TEXT,
            reader.OVERALL_SENTIMENT,
            reader.ENTITY_SENTIMENT,
        ),
    )

    # display.overall_sentiment_bar_graph(JSON_PATH, show=False)
    # display.get_top_magnitudes(JSON_PATH, show=True)
