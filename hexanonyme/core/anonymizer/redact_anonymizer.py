from .base_anonymizer import BaseAnonymizer
import re

class RedactAnonymizer(BaseAnonymizer):
    def __init__(self, entities=None):
        super().__init__()
        self.per_loc_date_token_classifier, self.address_token_classifier = self.load_pipelines()

        if entities is not None:
          self.entities = entities

        # Log of removed PII entities
        self.log_redactions = []

    def redact(self, text):
        """
        Redact PII entities from the given text.

        Args:
            text (str): The input text to be anonymized.

        Returns:
            str: The text with PII entities redacted.
        """

        # Get entities from both models
        per_loc_date_entities = self.per_loc_date_token_classifier(text)
        address_date_entities = self.address_token_classifier(text)

        # Merge overlapping entities
        per_loc_date_entities = self.merge_overlapping_entities(per_loc_date_entities)
        address_date_entities = self.merge_overlapping_entities(address_date_entities)

        entities = self.drop_duplicates_and_included_entities(per_loc_date_entities + address_date_entities)
        # Redact specified entities in the text
        self.log_redactions = []

        for entity_type in self.entities:
            text, redacted_entities = self._redact_entities(text, entities, entity_type)
            self.log_redactions.extend(redacted_entities)

        self.log_redactions = sorted(self.log_redactions, key=lambda x: x['start'])
        return text

    def _redact_entities(self, text, entities, entity_type):
        """
        Redact specific entity type in the text.

        Args:
            text (str): The input text to be processed.
            entities (list): List of dictionaries containing entity information.

        Returns:
            str: The text with the specified entities redacted.
            list: List of removed PII entities with their positions and original values.
        """
        if entity_type in ["ADDRESS", "PER", "DATE", "LOC"]:
          entities = [entity for entity in entities if entity["entity_group"]==entity_type]
          redacted_entities = []

          #print(f"Filter entities in _redact_entities function for {entity_type} is {entities}")
          for entity in entities:
              start = entity["start"]
              end = entity["end"]
              word = entity["word"]
              entity_group = entity["entity_group"]

              # Replace the entity with a redaction marker (e.g., "[REDACTED]")
              text = re.sub(word, "[REDACTED]", text)
              #print(f"Entity {word} has been removed from text and result is {text}")

              # Log the removed PII entity
              redacted_entities.append({"entity_group": entity_group, "word": word, "start": start, "end": end})

          return text, redacted_entities

        else:
          raise ValueError(f"Unsupported entity type: {entity_type}")


    def deanonymize(self, redacted_text):
        """
        Restore original PII entities to the redacted text using redactions.

        Args:
            redacted_text (str): The redacted text to be deanonymized.

        Returns:
            str: The deanonymized text with removed values restored.
        """

        entity_index = 0

        words = redacted_text.split()

        for i in range(len(words)):
            if '[REDACTED]' in words[i] and entity_index < len(self.log_redactions):
                words[i] = re.sub(r"\[REDACTED\]", (self.log_redactions[entity_index]['word']), words[i])
                entity_index += 1

        reconstructed_sentence = ' '.join(words)
        return reconstructed_sentence