from table import ENCODE_TABLE, DECODE_TABLE
from to_audio import *

def encode(text):
    for ch in text:
        if ch not in ENCODE_TABLE:
            print("Invalid character detected! Only [A-Z,a-z,0-9]")
            return
    return ' '.join(ENCODE_TABLE.get(ch, ch) for ch in text)

def decode(text):
    for ch in text:
        if ch not in DECODE_TABLE:
            print("Invalid character detected! Only [.-/]")
            return
    return ''.join(DECODE_TABLE.get(tok, tok) for tok in text.split())

def convert_to_audio(convert_type, play_audio_yn, save_audio_yn):
    if convert_type == '0':
        text = input("Enter text: ")
        morse = encode(text)
        user_hz = input("Enter pitch in Hz(Default: 700): ")
        user_dot_len = input("Enter dot length in miliseconds(Default: 100): ")
        if play_audio_yn == 'n' or save_audio_yn == 'y':
                file_name = input("What do you want the file name to be?(Default: morse.wav): ")
                if file_name == '':
                    file_name = 'morse.wav'
                if not file_name.endswith('.wav'):
                    file_name += '.wav'
        if user_hz == '':
            user_hz = 700
        if user_hz != '':
            user_hz = float(user_hz)
        if user_dot_len == '':
            user_dot_len = 100
        if user_dot_len != '':
            user_dot_len = float(user_dot_len)
        print("Generating audio...")
        audio_data = parse_and_synthesize(morse, user_hz, user_dot_len)
        if play_audio_yn == 'y':
            if len(audio_data) > 0:
                play_audio(audio_data)
            if save_audio_yn == 'y':
                save_audio(file_name, audio_data)
        if play_audio_yn == 'n':
            save_audio(file_name, audio_data)
            print(f"Saved to {file_name}")
    if convert_type == '1':
        morse = input("Enter morse(separated by space on letters and slash on words): ")
        user_hz = input("Enter pitch in Hz(Default: 700): ")
        user_dot_len = input("Enter dot length in miliseconds(Default: 100): ")
        if play_audio_yn == 'n' or save_audio_yn == 'y':
                file_name = input("What do you want the file name to be?(Default: morse.wav): ")
                if file_name == '':
                    file_name = 'morse.wav'
                if not file_name.endswith('.wav'):
                    file_name += '.wav'
        if user_hz == '':
            user_hz = 700
        if user_hz != '':
            user_hz = float(user_hz)
        if user_dot_len == '':
            user_dot_len = 100
        if user_dot_len != '':
            user_dot_len = float(user_dot_len)
        print("Generating audio...")
        audio_data = parse_and_synthesize(morse, user_hz, user_dot_len)
        if play_audio_yn == 'y':
            if len(audio_data) > 0:
                play_audio(audio_data)
            if save_audio_yn == 'y':
                save_audio(file_name, audio_data)
        if play_audio_yn == 'n':
            save_audio(file_name, audio_data)
            print(f"Saved to {file_name}")

run = True
try:
    while run == True:
        print("MORSE TRAINER 1.2.1A BY CORALFOXTHEBEACHFURRY")
        choice = input("What would you like to do?\n1. Text-to-Morse\n2. Morse-to-Text\n3. Text-to-Audio\n4. Morse-to-Audio\n0. Exit\n[ENTER YOUR CHOICE...]\n")
        if choice == '1':
            text = input("Enter text: ").strip().lower()
            print(encode(text))
        elif choice == '2':
            text = input("Enter Morse:").strip().lower()
            print(decode(text))
        elif choice == '3':
            play_audio_yn = input("Do you want to play the audio?(Y for yes, N for save only): ").strip().lower()
            if play_audio_yn != 'n':
                save_audio_yn = input("Do you want to save the resulting audio?(Y for yes, N for play audio only): ")
            convert_to_audio('0', play_audio_yn, save_audio_yn)
        elif choice == '4':
            play_audio_yn = input("Do you want to play the audio?(Y for yes, N for save only): ").strip().lower()
            if play_audio_yn != 'n':
                save_audio_yn = input("Do you want to save the resulting audio?(Y for yes, N for play audio only): ")
            convert_to_audio('1', play_audio_yn, save_audio_yn)
        elif choice == '0':
            print("Goodbye!")
            run = False
        else:
            print("Invalid option!")
except KeyboardInterrupt:
    print("Interrupted, goodbye!")
    run = False
except Exception as e:
    print("Unknown error! Open a issue and include the text after this message.\n", e)
