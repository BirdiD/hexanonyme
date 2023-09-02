# hexanonyme
Hexanonyme is a python package for data anonymization in French  

My Package is a Python library designed to anonymize and de-anonymize personally identifiable information (PII) in French language text data. It provides a set of anonymization classes capable of replacing, redacting, or transforming PII entities within the text while preserving the text's structure.

## Features

- Anonymize PII entities such as names, addresses, dates, and more.
- Redact PII entities from the text, replacing them with placeholders.
- Restore redacted PII entities in a de-anonymized text for auditing or analysis purposes.

## Installation

You can install My Package using `pip`:

```bash
pip install my-package

# Usage

Here's a quick example of how to use My Package to anonymize and de-anonymize French text:

from my_package.core.anonymizer import ReplaceAnonymizer, RedactAnonymizer

# Initialize ReplaceAnonymizer
replace_anonymizer = ReplaceAnonymizer(entities=["PER", "DATE", "ADDRESS"])

# Anonymize PII entities
text = "Jean Dupont lives at 123 Rue de la République. He was born on 01-01-1980."
anonymized_text = replace_anonymizer.replace(text)

# De-anonymize the text
original_text = replace_anonymizer.deanonymize(anonymized_text)

# Initialize RedactAnonymizer
redact_anonymizer = RedactAnonymizer(entities=["PER", "ADDRESS"])

# Redact PII entities
text = "Jean Dupont lives at 123 Rue de la République."
redacted_text = redact_anonymizer.redact(text)

# De-anonymize the redacted text
restored_text = redact_anonymizer.deanonymize(redacted_text)
```

# Why Data Anonymization Matters
Data anonymization is crucial for protecting individuals' privacy and complying with data protection regulations. When training AI-based language models, it's vital to ensure that personally identifiable information (PII) is not exposed. This library allows you to prepare your data before providing it to large language models like ChatGPT by removing or replacing PII.

# How it works

My Package uses Camembert fine-tuned Named Entity Recognition (NER) models specifically tailored to French. The list of available entities currently includes:

PER (person names)
LOC (locations, cities, birthplaces)
DATE (birthdates)
ADDRESS (postal addresses)
These NER models accurately identify PII entities in French text.