import speech_recognition as sr
from langdetect import detect, DetectorFactory

# Ensuring consistent language detection
DetectorFactory.seed = 0

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            print("Transcribed Text: " + text)

            # Detect the language of the transcribed text
            language = detect(text)
            print("Detected Language Code: " + language)
            
            # Optionally, you can map language codes to human-readable language names
            language_names = {
                'en': 'English',
                'es': 'Spanish',
                'hi': 'Hindi',
                'fr': 'French',
                'de': 'German',
                'zh': 'Chinese',
                # Add other language codes as needed
            }
            print("Detected Language: " + language_names.get(language, "Unknown"))

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Sorry, there was an error with the request: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    recognize_speech()
