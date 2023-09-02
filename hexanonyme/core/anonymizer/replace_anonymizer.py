from .base_anonymizer import BaseAnonymizer
from faker import Faker
import re


class ReplaceAnonymizer(BaseAnonymizer):
    """
    Anonymizes PII data in text by replacing entities with fake or specified values.

    Args:
        entities (list): List of entity types to be anonymized (default: ["PER", "LOC", "DATE", "ADDRESS"]).
        faker (bool): Whether to use Faker library for fake data generation (default: True).
        replacement_dict (dict): Dictionary of replacement values for specific entity types (default: {}).

    Attributes:
        log_replacements (list): List of tuples containing original words and their replacements.
    """

    def __init__(self, entities=None, faker=True, replacement_dict=None):
        super().__init__()
        self.faker = faker
        self.replacement_dict = replacement_dict or {}
        self.per_loc_date_token_classifier, self.address_token_classifier = self.load_pipelines()

        if entities is not None:
          self.entities = entities

        fake_seed = 123
        Faker.seed(fake_seed)
        self.fake = Faker('fr_FR')

        self.log_replacements = []


    def replace(self, text):
        """
        Replace entities in the given text with fake or specified values.

        Args:
            text (str): The input text to be anonymized.

        Returns:
            str: The anonymized text with entities replaced.
        """

        # Clear log_replacements before each run
        self.log_replacements = []

        # Get entities from both models
        per_loc_date_entities = self.per_loc_date_token_classifier(text)
        address_date_entities = self.address_token_classifier(text)

        # Merge overlapping entities
        per_loc_date_entities = self.merge_overlapping_entities(per_loc_date_entities)
        address_date_entities = self.merge_overlapping_entities(address_date_entities)


        for entity_type in self.entities:
          if entity_type == "PER" and per_loc_date_entities:
            text = self._replace_entities(text, per_loc_date_entities, entity_type)
          elif entity_type == "ADDRESS" and address_date_entities:
            text = self._replace_entities(text, address_date_entities, entity_type)
          elif entity_type == "LOC" and per_loc_date_entities:
            text = self._replace_entities(text, per_loc_date_entities, entity_type)
          elif entity_type == "DATE":
            text = self._replace_entities(text, per_loc_date_entities + address_date_entities, entity_type)
          else:
            raise ValueError(f"Unsupported entity type: {entity_type}")

        return text

    def _replace_entities(self, text, entities, entity_type):
        """
        Replace specific entity type in the text with a replacement value.

        Args:
            text (str): The input text to be processed.
            entities (list): List of dictionaries containing entity information.

        Returns:
            str: The text with the specified entities replaced by the corresponding replacement values.
        """
        # Replace only supplied entity_type values

        entities = [entity for entity in entities if entity["entity_group"]==entity_type]
        for entity in entities:
            word = entity["word"]
            if self.faker:
                replacement_value = self._get_faker_value(entity["entity_group"])
            else:
                replacement_value = self.replacement_dict.get(entity["entity_group"], f"<{entity['entity_group']}>")

            # Use regex to replace the word
            text = re.sub(word, replacement_value, text)

            self.log_replacements.append((word, replacement_value))

        return text

    def deanonymize(self, text):
        """
        Restore original words from the log of replacements in the given text.

        Args:
            text (str): The anonymized text to be deanonymized.

        Returns:
            str: The deanonymized text with replaced values restored.
        """
        for original_word, replacement in self.log_replacements:
            text = text.replace(replacement, original_word, 1)  # Replace only the first occurrence
        return text

    def _generate_random_loc(self):
        """
        Generate a random location using the Faker library.

        Returns:
            str: A randomly generated location.
        """
        return self.fake.city()

    def _generate_random_date(self):
        """
        Generate a random date using the Faker library.

        Returns:
            str: A randomly generated date.
        """
        return self.fake.date(pattern="%d-%m-%Y")

    def _generate_random_address(self):
        """
        Generate a random address using the Faker library.

        Returns:
            str: A randomly generated address.
        """
        return self.fake.address()

    def _generate_random_name(self):
        """
        Generate a random name using the Faker library.

        Returns:
            str: A randomly generated name.
        """
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        full_name = f"{first_name} {last_name}"
        return full_name

    def _get_faker_value(self, entity_type):
        """
        Generate a random faker entity_type value

        Args:
            entity_type (str): The entity type to be generated (PER, LOC, ADDRESS, DATE).

        Returns:
            str: The generated random faker value.
        """
        if entity_type == "PER":
            return self._generate_random_name()
        elif entity_type == "LOC":
            return self._generate_random_loc()
        elif entity_type == "DATE":
            return self._generate_random_date()
        elif entity_type == "ADDRESS":
            return self._generate_random_address()
        else:
            raise ValueError(f"Unsupported entity type: {entity_type}")
