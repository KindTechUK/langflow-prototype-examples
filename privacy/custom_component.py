from langflow.custom import Component
from langflow.io import StrInput, Output
from langflow.schema import Data
from transformers import pipeline
from typing import List, Dict, Tuple
import numpy as np

# Define the custom component
class PrivacyAnonymizer(Component):
    display_name = "Privacy Anonymizer"
    description = "Anonymizes text by masking sensitive information."
    icon = "shield"
    name = "PrivacyAnonymizer"

    # Define inputs and outputs
    inputs = [
        StrInput(name="text", display_name="Input Text", info="Text to be anonymized")
    ]
    outputs = [
        Output(name="anonymized_text", display_name="Anonymized Text", method="anonymize")
    ]

    def anonymize(self) -> Data:
        """Anonymize the input text."""
        text = self.text
        result = self.anonymize_text(text)
        return Data(data={"anonymized_text": result['masked_text']})

    def anonymize_text(self, text: str, verbose: bool = True) -> Dict:
        """Anonymize a given text using the privacy pipeline."""
        if verbose:
            print(f"Anonymizing text: {text}")

        # Get token classification results
        pipe = pipeline("token-classification", model="ai4privacy/llama-ai4privacy-english-anonymiser-openpii", device="cpu")
        result = pipe(text)

        if verbose:
            print("Raw token classification results:")
            print(result)
            print("\n" + "="*50)

        # Run the anonymization pipeline
        anonymized_result = self.run_anonymization_pipeline(result, text)

        if verbose:
            print("="*50)
            print(f"\nFinal anonymized text: {anonymized_result['masked_text']}")

        return anonymized_result

    def run_anonymization_pipeline(self, token_results: List[Dict], original_text: str = None) -> Dict:
        """Main pipeline function that processes token results and returns anonymized text."""
        if original_text is None:
            raise ValueError("Original text is required for proper anonymization")

        # Process the results
        result = self.process_anonymization_results(token_results, original_text, threshold=0.3)

        return result

    def process_anonymization_results(self, token_results: List[Dict], original_text: str, threshold: float = 0.3) -> Dict:
        """Process the token prediction results and return anonymized text."""
        # Aggregate privacy tokens
        aggregated_groups = self.aggregate_privacy_tokens(token_results, threshold)

        # Mask the text
        masked_text, replacements = self.mask_text_with_original(token_results, aggregated_groups, original_text)

        return {
            'masked_text': masked_text,
            'replacements': replacements,
            'original_text': original_text
        }

    def aggregate_privacy_tokens(self, token_predictions: List[Dict], threshold: float = 0.3) -> List[Dict]:
        """Aggregate privacy tokens into groups based on the JavaScript logic."""
        aggregated = []
        i = 0
        n = len(token_predictions)

        while i < n:
            current_token = token_predictions[i]
            if current_token['word'] in ['[CLS]', '[SEP]']:
                i += 1
                continue

            starts_with_space = current_token['word'].startswith('Ġ')
            is_first_word = len(aggregated) == 0 and i == 0

            if starts_with_space or is_first_word:
                group = {
                    'tokens': [current_token],
                    'indices': [i],
                    'scores': [current_token['score']],
                    'starts_with_space': starts_with_space
                }
                i += 1

                while (i < n and 
                       not token_predictions[i]['word'].startswith('Ġ') and 
                       token_predictions[i]['word'] not in ['[CLS]', '[SEP]']):
                    group['tokens'].append(token_predictions[i])
                    group['indices'].append(i)
                    group['scores'].append(token_predictions[i]['score'])
                    i += 1

                if max(group['scores']) >= threshold:
                    aggregated.append(group)
            else:
                i += 1

        return aggregated

    def mask_text_with_original(self, token_predictions: List[Dict], aggregated_groups: List[Dict], original_text: str) -> Tuple[str, List[Dict]]:
        """Mask the original text by replacing sensitive tokens with placeholders."""
        replacements = []
        redacted_counter = 1
        masked_text = original_text

        sorted_groups = sorted(aggregated_groups, key=lambda g: g['tokens'][0]['start'])

        for group in reversed(sorted_groups):
            start_pos = group['tokens'][0]['start']
            end_pos = group['tokens'][-1]['end']

            original_group_text = original_text[start_pos:end_pos]

            placeholder = f"[PII_{redacted_counter}]"
            replacements.append({
                'original': original_group_text,
                'placeholder': placeholder,
                'activation': max(group['scores'])
            })

            masked_text = masked_text[:start_pos] + placeholder + masked_text[end_pos:]

            redacted_counter += 1

        return masked_text, replacements