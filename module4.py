import speech_recognition as sr
from googletrans import Translator
from google.cloud import speech_v1p1beta1 as speech  # Import for Google Cloud Speech-to-Text (if used)
import os  # Import for setting credentials (if used)

def recognize_and_translate_speech():
  """Recognizes spoken language and translates it to English (using Google Translate).

  Uses speech_recognition for audio capture and Google Translate API for translation.
  Optionally uses Google Cloud Speech-to-Text for improved accuracy (requires credentials).
  """
  # Import Google Cloud libraries only if environment variables are set for credentials
  if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient()
  else:
    client = None

  lang = input("Enter the desired language code (or leave blank for automatic detection - might not be available): ")
  recognizer = sr.Recognizer()

  with sr.Microphone() as source:
    print("Adjusting for ambient noise...")
    recognizer.adjust_for_ambient_noise(source)
    print("Listening...")
    audio = recognizer.listen(source)

    try:
      if client:
        # Convert audio to bytes using get_wav_data()
        audio_content = audio.get_wav_data()

        # Configure the audio content
        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code=f"{lang}" if lang else None,  # Set language code or None for automatic (if available)
            enable_automatic_punctuation=True
        )

        # Detect speech using Google Cloud Speech-to-Text (if credentials provided)
        response = client.recognize(config=config, audio=audio)
        for result in response.results:
          text = result.alternatives[0].transcript
          break  # Process only the first alternative

      else:
        # Use speech_recognition for basic speech recognition (without language detection)
        text = recognizer.recognize_google(audio)

      print("You said:", text)

      # Translate the recognized text to English
      translator = Translator()
      translated_text = translator.translate(text, dest='en').text
      print("Translated text (English):", translated_text)

    except sr.UnknownValueError:
      print("Could not understand audio")
    except sr.RequestError as e:
      print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
      print(f"An error occurred:", e)

if __name__ == "__main__":
  recognize_and_translate_speech()
