import re
import json
import time
import threading
from os.path import getsize
from sys import argv
from queue import Queue
from gtts import gTTS
from playsound import playsound

def load_triggers(filepath):
    with open(filepath, 'r') as f:
        triggers = json.load(f)
    return triggers

def save_triggers(filepath, triggers):
    with open(filepath, 'w') as f:
        json.dump(triggers, f, indent=2)

def process_log_line(log_line, triggers, queue):
    for trigger in triggers:
        pattern = trigger['pattern']
        match = re.search(pattern, log_line)

        if match:
            speech_text = trigger['speech_text'].format(*match.groups())
            queue.put(speech_text)

def monitor_log_file(filepath, triggers, queue):
    file_position = getsize(filepath)

    while True:
        with open(filepath, 'r') as f:
            f.seek(file_position)
            log_line = f.readline().strip()

            if log_line:
                process_log_line(log_line, triggers, queue)
                file_position = f.tell()
            else:
                time.sleep(1)

def tts_engine(queue):
    while True:
        speech_text = queue.get()
        if speech_text == "QUIT":
            break
        tts = gTTS(text=speech_text, lang='en')
        tts.save('temp.mp3')
        playsound('temp.mp3')

def main():
    log_filepath = argv[1]
    triggers_filepath = 'triggers.json'
    triggers = load_triggers(triggers_filepath)

    queue = Queue()

    monitor_thread = threading.Thread(target=monitor_log_file, args=(log_filepath, triggers, queue))
    tts_thread = threading.Thread(target=tts_engine, args=(queue,))

    monitor_thread.start()
    tts_thread.start()

    quit_flag = False
    while not quit_flag:
        print("Menu:")
        print("1. List triggers")
        print("2. Add trigger")
        print("3. Delete trigger")
        print("4. Quit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            for i, trigger in enumerate(triggers, start=1):
                print(f"{i}. {trigger['pattern']} -> {trigger['speech_text']}")
        elif choice == '2':
            pattern = input("Enter regex pattern: ")
            speech_text = input("Enter speech text (use {0}, {1}, etc. for matched groups): ")
            triggers.append({'pattern': pattern, 'speech_text': speech_text})
            save_triggers(triggers_filepath, triggers)
        elif choice == '3':
            index = int(input("Enter the index of the trigger to delete: ")) - 1
            if 0 <= index < len(triggers):
                del triggers[index]
                save_triggers(triggers_filepath, triggers)
            else:
                print("Invalid index.")
        elif choice == '4':
            queue.put("QUIT")
            quit_flag = True
        else:
            print("Invalid choice.")

    monitor_thread.join()
    tts_thread.join()

if __name__ == '__main__':
    main()

