import math
import struct
import wave
import numpy as np
import sounddevice as sd
SAMPLE_RATE = 44100

#Helper function(or rather, where the magic happens.)
def generate_tone(frequency, duration_ms):
    #Generates a float32 sine wave for a specific pitch and duration
    num_samples = int(SAMPLE_RATE * (duration_ms / 1000.0))
    t = np.linspace(0, duration_ms / 1000.0, num_samples, endpoint=False)
    return 0.5 * np.sin(2 * np.pi * frequency * t)

def generate_silence(duration_ms):
    #Generates a silent flatline array for timing spacing
    num_samples = int(SAMPLE_RATE * (duration_ms / 1000.0))
    return np.zeros(num_samples)

def parse_and_synthesize(morse_input, frequency, dot_ms):
    #Parses a user string and transform it into audio
    dash_ms = dot_ms * 3
    element_space_ms = dot_ms
    letter_space_ms = dot_ms * 3
    word_space_ms = dot_ms * 7
    buffer_segments = []
    #Splits the morse into individually words
    words = morse_input.strip().split('/')

    for w_idx, word in enumerate(words):
        #Split words into individual letters
        letters = word.strip().split(' ')

        for l_idx, letter in enumerate(letters):
            #Process individual dots and dashes inside the letter
            for e_idx, element in enumerate(letter):
                if element == '.':
                    buffer_segments.append(generate_tone(frequency, dot_ms))
                elif element == '-':
                    buffer_segments.append(generate_tone(frequency, dash_ms))
                
                #Adds silence in between elements
                if e_idx < len(letter) - 1:
                    buffer_segments.append(generate_silence(element_space_ms))
            #Adds silence in between letters
            if l_idx < len(letters) - 1:
                buffer_segments.append(generate_silence(letter_space_ms))
        #Add silence between words
        if w_idx < len (words) - 1:
            buffer_segments.append(generate_silence(word_space_ms))
    if not buffer_segments:
        return np.zeros(0)
    
    return np.concatenate(buffer_segments)

def play_audio(audio_buffer):
    #Plays the generated sound
    if len(audio_buffer) == 0:
        return
    sd.play(audio_buffer, SAMPLE_RATE)
    sd.wait()

def save_audio(filename, audio_buffer):
    #Saves the array to PCM Wave format
    pcm_data = (audio_buffer * 32767).astype(np.int16)
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth92
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(pcm_data.tobytes())


