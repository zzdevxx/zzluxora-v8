"""
zzluxora — Audio Engine
Extracts audio features, computes Valence-Arousal, maps to HSV-RGBW.
"""

import numpy as np
import librosa


def extract_features(audio_path):
    """Extract audio features using librosa. Returns dict of features."""
    y, sr = librosa.load(audio_path, sr=22050, mono=True)
    duration = librosa.get_duration(y=y, sr=sr)

    # Tempo / BPM
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    if hasattr(tempo, '__len__'):
        tempo = float(tempo[0])
    else:
        tempo = float(tempo)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr).tolist()

    # RMS Energy
    rms = librosa.feature.rms(y=y)[0]
    rms_mean = float(np.mean(rms))

    # Spectral Centroid
    sc = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    sc_mean = float(np.mean(sc))

    # MFCC (13 coefficients)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc1_mean = float(np.mean(mfcc[0]))

    # Chroma
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)
    major_indices = [0, 2, 4, 5, 7, 9, 11]
    major_energy = float(np.sum(chroma_mean[major_indices]))
    total_energy = float(np.sum(chroma_mean))
    chroma_major = major_energy / total_energy if total_energy > 0 else 0.5
    chroma_peak = int(np.argmax(chroma_mean))

    # Onset
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_rate = float(len(onset_frames) / duration) if duration > 0 else 0

    # Spectral Bandwidth
    sb = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
    sb_mean = float(np.mean(sb))

    # RMS over time (for visualization)
    rms_times = librosa.frames_to_time(np.arange(len(rms)), sr=sr).tolist()
    rms_values = rms.tolist()

    # SC over time
    sc_times = librosa.frames_to_time(np.arange(len(sc)), sr=sr).tolist()
    sc_values = sc.tolist()

    return {
        'duration': round(duration, 2),
        'tempo': round(tempo, 1),
        'beat_times': beat_times,
        'rms_mean': round(rms_mean, 4),
        'rms_times': rms_times,
        'rms_values': rms_values,
        'sc_mean': round(sc_mean, 1),
        'sc_times': sc_times,
        'sc_values': sc_values,
        'mfcc1_mean': round(mfcc1_mean, 2),
        'chroma_major': round(chroma_major, 4),
        'chroma_peak': chroma_peak,
        'chroma_mean': chroma_mean.tolist(),
        'onset_rate': round(onset_rate, 2),
        'sb_mean': round(sb_mean, 1),
    }


def segment_song(audio_path, num_segments=None):
    """Segment song into structural sections using SSM + heuristic."""
    y, sr = librosa.load(audio_path, sr=22050, mono=True)
    duration = librosa.get_duration(y=y, sr=sr)

    # Compute chroma for self-similarity
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=512)
    # Self-similarity matrix
    ssm = librosa.segment.recurrence_matrix(chroma, mode='affinity', sym=True)

    # Use spectral clustering-like approach via novelty curve
    novelty = librosa.segment.novelty(ssm)
    # Find peaks in novelty = segment boundaries
    peaks = []
    threshold = np.mean(novelty) + 0.5 * np.std(novelty)
    for i in range(1, len(novelty) - 1):
        if novelty[i] > threshold and novelty[i] > novelty[i-1] and novelty[i] > novelty[i+1]:
            peaks.append(i)

    # Convert frames to times
    boundary_times = librosa.frames_to_time(peaks, sr=sr, hop_length=512).tolist()
    boundary_times = [0.0] + boundary_times + [duration]

    # Ensure reasonable number of segments (3-8)
    if len(boundary_times) < 4:
        # Too few boundaries, split evenly
        n = 4
        boundary_times = [duration * i / n for i in range(n + 1)]
    elif len(boundary_times) > 10:
        # Too many, keep strongest
        novelty_at_peaks = [novelty[p] for p in peaks]
        top_indices = np.argsort(novelty_at_peaks)[-7:]
        top_peaks = sorted([peaks[i] for i in top_indices])
        boundary_times = [0.0] + librosa.frames_to_time(top_peaks, sr=sr, hop_length=512).tolist() + [duration]

    # Label segments heuristically based on energy and position
    segments = []
    total_segs = len(boundary_times) - 1
    for i in range(total_segs):
        start = boundary_times[i]
        end = boundary_times[i + 1]
        seg_duration = end - start

        # Extract features for this segment
        start_sample = int(start * sr)
        end_sample = min(int(end * sr), len(y))
        y_seg = y[start_sample:end_sample]

        if len(y_seg) < sr * 0.5:
            continue

        seg_rms = float(np.mean(librosa.feature.rms(y=y_seg)[0]))
        seg_sc = float(np.mean(librosa.feature.spectral_centroid(y=y_seg, sr=sr)[0]))

        # Heuristic labeling based on position and energy
        rel_pos = (start + end) / 2 / duration  # relative position 0-1
        if i == 0 and seg_duration < duration * 0.15:
            label = 'intro'
        elif i == total_segs - 1 and seg_duration < duration * 0.15:
            label = 'outro'
        elif seg_rms > np.mean(librosa.feature.rms(y=y)[0]) * 1.15:
            label = 'chorus'
        elif 0.3 < rel_pos < 0.7 and seg_rms < np.mean(librosa.feature.rms(y=y)[0]) * 0.9:
            label = 'bridge'
        else:
            label = 'verse'

        segments.append({
            'index': i,
            'label': label,
            'start': round(start, 2),
            'end': round(end, 2),
            'duration': round(seg_duration, 2),
            'rms': round(seg_rms, 4),
            'sc': round(seg_sc, 1),
        })

    return segments


# === NORMALIZATION ===
RANGES = {
    'tempo': (60, 180),
    'rms_mean': (0.01, 0.50),
    'sc_mean': (500, 5000),
    'mfcc1_mean': (-300, 100),
    'onset_rate': (0.5, 8.0),
    'chroma_major': (0.0, 1.0),
}


def normalize(value, key):
    """Min-max normalize a value to [0, 1]."""
    lo, hi = RANGES.get(key, (0, 1))
    if hi == lo:
        return 0.5
    return max(0.0, min(1.0, (value - lo) / (hi - lo)))

