import json
import os
import deepl
from typing import Dict, List
from dotenv import load_dotenv

def extract_and_translate(input_file: str, target_languages: List[str], api_key: str) -> Dict:
    """
    Extract strings from Xcstrings file and translate them using DeepL API.
    
    Args:
        input_file: Path to the Xcstrings file
        target_languages: List of target language codes (e.g., ['FR', 'ES'])
        api_key: DeepL API key
    
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
                        print(f"Error translating {key} to {lang}: {str(e)}")
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

def main():
    # Load environment variables
    load_dotenv()
    
    # Configuration
    API_KEY = os.getenv('DEEPL_API_KEY')
    if not API_KEY:
        raise ValueError("Please set DEEPL_API_KEY environment variable")
    
    INPUT_FILE = "Localizable.xcstrings"
    OUTPUT_FILE = "Localizable_translated.xcstrings"
    TARGET_LANGUAGES = ['FR', 'ES', 'DE']  # Add more languages as needed
    
    # Extract and translate
    translated_xcstrings = extract_and_translate(INPUT_FILE, TARGET_LANGUAGES, API_KEY)
    
    # Save results in Xcstrings format
    save_xcstrings(translated_xcstrings, OUTPUT_FILE)
    
    # Print summary
    print("\nTranslation completed!")
    print(f"Output file: {OUTPUT_FILE}")
    print("\nTranslated languages:")
    for lang in TARGET_LANGUAGES:
        print(f"- {lang}")

if __name__ == "__main__":
    main()