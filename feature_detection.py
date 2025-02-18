import os
import librosa
import pandas as pd
import numpy as np
import ydata_profiling

# ✅ Set path to folder containing converted WAV files
input_folder = "converted_wav/studio001/middle"

# ✅ List all WAV/FLAC files in the folder
audio_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith((".wav", ".flac"))]

# ✅ Feature extraction function
def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, sr=44100)

        return {
            "filename": os.path.basename(file_path),
            "mfcc_mean": np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)),
            "mel_spectrogram_mean": np.mean(librosa.feature.melspectrogram(y=y, sr=sr)),
            "spectral_centroid": np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)),
            "spectral_contrast": np.mean(librosa.feature.spectral_contrast(y=y, sr=sr)),
            "rms_energy": np.mean(librosa.feature.rms(y=y)),
            "pitch_mean": np.mean(librosa.yin(y, fmin=50, fmax=300)),
            "zero_crossing_rate": np.mean(librosa.feature.zero_crossing_rate(y))
        }
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return None  # Skip files that cause errors

# ✅ Extract features for all audio files
feature_list = [extract_features(file) for file in audio_files if extract_features(file) is not None]

# ✅ Convert to DataFrame
df = pd.DataFrame(feature_list)

# ✅ Generate YData Report
profile = df.profile_report(title="Audio Feature Summary")
profile.to_file("audio_feature_report.html")

# ✅ Save extracted features to CSV for further analysis
df.to_csv("audio_features.csv", index=False)

print("✅ Feature extraction completed! Check `audio_feature_report.html` and `audio_features.csv`.")
