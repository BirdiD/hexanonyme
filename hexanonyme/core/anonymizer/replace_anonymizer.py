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
        self.classifier_filtres = self.load_pipelines()

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

        #Get entities from all classifiers
        entities_total = []
        for [classifier, filtre] in self.classifier_filtres:
            # Get entities from both models
            entities_classifier = classifier(text)
            # Merge overlapping entities
            entities_classifier = self.merge_overlapping_entities(entities_classifier)
            entities_classifier = [entity for entity in entities_classifier if entity["entity_group"] in filtre]
            entities_total += entities_classifier

        entities_total += self.find_telephone_number(text)
        entities_total += self.find_email(text)

        tokens = self.drop_duplicates_and_included_entities(entities_total)

        for entity_type in self.entities:
          if entity_type in ["ADDRESS", "PER", "DATE", "LOC", "ORG", "MISC", "TEL", "MAIL"]:
            text = self._replace_entities(text, tokens, entity_type)
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
            text = text.replace(replacement, original_word, 1)
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

    def _generate_random_org(self):
        """
        Generate a random name company the Faker library.

        Returns:
            str: A randomly generated company.
        """
        return self.fake.company()

    def _generate_random_per(self):
        """
        Generate a random name using the Faker library.

        Returns:
            str: A randomly generated name.
        """
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        full_name = f"{first_name} {last_name}"
        return full_name

    def _generate_random_misc(self):
        """
        Generate a random misc using the Faker library.

        Returns:
            str: A randomly generated misc.
        """
        words = self.fake.words()
        capitalized_words = [word.capitalize() for word in words]
        return ' '.join(capitalized_words)

    def _generate_random_tel(self):
        """
        Generate a random telephone number using the Faker library.

        Returns:
            str: A randomly telephone number.
        """
        return self.fake.phone_number()

    def _generate_random_mail(self):
        """
        Generate a random email using the Faker library.

        Returns:
            str: A randomly email.
        """
        return self.fake.ascii_free_email()

    def _get_faker_value(self, entity_type):
        """
        Generate a random faker entity_type value

        Args:
            entity_type (str): The entity type to be generated (PER, LOC, ADDRESS, DATE).

        Returns:
            str: The generated random faker value.
        """
        if entity_type in ["ADDRESS", "PER", "DATE", "LOC", "ORG", "MISC", "TEL", "MAIL"]:
            function = getattr(self,"_generate_random_{}".format(entity_type.lower()))
            return function()
        else:
            raise ValueError(f"Unsupported entity type: {entity_type}")