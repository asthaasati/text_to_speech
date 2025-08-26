import srt
import os
from gtts import gTTS
import re

def generate_voiceovers_from_srt(srt_file_path, output_dir="voiceovers", language="en"):
    """
    Generates individual MP3 voiceover files for each subtitle entry in an SRT file.

    Args:
        srt_file_path (str): The path to the input .srt file.
        output_dir (str): The directory where the audio files will be saved.
        language (str): The language code for the text-to-speech engine (e.g., 'en', 'es', 'fr').
    """
    try:
        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        print(f"Output directory '{output_dir}' is ready.")

        # Parse the SRT file
        print(f"Parsing '{srt_file_path}'...")
        # The .strip('"') method is used here to remove any leading/trailing
        # double quotes that users might include when pasting the path.
        with open(srt_file_path.strip('"'), 'r', encoding='utf-8') as f:
            file_content = f.read()

        # Find the start of the first subtitle block (e.g., '1\n00:00:00') and parse from there
        srt_start_match = re.search(r'^\d+\n', file_content, re.MULTILINE)
        if srt_start_match:
            start_index = srt_start_match.start()
            clean_content = file_content[start_index:]
            subtitle_generator = srt.parse(clean_content)
        else:
            subtitle_generator = srt.parse(file_content)

        subtitles = list(subtitle_generator)

        if not subtitles:
            print("No subtitles found in the file. Exiting.")
            return

        print(f"Found {len(subtitles)} subtitle entries. Generating voiceovers...")

        # Process each subtitle entry
        for i, sub in enumerate(subtitles):
            # Clean up the text by removing any formatting or extra newlines
            text_to_speak = sub.content.strip().replace('\n', ' ')
            
            # Skip empty subtitle entries
            if not text_to_speak:
                print(f"Skipping empty subtitle at index {sub.index}.")
                continue

            try:
                # Create a gTTS object
                tts = gTTS(text=text_to_speak, lang=language, slow=False)
                
                # Create a filename based on the subtitle index
                file_name = f"voiceover_{sub.index:04d}.mp3"
                file_path = os.path.join(output_dir, file_name)

                # Save the audio file
                tts.save(file_path)
                print(f"Generated voiceover for subtitle {sub.index}: '{text_to_speak[:40]}...' -> '{file_path}'")

            except Exception as e:
                print(f"Error generating voiceover for subtitle {sub.index}: {e}")
                continue

        print("\nAll voiceovers have been generated successfully!")
        
    except FileNotFoundError:
        print(f"Error: The file '{srt_file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # --- Configuration ---
    # Prompt the user for the SRT file path at runtime.
    input_srt_file = input("Please enter the path to your .srt file: ")
    # The directory where the voiceover audio files will be saved.
    output_folder = 'voiceover_audio'
    # The language of the subtitles. 'en' for English.
    language_code = 'en'
    # ---------------------

    generate_voiceovers_from_srt(input_srt_file, output_folder, language_code)
