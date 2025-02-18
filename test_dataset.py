import json

# Load dataset labels
label_file_path = "emotion_label.json"  # Ensure this file is in the working directory
with open(label_file_path, "r") as f:
    emotion_labels = json.load(f)

# Extract unique emotion labels
unique_emotions = set()
for annotations in emotion_labels.values():
    unique_emotions.add(annotations[0]["majority_emo"].lower())

# Print the unique emotion labels
print("Unique emotion labels in dataset:", unique_emotions)
print("Total number of unique labels:", len(unique_emotions))
