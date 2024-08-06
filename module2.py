from googletrans import Translator

def translate_to_english(text):
    # Create a Translator object
    translator = Translator()

    # Translate text to English
    translation = translator.translate(text, dest='en')

    return translation.text

def main():
    # Get user input
    text = input("Enter the text you want to translate to English: ")

    # Translate the text
    translated_text = translate_to_english(text)

    # Print the translated text
    print("Translated text in English:")
    print(translated_text)

if __name__ == "__main__":
    main()
