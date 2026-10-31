import wave
import numpy as np

def audio_to_morse(wav_filename):
    #Opens wave file and gets info
    with wave.open(wav_filename, 'rb') as wav_file:
        sample_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()
        channels = wav_file.getnchannels()
        sampwidth = wav_file.getsampwidth()
        raw_bytes = wav_file.readframes(num_frames)
    #Convert raw bytes to integer
    if sampwidth == 2:
        audio_data = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32)
    elif sampwidth == 1:
        audio_data = (np.frombuffer(raw_bytes, dtype=np.uint8).astype(np.float32) - 128)
    else:
        print("Unsupported audio format(8-bit or 16-bit PCM only)")
        return ""
    #Averages the channel if stereo
    if channels > 1:
        audio_data = audio_data.reshape(-1, channels).mean(axis=1)
    #Normalize the signal amplitude
    amplitude = np.abs(audio_data)
    max_amp = np.max(amplitude) if np.max(amplitude) > 0 else 1
    normalized = amplitude / max_amp
    is_sound = (normalized > 0.15).astype(np.int8)
    #Calculate length of all sound burst and silent gaps
    durations = []
    current_state = is_sound[0]
    current_length = 0
    for sample in is_sound:
        if sample == current_state:
            current_length += 1
        else:
            #Convert length in samples to duration in miliseconds
            duration_ms = (current_length / sample_rate) * 1000
            durations.append((current_state, duration_ms))
            current_state = sample
            current_length = 1
    #Add final element
    durations.append((current_state, (current_length / sample_rate) * 1000))
    #Extract sound durations to find baseline dynamic WPM speed
    sound_durations = [dur for state, dur in durations if state == 1 and dur > 5]
    if not sound_durations:
        return "No Morse code sound detected in file."
    #Calculate adaptive thresholds based on audio speed
    min_sound = min(sound_durations)
    max_sound = max(sound_durations)
    tone_threshold = (min_sound + max_sound) / 2
    #Filter out silence and ignore hardware jitters
    silence_durations = [dur for state, dur in durations if state == 0 and dur > 10]
    if silence_durations:
        min_silence = min(silence_durations)
        max_silence = max(silence_durations)
        #Set 2 adaptive cut-offs to classify silences(element, letter or word)
        letter_threshold = min_silence * 2.2
        word_threshold = min_silence * 5.0
    else:
        #Fallback if no gaps found
        letter_threshold = tone_threshold * 2
        word_threshold = tone_threshold * 5
    #Reconstruct the string
    morse_result = []
    for state, dur in durations:
        #Tone
        if state == 1:
            if dur < 10:
                #Ignores audio click artifacts
                continue
            if dur < tone_threshold:
                morse_result.append(".")
            else:
                morse_result.append("-")
        else:
            #Silence
            if dur > word_threshold:
                morse_result.append(" / ")
            elif dur > letter_threshold:
                morse_result.append(' ')
    #Clean up spacing
    return "".join(morse_result).strip().replace("   ", " ").replace("  ", " ")