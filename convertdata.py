import os
from pydub import AudioSegment
import json

# Root directory containing multiple "studioXXX/middle" folders
input_root = "./studio1-10"  # Update this to your actual path
output_root = "./converted_wav"  # Change this if you want to store WAV files elsewhere

# Function to convert FLAC to WAV while maintaining folder structure
def convert_flac_to_wav():
    for studio in os.listdir(input_root):  # Iterate through studioXXX folders
        studio_path = os.path.join(input_root, studio)
        
        if os.path.isdir(studio_path):  # Ensure it's a directory
            middle_path = os.path.join(studio_path, "middle")  # Only process "middle" folder
            
            if os.path.exists(middle_path):  # Ensure "middle" exists
                output_studio_path = os.path.join(output_root, studio, "middle")  # Preserve structure
                os.makedirs(output_studio_path, exist_ok=True)

                for file in os.listdir(middle_path):
                    if file.endswith(".flac"):  # Convert only FLAC files
                        input_file = os.path.join(middle_path, file)
                        output_file = os.path.join(output_studio_path, file.replace(".flac", ".wav"))
                        
                        # Convert FLAC to WAV
                        audio = AudioSegment.from_file(input_file, format="flac")
                        audio.export(output_file, format="wav")
                        print(f"Converted: {input_file} → {output_file}")

# Function to filter short audio files
def filter_short_audio(root_dir, min_duration=1000, short_audio_dir="short_audio_files", log_file="removed_files.txt"):
    os.makedirs(short_audio_dir, exist_ok=True)
    removed_files = []
    
    for studio in os.listdir(root_dir):  # Iterate through each studio folder
        studio_path = os.path.join(root_dir, studio)
        middle_path = os.path.join(studio_path, "middle")
        
        if os.path.exists(middle_path):
            for filename in os.listdir(middle_path):
                if filename.endswith(".wav") or filename.endswith(".mp3"):
                    file_path = os.path.join(middle_path, filename)
                    audio = AudioSegment.from_file(file_path)
                    
                    if len(audio) < min_duration:
                        os.rename(file_path, os.path.join(short_audio_dir, filename))
                        removed_files.append(filename.replace(".wav", ".flac"))  # Store as .flac format
                        print(f"Moved: {filename} (Duration: {len(audio)} ms)")
                    else:
                        print(f"Kept: {filename} (Duration: {len(audio)} ms)")
    
    # Save removed files list if any files were removed
    if removed_files:
        with open(log_file, "w") as f:
            for file in removed_files:
                f.write(file + "\n")
        print("Filtering complete. Removed files list saved.")
    else:
        print("No short files found. Skipping removal log creation.")
                        
# Function to generate a new cleaned JSON file based on removed files
def clean_json(json_path, removed_files_log, output_json="filtered_emotion_label.json"):
    if not os.path.exists(removed_files_log):
        print("No removed files log found. Skipping JSON cleaning.")
        return
    
    with open(removed_files_log, "r") as f:
        removed_files = set(f.read().splitlines())
    
    if not removed_files:
        print("Removed files log is empty. Skipping JSON cleaning.")
        return
    
    with open(json_path, "r") as f:
        data = json.load(f)
    
    filtered_data = {k: v for k, v in data.items() if k not in removed_files}
    
    with open(output_json, "w") as f:
        json.dump(filtered_data, f, indent=4)
    print(f"Filtered JSON file saved as {output_json}.")

if __name__ == "__main__":
    # Convert FLAC to WAV
    convert_flac_to_wav()

    # Run filtering for all studios
    filter_short_audio("./converted_wav")
    
    # Run JSON cleaning to create a new file
    clean_json("emotion_label.json", "removed_files.txt")
