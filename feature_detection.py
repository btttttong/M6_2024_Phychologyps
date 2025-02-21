import os
import librosa
import numpy as np

# ✅ Feature extraction function with flexible argument handling
def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, sr=44100)

        # ✅ Updated `safe_extract` function to handle both positional and keyword arguments
        def safe_extract(feature_function, *args, default=0, **kwargs):
            """Runs a feature extraction function safely, returning a default value if an error occurs."""
            try:
                result = feature_function(*args, **kwargs)
                return float(np.nan_to_num(np.mean(result), nan=default))
            except Exception as e:
                print(f"❌ Feature extraction failed for {feature_function.__name__}: {e}")
                return default  # Return default if feature extraction fails

        # ✅ Extract features safely
        features = {
            "filename": os.path.basename(file_path),
            "mfcc_mean": float(np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13))),
            "mel_spectrogram_mean": float(np.mean(librosa.feature.melspectrogram(y=y, sr=sr))),
            "spectral_centroid": float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))),
            "spectral_contrast": float(np.mean(librosa.feature.spectral_contrast(y=y, sr=sr))),
            "rms_energy": safe_extract(librosa.feature.rms, y=y),
            "zero_crossing_rate": safe_extract(librosa.feature.zero_crossing_rate, y=y),
            "pitch_mean": safe_extract(librosa.yin, y, fmin=50, fmax=300)
        }

        return features

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return None  # Skip corrupted files


# # ✅ Extract features for all audio files
# feature_list = [extract_features(file) for file in audio_files if extract_features(file) is not None]

# # ✅ Convert to DataFrame
# df = pd.DataFrame(feature_list)

# # ✅ Generate YData Report
# profile = df.profile_report(title="Audio Feature Summary")
# profile.to_file("audio_feature_report.html")

# # ✅ Save extracted features to CSV for further analysis
# df.to_csv("audio_features.csv", index=False)

print("✅ Feature extraction completed! Check `audio_feature_report.html` and `audio_features.csv`.")
