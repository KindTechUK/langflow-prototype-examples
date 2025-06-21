# Use a pipeline as a high-level helper
from transformers import pipeline
import re
from typing import List, Dict, Tuple
import numpy as np

def softmax(logits: List[float]) -> List[float]:
    """Compute softmax probabilities from logits."""
    exp_logits = [np.exp(x) for x in logits]
    sum_exp = sum(exp_logits)
    return [exp / sum_exp for exp in exp_logits]

def aggregate_privacy_tokens(token_predictions: List[Dict], threshold: float = 0.3) -> List[Dict]:
    """
    Aggregate privacy tokens into groups based on the JavaScript logic.
    
    Args:
        token_predictions: List of token prediction dictionaries
        threshold: Minimum score threshold for privacy detection
    
    Returns:
        List of aggregated token groups
    """
    aggregated = []
    i = 0
    n = len(token_predictions)
    
    while i < n:
        current_token = token_predictions[i]
        if current_token['word'] in ['[CLS]', '[SEP]']:
            i += 1
            continue
            
        starts_with_space = current_token['word'].startswith('Ġ')  # HuggingFace tokenizer uses 'Ġ' for space
        is_first_word = len(aggregated) == 0 and i == 0
        
        if starts_with_space or is_first_word:
            group = {
                'tokens': [current_token],
                'indices': [i],
                'scores': [current_token['score']],
                'starts_with_space': starts_with_space
            }
            i += 1
            
            # Continue adding tokens until we hit a space or special token
            while (i < n and 
                   not token_predictions[i]['word'].startswith('Ġ') and 
                   token_predictions[i]['word'] not in ['[CLS]', '[SEP]']):
                group['tokens'].append(token_predictions[i])
                group['indices'].append(i)
                group['scores'].append(token_predictions[i]['score'])
                i += 1
                
            # Only add group if max score meets threshold
            if max(group['scores']) >= threshold:
                aggregated.append(group)
        else:
            i += 1
            
    return aggregated

def mask_text_with_original(token_predictions: List[Dict], aggregated_groups: List[Dict], original_text: str) -> Tuple[str, List[Dict]]:
    """
    Mask the original text by replacing sensitive tokens with placeholders.
    
    Args:
        token_predictions: List of token prediction dictionaries
        aggregated_groups: List of aggregated token groups to mask
        original_text: The complete original text
    
    Returns:
        Tuple of (masked_text, replacements)
    """
    replacements = []
    redacted_counter = 1
    masked_text = original_text
    
    # Sort groups by their position in the original text (start position)
    sorted_groups = sorted(aggregated_groups, key=lambda g: g['tokens'][0]['start'])
    
    # Process groups in reverse order to avoid position shifting
    for group in reversed(sorted_groups):
        # Get the text span for this group
        start_pos = group['tokens'][0]['start']
        end_pos = group['tokens'][-1]['end']
        
        # Extract the original text for this group
        original_group_text = original_text[start_pos:end_pos]
        
        # Create placeholder
        placeholder = f"[PII_{redacted_counter}]"
        replacements.append({
            'original': original_group_text,
            'placeholder': placeholder,
            'activation': max(group['scores'])
        })
        
        # Replace in the masked text
        masked_text = masked_text[:start_pos] + placeholder + masked_text[end_pos:]
        
        redacted_counter += 1
    
    return masked_text, replacements

def process_anonymization_results(token_results: List[Dict], original_text: str, threshold: float = 0.3) -> Dict:
    """
    Process the token prediction results and return anonymized text.
    
    Args:
        token_results: List of token prediction dictionaries from the model
        original_text: Original input text
        threshold: Minimum score threshold for privacy detection
    
    Returns:
        Dictionary containing masked_text and replacements
    """
    # Aggregate privacy tokens
    aggregated_groups = aggregate_privacy_tokens(token_results, threshold)
    
    # Mask the text
    masked_text, replacements = mask_text_with_original(token_results, aggregated_groups, original_text)
    
    return {
        'masked_text': masked_text,
        'replacements': replacements,
        'original_text': original_text
    }

def run_anonymization_pipeline(token_results: List[Dict], original_text: str = None) -> Dict:
    """
    Main pipeline function that processes token results and returns anonymized text.
    
    Args:
        token_results: List of token prediction dictionaries from the model
        original_text: Original input text (required for proper masking)
    
    Returns:
        Dictionary containing anonymization results
    """
    print("Running anonymization pipeline...")
    print(f"Input token results: {token_results}")
    
    if original_text is None:
        raise ValueError("Original text is required for proper anonymization")
    
    # Process the results
    result = process_anonymization_results(token_results, original_text, threshold=0.3)
    
    print(f"Original text: {result['original_text']}")
    print(f"Masked text: {result['masked_text']}")
    print("Replacements:")
    for replacement in result['replacements']:
        print(f"  {replacement['original']} -> {replacement['placeholder']} (score: {replacement['activation']:.4f})")
    
    return result

def initialize_privacy_pipeline():
    """
    Initialize the privacy anonymization pipeline.
    
    Returns:
        The initialized transformers pipeline
    """
    print("Initializing privacy anonymization pipeline...")
    pipe = pipeline("token-classification", model="ai4privacy/llama-ai4privacy-english-anonymiser-openpii")
    print("Pipeline initialized successfully!")
    return pipe

def anonymize_text(pipe, text: str, verbose: bool = True) -> Dict:
    """
    Anonymize a given text using the privacy pipeline.
    
    Args:
        pipe: The initialized transformers pipeline
        text: Text to anonymize
        verbose: Whether to print detailed output
    
    Returns:
        Dictionary containing anonymization results
    """
    if verbose:
        print(f"Anonymizing text: {text}")
    
    # Get token classification results
    result = pipe(text)
    
    if verbose:
        print("Raw token classification results:")
        print(result)
        print("\n" + "="*50)
    
    # Run the anonymization pipeline
    anonymized_result = run_anonymization_pipeline(result, text)
    
    if verbose:
        print("="*50)
        print(f"\nFinal anonymized text: {anonymized_result['masked_text']}")
    
    return anonymized_result

def main():
    """
    Main function to demonstrate the privacy anonymization pipeline.
    """
    # Initialize the pipeline
    pipe = initialize_privacy_pipeline()
    
    # Test text
    test_text = "I am living in South London and currently unemployed, looking to apply for benefits"
    
    # Anonymize the text
    result = anonymize_text(pipe, test_text)
    
    print("\nPipeline completed successfully!")
    return result

if __name__ == "__main__":
    main()