import asyncio
import json
import os
from validate_prompt_speeach import analyze_user_audio_input, evaluate_accuracy

# Get list of converted WAV files (ONLY from studio001/middle/)
converted_wav_path = "converted_wav/studio001/middle"  # Limit to studio001

# Collect only the first 5 .wav files from studio001/middle
audio_files = sorted([
    os.path.join(converted_wav_path, file)
    for file in os.listdir(converted_wav_path)
    if file.endswith(".wav")
])[:5]  # ✅ Limit to the first 5 files

# Run evaluation (batch process)
if __name__ == "__main__":
    report, predictions = asyncio.run(evaluate_accuracy(audio_files))  # ✅ Now always receives two values

    # Save OpenAI predictions to a file
    with open("openai_predictions.json", "w") as f:
        json.dump(predictions, f, indent=4)

    # Save accuracy report to a file
    with open("accuracy_report.json", "w") as f:
        json.dump(report, f, indent=4)

    # Print both to the console
    print("\n===== OpenAI Predictions =====\n")
    print(json.dumps(predictions, indent=4))

    print("\n===== Accuracy Evaluation Report =====\n")
    print(json.dumps(report, indent=4))



