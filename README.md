# Hexanonyme
Hexanonyme is a Python library designed to anonymize and de-anonymize personally identifiable information (PII) in French language text data. It provides a set of anonymization classes capable of replacing, redacting, or transforming PII entities within the text while preserving the text's structure.

## Features

- Anonymize PII entities such as names, addresses, dates, and more.
- Redact PII entities from the text, replacing them with placeholders.
- Restore redacted PII entities in a de-anonymized text for auditing or analysis purposes.

## Installation

You can install Hexanonyme using `pip`:

```
pip install hexanonyme
```

# Usage

Here's a quick example of how to use hexanonyme to anonymize and de-anonymize French text:

```python
# Import anonymizer
from hexanonyme import ReplaceAnonymizer, RedactAnonymizer
```
## ReplaceAnoymizer

The replace anonymizer can take the following arguments 
- entities : List of entity types to be anonymized. Default values are: `["PER", "LOC", "DATE", "ADDRESS"]`.
- faker (bool): Whether to use Faker library for fake data generation (default: `True`). For instance if entities list is  ["PER", "LOC"], fakes names and cities will be generated and used to replaced the entities in the original text.
- replacement_dict : Dictionary of replacement values for specific entity types . If faker argument is set to `False`, you can supply a dictionary for you entity replacement. For instance `{"PER" : "Jean Pierre", "LOC" : "Marseille"}` will replace all PER and LOC entities by respectively **Jean Pierre** and **Marseille**. 

If replacement_dict is not supplied and faker is set to `False`, a default dict will be used: `{'entity_type' : '<entity_type>'}`. 

### Example 1 

```python
# Initialize ReplaceAnonymizer
replace_anonymizer = ReplaceAnonymizer()

# Anonymize PII entities
text = "Je réside au 11 impasse de la défense 75018 Paris. Je m'appelle Amel Douc. J'habite à Bordeaux. Je suis né le 29/12/2021."
anonymized_text = replace_anonymizer.replace(text)
print(anonymized_text)
"Je réside au 7, rue Virginie Morel 48649 Le Rouxboeuf. Je m'appelle Dominique Roux. J'habite à Guilbert. Je suis né le 18-09-1992."

# Deanonymize and restore original text
restored_text = replace_anonymizer.deanonymize(anonymized_text)
print(restored_text)
"Je réside au 11 impasse de la défense 75018 Paris. Je m'appelle Amel Douc. J'habite à Bordeaux. Je suis né le 29/12/2021."
```

### Example 2

```python
# Initialize ReplaceAnonymizer
replace_anonymizer = ReplaceAnonymizer(faker=True)

# Anonymize PII entities
text = "Je réside au 11 impasse de la défense 75018 Paris. Je m'appelle Amel Douc. J'habite à Bordeaux. Je suis né le 29/12/2021."
anonymized_text = replace_anonymizer.replace(text)
print(anonymized_text)
"Je réside au <ADDRESS>. Je m'appelle <PER>. J'habite à <LOC>. Je suis né le <DATE>."

# Deanonymize and restore original text
restored_text = replace_anonymizer.deanonymize(anonymized_text)
```

## RedactAnonymizer

Contrary to the replace anonymizer, the redact anonymizer takes only one argument (the list of entities) 
- entities : List of entity types to be anonymized. Default values are: `["PER", "LOC", "DATE", "ADDRESS", "ORG", "MISC"]`.

```python
# Initialize ReplaceAnonymizer
redact_anonymizer = RedactAnonymizer(["PER", "ADDRESS"])

# REDACT PII entities
text = "Mon nom est Jean Dupont. J'habite au 123 rue de la Ville, Paris."
redacted_text = redact_anonymizer.replace(text)

print(anonymized_text)
"Mon nom est [REDACTED]. J'habite au [REDACTED]."

# Deanonymize and restore original text
restored_text = redact_anonymizer.deanonymize(redacted_text)
```

## Note

When you provide a list of entities that contains address, make sure address is the first element of the list. Postal addresses may contain some PER or LOC as in the exemple below : `J'habite au 10 rue Victor Hugo, Paris`. To avoid the model considering Victor Hugo as seperate entity from address, add the latter in the first position of the list.

# Why Data Anonymization Matters
Data anonymization is crucial for protecting individuals' privacy and complying with data protection regulations. When training AI-based language models, it's vital to ensure that personally identifiable information (PII) is not exposed. This library allows you to prepare your data before providing it to large language models like ChatGPT by removing or replacing PII.

# How it works

**Hexanonyme** uses **Camembert** language model fine-tuned Named Entity Recognition (NER) tasks. Two finetuned models are used. The models can be found on [Hugging Face](https://huggingface.co/DioulaD) : The list of available entities currently includes:

- PER (person names)
- LOC (locations, cities, birthplaces)
- DATE (birthdates)
- ADDRESS (postal addresses)
- ORG (organisation)
- MISC (films, series)

These NER models accurately identify PII entities in French text.

# Contributions
Contributions are welcomed. If you'd  like to add new anonymization classes or support additional types of entities, follow these steps:
- Fork the repository
- Create a new branch for your feature 
- Make your changes and ensure the tests pass
- Updated the documentation as needed
- Submit a pull request