import json
import os
import deepl
import argparse
from typing import Dict, List
from dotenv import load_dotenv

def extract_and_translate(input_file: str, target_languages: List[str], api_key: str, verbose: bool = False) -> Dict:
    """
    Extract strings from Xcstrings file and translate them using DeepL API.
    
    Args:
        input_file: Path to the Xcstrings file
        target_languages: List of target language codes (e.g., ['FR', 'ES'])
        api_key: DeepL API key
        verbose: Whether to print detailed progress messages
    
    Returns:
        Dictionary containing the complete Xcstrings structure with translations
    """
    # Initialize DeepL translator
    translator = deepl.Translator(api_key)
    
    # Read and parse the Xcstrings file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create a copy of the original data to preserve structure
    output_data = {
        "sourceLanguage": data["sourceLanguage"],
        "strings": {},
        "version": data.get("version", "1.0")  # Preserve original version or default to "1.0"
    }
    
    # Process each string
    for key, value in data['strings'].items():
        # Initialize the string entry with original metadata
        output_data['strings'][key] = {
            "extractionState": value.get("extractionState", "manual"),
            "localizations": {}
        }
        
        # Get English text if available
        english_text = None
        if 'localizations' in value and 'en' in value['localizations']:
            english_text = value['localizations']['en']['stringUnit']['value']
            # Add English translation to output
            output_data['strings'][key]['localizations']['en'] = {
                "stringUnit": {
                    "state": "translated",
                    "value": english_text
                }
            }
            
            # Translate to target languages
            if english_text:
                for lang in target_languages:
                    if verbose:
                        print(f"Translating to {lang}: {key}")
                    try:
                        result = translator.translate_text(
                            english_text,
                            target_lang=lang
                        )
                        output_data['strings'][key]['localizations'][lang.lower()] = {
                            "stringUnit": {
                                "state": "translated",
                                "value": result.text
                            }
                        }
                    except Exception as e:
                        error_msg = f"Error translating {key} to {lang}: {str(e)}"
                        if verbose:
                            print(error_msg)
                        output_data['strings'][key]['localizations'][lang.lower()] = {
                            "stringUnit": {
                                "state": "error",
                                "value": f"ERROR: {str(e)}"
                            }
                        }
    
    return output_data

def save_xcstrings(translations: Dict, output_file: str):
    """Save translations to an Xcstrings file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)

def parse_languages(languages_str: str) -> List[str]:
    """Parse comma-separated language codes into a list."""
    return [lang.strip().upper() for lang in languages_str.split(',')]

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Translate Xcstrings file using DeepL API')
    parser.add_argument('--in', dest='input_languages', required=True,
                      help='Comma-separated list of target language codes (e.g., FR,DE,IT,ES)')
    parser.add_argument('--input', default="Localizable.xcstrings",
                      help='Input Xcstrings file path (default: Localizable.xcstrings)')
    parser.add_argument('--output', default="Localizable_translated.xcstrings",
                      help='Output Xcstrings file path (default: Localizable_translated.xcstrings)')
    parser.add_argument('-v', '--verbose', action='store_true',
                      help='Display detailed progress messages')
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Configuration
    API_KEY = os.getenv('DEEPL_API_KEY')
    if not API_KEY:
        raise ValueError("Please set DEEPL_API_KEY environment variable")
    
    # Parse target languages
    target_languages = parse_languages(args.input_languages)
    
    if args.verbose:
        print("\nStarting translation process...")
        print(f"Target languages: {', '.join(target_languages)}")
    
    # Extract and translate
    translated_xcstrings = extract_and_translate(args.input, target_languages, API_KEY, args.verbose)
    
    # Save results in Xcstrings format
    save_xcstrings(translated_xcstrings, args.output)
    
    # Print summary
    print("\nTranslation completed!")
    print(f"Input file: {args.input}")
    print(f"Output file: {args.output}")
    print("\nTranslated languages:")
    for lang in target_languages:
        print(f"- {lang}")

if __name__ == "__main__":
    main()