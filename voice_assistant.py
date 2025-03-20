import speech_recognition as sr
import pyttsx3
import wikipediaapi
import pywhatkit
from duckduckgo_search import DDGS

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set voice to female
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower():  # Check for female in the voice name
        engine.setProperty('voice', voice.id)
        break

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Capture voice input and convert to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return "Listening timed out. Please try again."
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."
    except sr.RequestError as e:
        return f"Error connecting to speech recognition service: {str(e)}"

def search_wikipedia(query):
    """Fetch a detailed yet concise answer from Wikipedia."""
    wiki_wiki = wikipediaapi.Wikipedia(user_agent="Mozilla/5.0", language="en")
    page = wiki_wiki.page(query)
    if page.exists():
        summary = page.summary.split(". ")
        # Return 2 sentences for more context
        return ". ".join(summary[:2]) + "." if summary else "I couldn't find relevant info on Wikipedia."
    return "No relevant page found on Wikipedia."

def web_search(query):
    """Fetch a reliable answer using DuckDuckGo search."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        if results:
            # Combine snippets for a comprehensive answer
            snippets = [result["body"] for result in results if "body" in result]
            return " ".join(snippets[:2])  # Limit to 2 snippets for clarity
        return "No results found for your query."
    except Exception as e:
        return f"Error fetching web search: {str(e)}"

def play_song(song_name):
    """Play a song on YouTube."""
    speak(f"Playing {song_name} on YouTube.")
    try:
        pywhatkit.playonyt(song_name)
    except Exception as e:
        speak(f"Sorry, there was an error playing the song: {str(e)}")

def answer_question(question):
    """Try Wikipedia first, then fallback to web search."""
    wiki_answer = search_wikipedia(question)
    if wiki_answer and "No relevant page" not in wiki_answer:
        return wiki_answer
    return web_search(question)  # Use DuckDuckGo if Wikipedia fails

def main():
    """Main loop for the voice assistant."""
    speak("Hello, I am your assistant. How can I help you today?")
    while True:
        command = listen().lower()
        print("You said:", command)

        if "exit" in command or "stop" in command:
            speak("Goodbye!")
            print("Goodbye!")
            break

        elif "play" in command:
            song = command.replace("play", "").strip()
            play_song(song)

        elif "wikipedia" in command:
            query = command.replace("wikipedia", "").strip()
            result = search_wikipedia(query)
            print("Wikipedia:", result)
            speak(result)

        elif "search" in command:
            query = command.replace("search", "").strip()
            result = web_search(query)
            print("Search Result:", result)
            speak(result)

        elif "what is" in command or "who is" in command or "how" in command:
            result = answer_question(command)
            print("Answer:", result)
            speak(result)

        else:
            print("Command not recognized.")  # Silent for unrecognized commands

if __name__ == "__main__":
    main()
