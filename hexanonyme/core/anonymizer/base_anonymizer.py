from transformers import pipeline
import re

class BaseAnonymizer:
    def __init__(self):
        self.entities = ["ADDRESS", "PER", "LOC", "DATE", "ORG", "MISC", "TEL", "MAIL"]

    def load_pipelines(self):
        self.models = ["Jean-Baptiste/camembert-ner-with-dates",
                       "DioulaD/birdi-finetuned-ner",
                       "DioulaD/birdi-finetuned-ner-address-v2"]
        self.filters = [
                        ['ORG', 'MISC','DATE'],
                        ["ADDRESS", "PER", "LOC", "DATE", "ORG", "MISC", "TEL", "MAIL"],
                        ["ADDRESS", "PER", "LOC", "DATE", "ORG", "MISC", "TEL", "MAIL"]
                       ]

        #We iterate on every model to create a list of classifier
        n = len(self.models)
        liste_classifier_filters = []
        for i in range(n):
            classifier = pipeline(
                "token-classification",
                model = self.models[i],
                aggregation_strategy = "simple"
            )
            liste_classifier_filters.append([classifier,self.filters[i]])
        return liste_classifier_filters

    def merge_overlapping_entities(self, entities):
        """
        Merge overlaps over one entity.
        In some cases a person name like "Cecile Da Costa." can be identified as two PER entities bacause of the formating of the text and what comes before

        Args:
            entities (list): A list of dictionaries, where each dictionary represents an entity.

        Returns:
            list: A list of dictionaries, where overlaps entities are grouped together
        """
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

    def find_telephone_number(self, text):
        entities = []
        multiples_regex_formats = ["((?:(?:\+|00)33[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2}))"]
        for regex_format in multiples_regex_formats:
            all_matchs = re.findall(regex_format, text)
            for match in all_matchs:
                entity = {
                    "entity_group": "TEL",
                    "score": 1,
                    "word": match,
                    "start": text.index(match),
                    "end": text.index(match) + len(match)
                }
                entities.append(entity)
        return entities

    def find_email(self, text):
        entities = []
        multiples_regex_formats = ["([a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*)"]
        for regex_format in multiples_regex_formats:
            all_matchs = re.findall(regex_format, text)
            for match in all_matchs:
                entity = {
                    "entity_group": "MAIL",
                    "score": 1,
                    "word": match,
                    "start": text.index(match),
                    "end": text.index(match) + len(match)
                }
                entities.append(entity)
        return entities

    def drop_duplicates_and_included_entities(self, list_of_dicts):
        """
        Drop duplicate entities and entities included in other entities from a list of dictionaries.

        Args:
            list_of_dicts (list): A list of dictionaries, where each dictionary represents an entity.

        Returns:
            list: A list of dictionaries, where duplicate entities and entities included in other entities have been dropped.
        """

        # Sort the list by 'start' position
        list_of_dicts = sorted(list_of_dicts, key=lambda x: x['start'])

        # Define a function to check if one entity is included in another
        def is_included(entity1, entity2):
            return entity1['start'] >= entity2['start'] and entity1['end'] <= entity2['end']

        # Initialize a variable to keep track of whether changes were made
        changes_made = True

        # Continue processing until no more changes are made
        while changes_made:
            changes_made = False
            i = 0

            while i < len(list_of_dicts):
                current_entity = list_of_dicts[i]

                # Check if the current entity is included in another
                for j in range(i + 1, len(list_of_dicts)):
                    if is_included(current_entity, list_of_dicts[j]):
                        # Remove the current entity from the list
                        list_of_dicts.pop(i)
                        changes_made = True
                        break
                    elif is_included(list_of_dicts[j], current_entity):
                        # Remove the other entity (j) if it's included in the current entity
                        list_of_dicts.pop(j)
                        changes_made = True
                        break
                else:
                    i += 1

        return list_of_dicts
