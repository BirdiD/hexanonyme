from transformers import pipeline


class BaseAnonymizer:
    def __init__(self):
        self.entities = ["ADDRESS", "PER", "LOC", "DATE"]

    def load_pipelines(self):
        model_per_loc_date_checkpoint = "DioulaD/birdi-finetuned-ner"
        model_address_checkpoint = "DioulaD/birdi-finetuned-ner-address-v2"

        per_loc_date_token_classifier = pipeline(
            "token-classification",
            model=model_per_loc_date_checkpoint,
            aggregation_strategy="simple"
        )
        address_token_classifier = pipeline(
            "token-classification",
            model=model_address_checkpoint,
            aggregation_strategy="simple"
        )
        return per_loc_date_token_classifier, address_token_classifier

    def merge_overlapping_entities(self, entities):
        merged_entities = []
        i = 0
        while i < len(entities):
            entity = entities[i]
            j = i + 1
            while j < len(entities) and entity["entity_group"] == entities[j]["entity_group"] and entity["end"] == entities[j]["start"]:
                entity = {
                    "entity_group": entity["entity_group"],
                    "score": max(entity["score"], entities[j]["score"]),
                    "word": entity["word"] + entities[j]["word"],
                    "start": entity["start"],
                    "end": entities[j]["end"]
                }
                j += 1
            merged_entities.append(entity)
            i = j
        return merged_entities

    def drop_duplicates_and_included_entities(self, list_of_dicts):
        """
        Drop duplicate entities and entities included in other entities from a list of dictionaries.

        Args:
            list_of_dicts (list): A list of dictionaries, where each dictionary represents an entity.

        Returns:
            list: A list of dictionaries, where duplicate entities and entities included in other entities have been dropped.
        """

        list_of_dicts = sorted(list_of_dicts, key=lambda x: x['start'])

        for i, dict in enumerate(list_of_dicts):
            if i > 0 and dict['start'] >= list_of_dicts[i - 1]['start'] and dict['end'] <= list_of_dicts[i - 1]['end']:
                del list_of_dicts[i]
                continue

            if i > 0 and dict['entity_group'] == list_of_dicts[i - 1]['entity_group'] and dict['word'] == list_of_dicts[i - 1]['word']:
                del list_of_dicts[i]
                continue

        return list_of_dicts