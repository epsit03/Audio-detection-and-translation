import speech_recognition as sr
from google.cloud import speech_v1p1beta1 as speech
import os

def recognize_speech():
    lang = input("Enter the desired language code: ")
    recognizer = sr.Recognizer()

    # Replace with your Google Cloud Speech-to-Text credentials
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\hp\Downloads\bookshelf-analytics-sqlonlyapp-858cffbd6345.json'

    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            # Convert audio to bytes using get_wav_data()
            audio_content = audio.get_wav_data()

            # Create a speech client
            client = speech.SpeechClient()

            # Configure the audio content
            audio = speech.RecognitionAudio(content=audio_content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=44100,
                language_code=f"{lang}",  # Set initial language
                enable_automatic_punctuation=True
            )

            # Detect speech
            response = client.recognize(config=config, audio=audio)

            # Extract the text and language code (assuming language code is still present in newer versions)
            for result in response.results:
                text = result.alternatives[0].transcript
                # Check if language_code is still available
                if hasattr(result, 'language_code'):
                    language = result.language_code
                else:
                    print("Language code might not be available in this version.")
                    language = "Unknown"

                print("Transcribed Text:", text)
                print("Detected Language Code:", language)

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Sorry, there was an error with the request: {e}")
        except Exception as e:
            print(f"An error occurred:", e)

if __name__ == "__main__":
    recognize_speech()

