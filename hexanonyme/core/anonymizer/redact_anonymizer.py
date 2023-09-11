from .base_anonymizer import BaseAnonymizer
import re

class RedactAnonymizer(BaseAnonymizer):
    def __init__(self, entities=None):
        super().__init__()
        self.classifier_filtres = self.load_pipelines()

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

        #Get entities from all classifiers
        for [classifier, filtre] in self.classifier_filtres:
            # Get entities from both models
            entities_classifier = classifier(text)
            # Merge overlapping entities
            entities_classifier = self.merge_overlapping_entities(entities_classifier)
            entities_classifier = [entity for entity in entities_classifier if entity["entity_group"] in filtre]
            entities_total += entities_classifier
            
        entities_total += self.find_telephone_number(text)
        entities_total += self.find_email(text)
        
        entities = self.drop_duplicates_and_included_entities(entities_total)

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
        if entity_type in ["ADDRESS", "PER", "DATE", "LOC", "ORG", "MISC", "TEL", "MAIL"]:
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

        for word in words:
            if '[REDACTED]' in word and entity_index < len(self.log_redactions):
                word = re.sub(r"\[REDACTED\]", (self.log_redactions[entity_index]['word']), word)
                entity_index += 1

        reconstructed_sentence = ' '.join(words)
        return reconstructed_sentence
