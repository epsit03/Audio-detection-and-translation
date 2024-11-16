import cv2
import speech_recognition as sr
from deep_translator import GoogleTranslator
import threading
import queue
import sys


def recognize_and_translate_speech():
    """Recognizes spoken language, translates it to English, and saves a transcript."""
    lang = input("Enter the desired language code (or leave blank for auto-detection): ")
    recognizer = sr.Recognizer()
    audio_queue = queue.Queue()
    stop_event = threading.Event()
    transcript = []  # To store recognized speech

    recognized_text = ""
    translated_text = ""

    # Font settings for better readability
    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 1
    font_thickness = 2
    text_color = (255, 255, 255)  # White text color

    def wrap_text(text, width=80):
        """Wraps text to fit within the specified width."""
        lines = []
        words = text.split(" ")
        line = ""

        for word in words:
            if len(line + word) <= width:
                line += (word + " ")
            else:
                lines.append(line.strip())
                line = word + " "

        if line:
            lines.append(line.strip())
        
        return lines

    def open_camera():
        """Opens the camera feed with real-time transcription overlay."""
        nonlocal recognized_text, translated_text
        cap = cv2.VideoCapture(0)  # Access the default camera

        if not cap.isOpened():
            print("Error: Could not open the camera.")
            stop_event.set()
            return

        # Set desired resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Set full-screen mode
        cv2.namedWindow("Camera Feed", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Camera Feed", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        while not stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read the frame.")
                break

            # Add overlay for text display
            overlay = frame.copy()
            height, width, _ = frame.shape
            cv2.rectangle(overlay, (0, height - 120), (width, height), (0, 0, 0), -1)
            frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)

            # Wrap and display the recognized and translated text
            lines = wrap_text(f"You said: {recognized_text}", width=60)
            lines_translated = wrap_text(f"Translated: {translated_text}", width=60)

            y0, dy = height - 100, 30
            for i, line in enumerate(lines + lines_translated):
                y = y0 + i * dy
                cv2.putText(frame, line, (20, y), font, font_scale, text_color, font_thickness)

            cv2.imshow("Camera Feed", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to quit
                stop_event.set()
                break

        cap.release()
        cv2.destroyAllWindows()

    def audio_processing():
        """Processes the audio from the queue and translates it."""
        nonlocal recognized_text, translated_text
        while not stop_event.is_set():
            try:
                audio = audio_queue.get(timeout=1)
            except queue.Empty:
                continue

            try:
                recognized_text = recognizer.recognize_google(audio, language=lang or None)
                print(f"You said: {recognized_text}")

                translated_text = GoogleTranslator(source=lang or "auto", target="en").translate(recognized_text)
                print(f"Translated text (English): {translated_text}")

                # Append the recognized text to transcript
                transcript.append(recognized_text)

            except sr.UnknownValueError:
                print("Could not understand the audio.")
            except sr.RequestError as e:
                print(f"Error with Google Speech Recognition service: {e}")
            except Exception as e:
                print(f"Error during translation: {e}")

    def audio_capture():
        """Captures audio from the microphone and puts it in the queue."""
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please remain silent.")
            recognizer.adjust_for_ambient_noise(source, duration=3)
            print("Listening...")

            while not stop_event.is_set():
                try:
                    print("Speak now...")
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
                    audio_queue.put(audio)
                except sr.WaitTimeoutError:
                    print("No speech detected. Retrying...")
                except Exception as e:
                    print(f"Error during audio capture: {e}")

    # Save the transcript to a file when the program ends
    def save_transcript():
        if transcript:
            try:
                filename = "transcript.txt"
                with open(filename, "w", encoding="utf-8") as file:
                    file.write("\n".join(transcript))
                print(f"Transcript saved as {filename}.")
            except Exception as e:
                print(f"Error saving transcript: {e}")

    # Start threads
    threads = [
        threading.Thread(target=open_camera),
        threading.Thread(target=audio_capture),
        threading.Thread(target=audio_processing),
    ]

    for thread in threads:
        thread.start()

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("Shutting down...")
        stop_event.set()
        save_transcript()
        for thread in threads:
            thread.join()
        sys.exit(0)

    save_transcript()  # Save transcript when exiting normally


if __name__ == "__main__":
    recognize_and_translate_speech()
