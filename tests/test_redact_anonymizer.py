import unittest
from hexanonyme.core.anonymizer.redact_anonymizer import RedactAnonymizer

class TestRedactAnonymizer(unittest.TestCase):

    def setUp(self):
        self.redact_anonymizer = RedactAnonymizer(entities=["PER", "ADDRESS"])

    def test_redact_names_and_addresses(self):
        input_text = "Mon nom est Jean Dupont. J'habite au 123 rue de la Ville, Paris."
        expected_output = "Mon nom est [REDACTED]. J'habite au [REDACTED]."
        redacted_text = self.redact_anonymizer.redact(input_text)
        self.assertEqual(redacted_text, expected_output)


if __name__ == '__main__':
    unittest.main()
