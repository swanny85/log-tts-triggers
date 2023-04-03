# Log Monitor with Text to Speech Readme

This is a Python script that monitors a log file for specific patterns using regular expressions and reads out a customizable message using text-to-speech (TTS) when a pattern is matched.

## Dependencies

- Python 3.6 or higher
- `gtts` library
- `playsound` library

## Usage

1. Clone the repository or download the script file `log_monitor.py`.
2. Install the required libraries using `pip install gtts playsound`.
3. Create a JSON file named `triggers.json` in the same directory as the script. This file contains a list of triggers, where each trigger is an object with two fields: `pattern` (the regular expression pattern to match) and `speech_text` (the message to be read out when the pattern is matched, with `{0}`, `{1}`, etc. as placeholders for matched groups).
4. Run the script using `python log_monitor.py [log_filepath]`, where `[log_filepath]` is the path to the log file to monitor.

## Functionality

When the script is run, it starts two threads: one for monitoring the log file and another for the TTS engine. The log file is monitored continuously, and when a new line is added to the file, it is checked against the list of triggers in `triggers.json`. If a pattern is matched, the corresponding message is added to a queue, which is read by the TTS thread. The TTS engine converts the message to an MP3 file and plays it using the `playsound` library.

The `triggers.json` file should contain a list of triggers, where each trigger is an object with two fields:

- `pattern`: A regular expression pattern to match against log lines. The pattern should contain one or more groups that can be referred to in the `speech_text` field using `{0}`, `{1}`, etc.
- `speech_text`: The message to be read out when the pattern is matched, with `{0}`, `{1}`, etc. as placeholders for matched groups.

Here's an example `triggers.json` file:

```json
[
  {
    "pattern": "(\\w+)\\s+tells you,\\s+'(.+)'",
    "speech_text": "{0} says: {1}"
  },
  {
    "pattern": "Hail",
    "speech_text": "Well, hello there."
  }
]
