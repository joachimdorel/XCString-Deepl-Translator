# XCStrings Translator

A Python tool to automate the translation of iOS Localizable.xcstrings files using the DeepL API. This tool helps you maintain localization files for your iOS applications by automatically translating strings to multiple languages.

## Prerequisites

- Python 3.8 or higher
- A DeepL API key (free or pro)
- Xcode project with localization setup

## Important: Before You Start

⚠️ **Critical Setup Step**: Before using this tool, you must first set up your languages in Xcode:

1. Open your Xcode project
2. Select your Localizable.xcstrings file
3. Click the "+" button in the bottom left corner
4. Select the languages you want to add from the list
5. Export or copy your Localizable.xcstrings file to the same directory as this script

This step is mandatory because the tool relies on the language structure being present in the Localizable.xcstrings file.

## Installation

1. Clone or download this repository:
```bash
git clone <repository-url>
cd xcstrings-translator
```

2. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv .venv

# Activate it on macOS/Linux:
source .venv/bin/activate

# Activate it on Windows:
.venv\Scripts\activate

```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

5. Edit the `.env` file and add your DeepL API key:
```
DEEPL_API_KEY=your-deepl-api-key-here
```

## Usage

1. Place your `Localizable.xcstrings` file in the project directory

2. Run the translation script:
```bash
python xcstrings_translator.py --in=FR,DE,IT,ES
```

#### Additional options:
- ```--in```: Required. Comma-separated list of target language codes (e.g., FR,DE,IT,ES)
- ```--input```: Optional. Specify input file path (default: Localizable.xcstrings)
- ```--output```: Optional. Specify output file path (default: Localizable_translated.xcstrings)
- ```-v```, ```--verbose```: Optional. Display detailed progress messages during translation


###### Examples:

Basic usage:
```
python xcstrings_translator.py --in=FR,DE,IT,ES
```

With custom input/output files:
```
python xcstrings_translator.py --in=FR,DE,IT,ES --input=./input.xcstrings --output=./output.xcstrings
```

With verbose output:
```
python xcstrings_translator.py --in=FR,DE,IT,ES -v
```

3. The translated file will be generated as `Localizable_translated.xcstrings`

### Supported Language Codes

Here are some common language codes for DeepL:
- 'FR' (French)
- 'ES' (Spanish)
- 'DE' (German)
- 'IT' (Italian)
- 'JA' (Japanese)
- 'NL' (Dutch)
- 'PL' (Polish)
- 'PT' (Portuguese)
- 'RU' (Russian)
- 'ZH' (Chinese)

For a complete list of supported languages, refer to the [DeepL API documentation](https://www.deepl.com/docs-api/translate-text/).

## File Structure

```
xcstrings_translator/
├── .env                          # API key configuration
├── .env.example                  # Example environment file
├── .gitignore                   # Git ignore file
├── requirements.txt             # Python dependencies
├── xcstrings_translator.py      # Main translation script
└── Localizable.xcstrings        # Your input file
```

## Error Handling

Common errors and solutions:

1. "Authorization failure, check auth_key":
   - Verify your DeepL API key in the `.env` file
   - Ensure you're using the correct API key type (Free or Pro)

2. "File not found":
   - Make sure `Localizable.xcstrings` is in the same directory as the script

3. "Invalid language code":
   - Check that your language codes are correctly formatted (e.g., FR, DE, ES)
   - Verify that the languages are supported by DeepL

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [DeepL API](https://www.deepl.com/docs-api) for translation services
- [python-dotenv](https://github.com/theskumar/python-dotenv) for environment management