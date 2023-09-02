import unittest
from hexanonyme.core.anonymizer.replace_anonymizer import ReplaceAnonymizer

class TestReplaceAnonymizer(unittest.TestCase):

    def test_replace_with_faker(self):
        # Initialize the anonymizer with faker=True
        anonymizer = ReplaceAnonymizer(entities=["PER"], faker=True)

        # Test text with a person's name
        text = "Bonjour, je m'appelle John Doe."
        anonymized_text = anonymizer.replace(text)

        # Ensure the person's name is replaced with a fake name
        self.assertNotEqual(text, anonymized_text)
        self.assertTrue(anonymized_text.startswith("Bonjour, je m'appelle "))

    def test_replace_with_replacement_dict(self):
        # Initialize the anonymizer with a replacement dictionary
        replacement_dict = {"PER": "John Smith"}
        anonymizer = ReplaceAnonymizer(entities=["PER"], faker=False, replacement_dict=replacement_dict)

        # Test text with a person's name
        text = "Bonjour, je m'appelle John Doe."
        anonymized_text = anonymizer.replace(text)

        # Ensure the person's name is replaced with the specified replacement
        self.assertNotEqual(text, anonymized_text)
        self.assertEqual(anonymized_text, "Bonjour, je m'appelle John Smith.")

    def test_deanonymize(self):
        # Initialize the anonymizer with faker=True
        anonymizer = ReplaceAnonymizer(entities=["PER"], faker=True)

        # Test text with a person's name
        text = "Bonjour, je m'appelle John Doe."
        anonymized_text = anonymizer.replace(text)

        # Deanonymize the text
        deanonymized_text = anonymizer.deanonymize(anonymized_text)

        # Ensure the deanonymized text matches the original text
        self.assertEqual(text, deanonymized_text)

    def test_replace_multiple_entity_types(self):
        anonymizer = ReplaceAnonymizer(entities=["PER", "LOC"], faker=False)

        text = "John Doe habite à Paris."
        anonymized_text = anonymizer.replace(text)

        self.assertNotEqual(text, anonymized_text)
        self.assertTrue(anonymized_text.startswith("<PER> habite à <LOC>."))

if __name__ == '__main__':
    unittest.main()
