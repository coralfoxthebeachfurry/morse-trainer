from table import ENCODE_TABLE, DECODE_TABLE

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

run = True
try:
    while run == True:
        print("MORSE TRAINER 1.0A BY CORALFOXTHEBEACHFURRY")
        choice = input("What would you like to do?\n1. Text-to-Morse\n2. Morse-to-Text\n0. Exit\n[ENTER YOUR CHOICE...]\n")
        if choice == '1':
            text = input("Enter text: ").strip().lower()
            print(encode(text))
        elif choice == '2':
            text = input("Enter Morse:").strip().lower()
            print(decode(text))
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